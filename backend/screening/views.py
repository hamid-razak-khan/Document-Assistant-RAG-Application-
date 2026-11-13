import os
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Q

from .models import JobDescription, Resume, JobHistory, RankedResult
from .serializers import (
    JobDescriptionSerializer, 
    ResumeSerializer, 
    JobHistorySerializer,
    JobHistoryListSerializer
)
from .rag_pipeline import index_resume, rank_resumes
from .pdf_generator import generate_candidate_report, generate_full_screening_report


@api_view(["POST"])
def create_job_description(request):
    """
    Body: { "title": "", "text": "JD text..." }
    """
    serializer = JobDescriptionSerializer(data=request.data)
    if serializer.is_valid():
        jd = serializer.save()
        return Response(JobDescriptionSerializer(jd).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def upload_resumes(request, job_id):
    """
    Upload one or more resumes for a specific job.
    Form-data: files[]: <file1>, <file2> ...
    """
    try:
        job = get_object_or_404(JobDescription, pk=job_id)
        print(f"Received upload request for job {job_id}")

        files = request.FILES.getlist("files")
        print(f"Number of files received: {len(files)}")
        
        if not files:
            return Response({"error": "No files provided"}, status=status.HTTP_400_BAD_REQUEST)
            
        created = []

        for i, f in enumerate(files):
            try:
                print(f"Processing file {i+1}: {f.name}")
                resume = Resume.objects.create(
                    job=job,
                    file=f,
                    filename=f.name,
                )
                file_path = resume.file.path
                full_text = index_resume(job.id, resume.id, resume.filename, file_path)
                resume.text = full_text
                resume.save()

                # Serialize the resume data
                serialized_data = ResumeSerializer(resume).data
                print(f"Serialized resume data: {serialized_data}")
                created.append(serialized_data)
                print(f"Finished processing file {i+1}: {f.name}")
            except Exception as e:
                # If there's an error with one file, continue with others
                print(f"Error processing file {f.name}: {str(e)}")
                # Log the full traceback for debugging
                import traceback
                traceback.print_exc()
                continue

        print(f"All files processed. Created {len(created)} resumes.")
        # Send a simplified response to avoid potential serialization issues
        response_data = {
            "message": f"Successfully uploaded {len(created)} resumes", 
            "count": len(created),
            "resumes": created
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"Error in upload_resumes: {str(e)}")
        # Log the full traceback for debugging
        import traceback
        traceback.print_exc()
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_resumes(request, job_id):
    job = get_object_or_404(JobDescription, pk=job_id)
    resumes = job.resumes.all().order_by("-uploaded_at")
    serializer = ResumeSerializer(resumes, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def process_screening(request, job_id):
    """
    Process ranking for all resumes under a job.
    Body: none (job_id in path)
    """
    job = get_object_or_404(JobDescription, pk=job_id)
    job_text = job.text

    resumes_qs = job.resumes.all()
    if not resumes_qs.exists():
        return Response({"detail": "No resumes uploaded."}, status=status.HTTP_400_BAD_REQUEST)

    resumes = [
        {"id": r.id, "filename": r.filename, "text": r.text}
        for r in resumes_qs
    ]

    ranked = rank_resumes(job_text, resumes)

    # Save to JobHistory
    if ranked:
        top_candidate = ranked[0]["filename"]
        highest_score = ranked[0]["final_score"]
    else:
        top_candidate = None
        highest_score = None

    job_history = JobHistory.objects.create(
        job_title=job.title,
        job_description=job.text,
        total_resumes=len(ranked),
        top_candidate=top_candidate,
        highest_score=highest_score,
        results_data=ranked,
        job_reference=job
    )

    # Save individual ranked results
    for idx, result in enumerate(ranked, 1):
        RankedResult.objects.create(
            job_history=job_history,
            resume_id=result["resume_id"],
            filename=result["filename"],
            keyword_score=result["keyword_score"],
            semantic_score=result["semantic_score"],
            final_score=result["final_score"],
            summary=result["summary"],
            matching_skills=result["matching_skills"],
            missing_skills=result["missing_skills"],
            rating=result.get("rating"),
            llm_analyzed=result.get("llm_analyzed", False),
            rank_position=idx
        )

    return Response(
        {
            "job": JobDescriptionSerializer(job).data,
            "results": ranked,
            "history_id": job_history.id,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def get_job_history(request):
    """
    Get list of all job screening history.
    Query params:
        - search: Filter by job title
    """
    search_term = request.query_params.get('search', '')
    
    history = JobHistory.objects.all()
    
    if search_term:
        history = history.filter(
            Q(job_title__icontains=search_term) |
            Q(job_description__icontains=search_term)
        )
    
    serializer = JobHistoryListSerializer(history, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_job_history_details(request, history_id):
    """
    Get detailed results for a specific job history entry.
    """
    history = get_object_or_404(JobHistory, pk=history_id)
    serializer = JobHistorySerializer(history)
    return Response(serializer.data)


@api_view(["DELETE"])
def delete_job_history(request, history_id):
    """
    Delete a job history entry.
    """
    history = get_object_or_404(JobHistory, pk=history_id)
    history.delete()
    return Response({"detail": "History deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["DELETE"])
def clear_all_history(request):
    """
    Clear all job history entries.
    """
    JobHistory.objects.all().delete()
    return Response({"detail": "All history cleared successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def download_candidate_pdf(request, history_id, result_id):
    """
    Download PDF report for a specific candidate.
    """
    history = get_object_or_404(JobHistory, pk=history_id)
    result = get_object_or_404(RankedResult, pk=result_id, job_history=history)
    
    candidate_data = {
        "filename": result.filename,
        "final_score": result.final_score,
        "keyword_score": result.keyword_score,
        "semantic_score": result.semantic_score,
        "summary": result.summary,
        "matching_skills": result.matching_skills,
        "missing_skills": result.missing_skills,
        "rating": result.rating,
        "llm_analyzed": result.llm_analyzed,
    }
    
    pdf_buffer = generate_candidate_report(
        candidate_data,
        history.job_title,
        history.job_description
    )
    
    response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{result.filename}_report.pdf"'
    return response


@api_view(["GET"])
def download_full_report_pdf(request, history_id):
    """
    Download complete PDF report for all candidates in a job history.
    """
    history = get_object_or_404(JobHistory, pk=history_id)
    
    # Use results_data if available, otherwise build from RankedResult
    if history.results_data:
        results = history.results_data
    else:
        ranked_results = history.ranked_results.all()
        results = [
            {
                "filename": r.filename,
                "final_score": r.final_score,
                "keyword_score": r.keyword_score,
                "semantic_score": r.semantic_score,
                "summary": r.summary,
                "matching_skills": r.matching_skills,
                "missing_skills": r.missing_skills,
                "rating": r.rating,
                "llm_analyzed": r.llm_analyzed,
            }
            for r in ranked_results
        ]
    
    pdf_buffer = generate_full_screening_report(
        results,
        history.job_title,
        history.job_description
    )
    
    response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{history.job_title}_full_report.pdf"'
    return response


@api_view(["GET"])
def get_resume_text(request, resume_id):
    """
    Get extracted text from a resume for preview.
    """
    resume = get_object_or_404(Resume, pk=resume_id)
    return Response({
        "id": resume.id,
        "filename": resume.filename,
        "text": resume.text,
        "uploaded_at": resume.uploaded_at,
    })


# ============================================================
# EMAIL SENDING FEATURE
# ============================================================

import re
from django.core.mail import send_mail


def extract_email_from_text(text):
    """
    Extract the first email address from text using regex.
    """
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else None


@api_view(["POST"])
def preview_bulk_email(request):
    """
    Preview candidates based on different filtering modes without sending emails.
    
    Supported modes:
    1. top_n: Preview top N candidates
    2. score_threshold: Preview candidates with final score >= X
    3. selected: Preview explicit list of resume IDs
    
    Expected request data:
    {
        "mode": "top_n" | "score_threshold" | "selected",
        "count": 3,  # Required for top_n mode
        "score": 75,  # Required for score_threshold mode
        "resume_ids": [1, 2, 3],  # Required for selected mode
    }
    """
    try:
        mode = request.data.get("mode")
        
        if not mode:
            return Response(
                {"error": "Mode is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all ranked results
        all_results = RankedResult.objects.select_related('resume').all()
        
        # Filter candidates based on mode
        filtered_results = []
        
        if mode == "top_n":
            count = request.data.get("count", 3)
            filtered_results = all_results.order_by('-final_score')[:count]
            
        elif mode == "score_threshold":
            score_threshold = request.data.get("score", 75)
            filtered_results = all_results.filter(final_score__gte=score_threshold)
            
        elif mode == "selected":
            resume_ids = request.data.get("resume_ids", [])
            filtered_results = all_results.filter(resume_id__in=resume_ids)
            
        else:
            return Response(
                {"error": "Invalid mode. Supported modes: top_n, score_threshold, selected"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract emails for preview
        candidates = []
        
        for result in filtered_results:
            # Extract email from resume text
            email = None
            if result.resume and result.resume.text:
                email = extract_email_from_text(result.resume.text)
            
            candidates.append({
                "id": result.resume_id,
                "email": email,
                "candidate": result.filename,
                "score": result.final_score
            })
        
        return Response({
            "candidates": candidates,
            "total_candidates": len(candidates)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"Failed to preview candidates: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
def send_bulk_email(request):
    """
    Send bulk emails to candidates based on different filtering modes.
    
    Supported modes:
    1. top_n: Send to top N candidates
    2. score_threshold: Send to candidates with final score >= X
    3. selected: Send to explicit list of resume IDs
    
    Expected request data:
    {
        "mode": "top_n" | "score_threshold" | "selected",
        "count": 3,  # Required for top_n mode
        "score": 75,  # Required for score_threshold mode
        "resume_ids": [1, 2, 3],  # Required for selected mode
        "message": "Custom email message here"
    }
    """
    try:
        mode = request.data.get("mode")
        message = request.data.get("message", "")
        
        if not mode or not message:
            return Response(
                {"error": "Both 'mode' and 'message' are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all ranked results
        all_results = RankedResult.objects.select_related('resume').all()
        
        # Filter candidates based on mode
        filtered_results = []
        
        if mode == "top_n":
            count = request.data.get("count", 3)
            filtered_results = all_results.order_by('-final_score')[:count]
            
        elif mode == "score_threshold":
            score_threshold = request.data.get("score", 75)
            filtered_results = all_results.filter(final_score__gte=score_threshold)
            
        elif mode == "selected":
            resume_ids = request.data.get("resume_ids", [])
            filtered_results = all_results.filter(resume_id__in=resume_ids)
            
        else:
            return Response(
                {"error": "Invalid mode. Supported modes: top_n, score_threshold, selected"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract emails and send
        sent_to = []
        skipped = []
        
        for result in filtered_results:
            # Extract email from resume text
            email = None
            if result.resume and result.resume.text:
                email = extract_email_from_text(result.resume.text)
            
            if email:
                try:
                    send_mail(
                        subject=f"Job Application Update - {result.job_history.job_title}",
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                    sent_to.append({
                        "email": email,
                        "candidate": result.filename,
                        "score": result.final_score
                    })
                except Exception as e:
                    skipped.append({
                        "email": email,
                        "candidate": result.filename,
                        "reason": f"Failed to send email: {str(e)}"
                    })
            else:
                skipped.append({
                    "candidate": result.filename,
                    "reason": "No email found in resume"
                })
        
        return Response({
            "sent_to": sent_to,
            "skipped": skipped,
            "total_sent": len(sent_to),
            "total_skipped": len(skipped)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"Failed to send emails: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
