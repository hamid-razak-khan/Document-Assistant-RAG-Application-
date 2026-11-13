"""
PDF Report Generator for Resume Screening Results
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime


def generate_candidate_report(candidate_data, job_title, job_description):
    """
    Generate a PDF report for a single candidate.
    
    Args:
        candidate_data: Dict containing candidate resume analysis results
        job_title: Job position title
        job_description: Full job description text
    
    Returns:
        BytesIO buffer containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a56db'),
        spaceAfter=12
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=10,
        spaceBefore=12
    )
    
    story = []
    
    # Title
    story.append(Paragraph("Resume Screening Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Candidate Info
    story.append(Paragraph(f"<b>Candidate:</b> {candidate_data.get('filename', 'N/A')}", styles['Normal']))
    story.append(Paragraph(f"<b>Job Position:</b> {job_title}", styles['Normal']))
    story.append(Paragraph(f"<b>Report Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Scores Section
    story.append(Paragraph("Screening Scores", heading_style))
    
    scores_data = [
        ['Metric', 'Score'],
        ['Final Score', f"{candidate_data.get('final_score', 0):.2f}"],
        ['Keyword Match Score', f"{candidate_data.get('keyword_score', 0):.2f}"],
        ['Semantic Match Score', f"{candidate_data.get('semantic_score', 0):.2f}"],
    ]
    
    if candidate_data.get('rating') is not None:
        scores_data.append(['LLM Skill Match Rating', f"{candidate_data.get('rating', 0):.1f}%"])
    
    scores_table = Table(scores_data, colWidths=[3*inch, 2*inch])
    scores_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e5e7eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
    ]))
    story.append(scores_table)
    story.append(Spacer(1, 0.2*inch))
    
    # LLM Analysis Status
    llm_analyzed = candidate_data.get('llm_analyzed', False)
    if llm_analyzed:
        story.append(Paragraph(
            "<b>✓ LLM Analysis:</b> Completed",
            styles['Normal']
        ))
    else:
        story.append(Paragraph(
            "<b>⚠ LLM Analysis:</b> Skipped (API limit optimization - algorithmic score only)",
            styles['Normal']
        ))
    story.append(Spacer(1, 0.2*inch))
    
    # Summary
    story.append(Paragraph("Candidate Summary", heading_style))
    summary = candidate_data.get('summary', 'No summary available')
    story.append(Paragraph(summary, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Matching Skills
    story.append(Paragraph("Matching Skills", heading_style))
    matching_skills = candidate_data.get('matching_skills', [])
    if isinstance(matching_skills, list) and matching_skills:
        skills_text = ", ".join(matching_skills)
        story.append(Paragraph(skills_text, styles['BodyText']))
    else:
        story.append(Paragraph("No matching skills identified", styles['Italic']))
    story.append(Spacer(1, 0.2*inch))
    
    # Missing Skills
    story.append(Paragraph("Missing Skills", heading_style))
    missing_skills = candidate_data.get('missing_skills', [])
    if isinstance(missing_skills, list) and missing_skills:
        skills_text = ", ".join(missing_skills)
        story.append(Paragraph(skills_text, styles['BodyText']))
    else:
        story.append(Paragraph("No missing skills identified", styles['Italic']))
    story.append(Spacer(1, 0.2*inch))
    
    # Recommendation
    story.append(Paragraph("Recommendation", heading_style))
    final_score = candidate_data.get('final_score', 0)
    if final_score >= 70:
        recommendation = "✓ <b>Highly Recommended</b> - Strong match for the position"
        color = colors.HexColor('#059669')
    elif final_score >= 50:
        recommendation = "→ <b>Recommended</b> - Good match, consider for interview"
        color = colors.HexColor('#d97706')
    else:
        recommendation = "✗ <b>Not Recommended</b> - Limited match for the position"
        color = colors.HexColor('#dc2626')
    
    rec_style = ParagraphStyle(
        'Recommendation',
        parent=styles['Normal'],
        textColor=color,
        fontSize=12
    )
    story.append(Paragraph(recommendation, rec_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Job Description Reference
    story.append(Paragraph("Job Description Reference", heading_style))
    job_desc_text = job_description[:500] + "..." if len(job_description) > 500 else job_description
    story.append(Paragraph(job_desc_text, styles['BodyText']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_full_screening_report(results, job_title, job_description):
    """
    Generate a comprehensive PDF report for all candidates.
    
    Args:
        results: List of candidate result dictionaries
        job_title: Job position title
        job_description: Full job description text
    
    Returns:
        BytesIO buffer containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a56db'),
        spaceAfter=12
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=10,
        spaceBefore=12
    )
    
    story = []
    
    # Title
    story.append(Paragraph("Complete Screening Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Job Info
    story.append(Paragraph(f"<b>Job Position:</b> {job_title}", styles['Normal']))
    story.append(Paragraph(f"<b>Total Candidates:</b> {len(results)}", styles['Normal']))
    story.append(Paragraph(f"<b>Report Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Summary Table
    story.append(Paragraph("Candidate Rankings", heading_style))
    
    table_data = [['Rank', 'Candidate', 'Final Score', 'LLM Analysis']]
    for idx, result in enumerate(results, 1):
        llm_status = "✓" if result.get('llm_analyzed', False) else "✗"
        table_data.append([
            str(idx),
            result.get('filename', 'N/A'),
            f"{result.get('final_score', 0):.2f}",
            llm_status
        ])
    
    results_table = Table(table_data, colWidths=[0.8*inch, 3*inch, 1.5*inch, 1.2*inch])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
    ]))
    story.append(results_table)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
