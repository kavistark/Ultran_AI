import json
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import UploadedDocument
from assistant.services import analyze_document_with_gemini


def extract_text(doc):
    """Extract text from document file."""
    try:
        file_path = doc.file.path
        if doc.file_type == 'application/pdf' or doc.name.lower().endswith('.pdf'):
            try:
                import PyPDF2
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = '\n'.join(page.extract_text() or '' for page in reader.pages)
                return text
            except ImportError:
                return "PDF reading requires PyPDF2. Please install it."
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


@login_required
@require_http_methods(["POST"])
def ask_document_api(request, doc_id):
    doc = get_object_or_404(UploadedDocument, id=doc_id, user=request.user)
    try:
        data = json.loads(request.body)
        question = data.get('question', '').strip()
        if not question:
            return JsonResponse({'error': 'Question cannot be empty.'}, status=400)

        content = extract_text(doc)
        result = analyze_document_with_gemini(content, doc.name, question)

        if result['error']:
            return JsonResponse({'error': result['error']}, status=503)

        return JsonResponse({'response': result['text']})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def upload_document_api(request):
    if not request.FILES.get('document'):
        return JsonResponse({'error': 'No file uploaded.'}, status=400)

    uploaded_file = request.FILES['document']
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024)
    if uploaded_file.size > max_size:
        return JsonResponse({'error': 'File too large (maximum size is 10 MB).'}, status=400)

    ext = os.path.splitext(uploaded_file.name)[1].lower()
    if ext not in ['.pdf', '.txt', '.md']:
        return JsonResponse({'error': 'Unsupported file format. Please upload PDF, TXT, or Markdown.'}, status=400)

    file_type = 'application/pdf' if ext == '.pdf' else 'text/plain'
    doc = UploadedDocument.objects.create(
        user=request.user,
        name=uploaded_file.name,
        file=uploaded_file,
        file_type=file_type,
        file_size=uploaded_file.size,
    )
    return JsonResponse({
        'success': True,
        'doc_id': doc.id,
        'name': doc.name,
        'size': doc.file_size,
    })
