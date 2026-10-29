from django.urls import path
from . import views

urlpatterns = [
    path('', views.documents_view, name='documents'),
    path('upload/', views.upload_document_view, name='upload_document'),
    path('<int:doc_id>/analyze/', views.document_analyze_view, name='document_analyze'),
    path('<int:doc_id>/delete/', views.document_delete_view, name='document_delete'),
]
