from django.db import models
from django.utils import timezone

class JobDescription(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"JD {self.id}"


class Resume(models.Model):
    job = models.ForeignKey(JobDescription, related_name="resumes", on_delete=models.CASCADE)
    file = models.FileField(upload_to="resumes/")
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)  # extracted text

    def __str__(self):
        return self.filename


class JobHistory(models.Model):
    """
    Stores history of completed job screenings for tracking and retrieval.
    """
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_resumes = models.IntegerField(default=0)
    top_candidate = models.CharField(max_length=255, null=True, blank=True)
    highest_score = models.FloatField(null=True, blank=True)
    # Store full ranking results as JSON
    results_data = models.JSONField(null=True, blank=True)
    job_reference = models.ForeignKey(
        JobDescription, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="history_entries"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Job Histories"

    def __str__(self):
        return f"{self.job_title} - {self.created_at.strftime('%Y-%m-%d')}"


class RankedResult(models.Model):
    """
    Stores individual ranked resume results linked to job history.
    """
    job_history = models.ForeignKey(
        JobHistory, 
        on_delete=models.CASCADE, 
        related_name="ranked_results"
    )
    resume = models.ForeignKey(
        Resume, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    filename = models.CharField(max_length=255)
    keyword_score = models.FloatField()
    semantic_score = models.FloatField()
    final_score = models.FloatField()
    summary = models.TextField(blank=True)
    matching_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    rating = models.FloatField(null=True, blank=True)
    llm_analyzed = models.BooleanField(default=False)
    rank_position = models.IntegerField()

    class Meta:
        ordering = ['rank_position']

    def __str__(self):
        return f"Rank {self.rank_position}: {self.filename}"
