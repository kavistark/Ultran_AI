import os
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import UploadedDocument


ALLOWED_TYPES = {
    'application/pdf': '.pdf',
    'text/plain': '.txt',
    'text/markdown': '.md',
}


@login_required
def documents_view(request):
    return redirect('home')


@login_required
def upload_document_view(request):
    if request.method == 'POST' and request.FILES.get('document'):
        uploaded_file = request.FILES['document']

        # Validate size
        max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024)
        if uploaded_file.size > max_size:
            messages.error(request, 'File too large. Maximum size is 10 MB.')
            return redirect('home')

        # Validate type (check content-type and extension)
        content_type = uploaded_file.content_type
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        allowed_exts = {'.pdf', '.txt', '.md'}
        if ext not in allowed_exts and content_type not in ALLOWED_TYPES:
            messages.error(request, 'File type not supported. Use PDF, TXT, or Markdown files.')
            return redirect('home')

        file_type = 'application/pdf' if ext == '.pdf' else 'text/plain'

        doc = UploadedDocument.objects.create(
            user=request.user,
            name=uploaded_file.name,
            file=uploaded_file,
            file_type=file_type,
            file_size=uploaded_file.size,
        )
        messages.success(request, f'"{doc.name}" uploaded successfully.')
        return redirect('home')

    return redirect('home')


@login_required
def document_analyze_view(request, doc_id):
    return redirect('home')


@login_required
def document_delete_view(request, doc_id):
    doc = get_object_or_404(UploadedDocument, id=doc_id, user=request.user)
    if request.method == 'POST':
        if doc.file:
            try:
                if os.path.exists(doc.file.path):
                    os.remove(doc.file.path)
            except Exception:
                pass
        doc.delete()
        messages.success(request, 'Document deleted.')
    return redirect('home')
