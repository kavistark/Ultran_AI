from django.urls import path
from . import api_views

urlpatterns = [
    path('upload/', api_views.upload_document_api, name='upload_document_api'),
    path('<int:doc_id>/ask/', api_views.ask_document_api, name='ask_document_api'),
]
