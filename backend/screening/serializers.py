from rest_framework import serializers
from .models import JobDescription, Resume, JobHistory, RankedResult

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = ["id", "title", "text", "created_at"]


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "job", "filename", "uploaded_at", "text"]
        read_only_fields = ["text", "uploaded_at"]


class RankedResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RankedResult
        fields = [
            "id", "filename", "keyword_score", "semantic_score",
            "final_score", "summary", "matching_skills", "missing_skills",
            "rating", "llm_analyzed", "rank_position"
        ]


class JobHistorySerializer(serializers.ModelSerializer):
    ranked_results = RankedResultSerializer(many=True, read_only=True)
    
    class Meta:
        model = JobHistory
        fields = [
            "id", "job_title", "job_description", "created_at",
            "total_resumes", "top_candidate", "highest_score",
            "results_data", "ranked_results"
        ]
        read_only_fields = ["created_at"]


class JobHistoryListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing job history without full results."""
    class Meta:
        model = JobHistory
        fields = [
            "id", "job_title", "created_at",
            "total_resumes", "top_candidate", "highest_score"
        ]
