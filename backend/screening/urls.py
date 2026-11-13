from django.urls import path
from . import views

urlpatterns = [
    # Job Description endpoints
    path("jobs/", views.create_job_description, name="create_job"),
    path("jobs/<int:job_id>/resumes/", views.upload_resumes, name="upload_resumes"),
    path("jobs/<int:job_id>/resumes/list/", views.get_resumes, name="list_resumes"),
    path("jobs/<int:job_id>/rank/", views.process_screening, name="process_screening"),
    
    # Resume preview endpoint
    path("resumes/<int:resume_id>/text/", views.get_resume_text, name="get_resume_text"),
    
    # Job History endpoints
    path("history/", views.get_job_history, name="job_history"),
    path("history/<int:history_id>/", views.get_job_history_details, name="job_history_details"),
    path("history/<int:history_id>/delete/", views.delete_job_history, name="delete_job_history"),
    path("history/clear/", views.clear_all_history, name="clear_all_history"),
    
    # Email endpoints
    path("preview-bulk-email/", views.preview_bulk_email, name="preview_bulk_email"),
    path("send-bulk-email/", views.send_bulk_email, name="send_bulk_email"),
    
    # PDF Download endpoints
    path("history/<int:history_id>/download/", views.download_full_report_pdf, name="download_full_report"),
    path("history/<int:history_id>/results/<int:result_id>/download/", views.download_candidate_pdf, name="download_candidate_pdf"),
]
