import pillow_heif
pillow_heif.register_heif_opener()

import os
import zipfile
from django.shortcuts import render, redirect
from django.conf import settings
from .models import UploadSession, UploadedImage
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from uuid import uuid4

from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

def upload_view(request):
    if request.method == 'POST':
        files = request.FILES.getlist('images')
        class_string = request.POST.get('classCount', '').strip()

        if not files or not class_string:
            return render(request, 'index.html', {'error': 'Please upload files and enter classes.'})

        session = UploadSession.objects.create(class_names=class_string)

        for file in files:
            filename = file.name.lower()

            if filename.endswith('.zip'):
                zf = zipfile.ZipFile(file)
                for zip_info in zf.infolist():
                    name = os.path.basename(zip_info.filename)
                    ext = name.lower().split('.')[-1]

                    if ext in ['jpg', 'jpeg', 'png', 'webp']:
                        file_data = zf.read(zip_info.filename)
                        saved_name = f"sessions/{session.id}/{uuid4()}_{name}"
                        default_storage.save(saved_name, ContentFile(file_data))
                        UploadedImage.objects.create(session=session, image=saved_name)

                    elif ext == 'heic':
                        try:
                            file_data = zf.read(zip_info.filename)
                            image = Image.open(io.BytesIO(file_data)).convert("RGB")
                            buffer = io.BytesIO()
                            image.save(buffer, format="JPEG")
                            buffer.seek(0)
                            new_name = name.rsplit('.', 1)[0] + ".jpg"
                            saved_name = f"sessions/{session.id}/{uuid4()}_{new_name}"
                            default_storage.save(saved_name, ContentFile(buffer.read()))
                            UploadedImage.objects.create(session=session, image=saved_name)
                        except Exception as e:
                            print(f"Failed to convert HEIC in zip: {e}")

            else:
                if filename.endswith('.heic'):
                    try:
                        image = Image.open(file).convert("RGB")
                        buffer = io.BytesIO()
                        image.save(buffer, format="JPEG")
                        buffer.seek(0)
                        new_name = file.name.rsplit('.', 1)[0] + ".jpg"
                        converted_file = InMemoryUploadedFile(
                            buffer, None, new_name, 'image/jpeg', buffer.getbuffer().nbytes, None
                        )
                        UploadedImage.objects.create(session=session, image=converted_file)
                    except Exception as e:
                        print(f"Failed to convert direct HEIC: {e}")
                else:
                    UploadedImage.objects.create(session=session, image=file)

        return redirect('label', session_id=session.id)

    return render(request, 'index.html')




from django.shortcuts import get_object_or_404
from .models import UploadSession, UploadedImage, LabeledImage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def label_view(request, session_id):
    session = get_object_or_404(UploadSession, id=session_id)
    class_list = session.get_class_list()

    # All images in consistent order
    all_images = session.images.order_by('id')
    image_ids = list(all_images.values_list('id', flat=True))

    # Get index from request
    index = int(request.GET.get('index', 0))
    if index < 0:
        index = 0
    elif index >= len(image_ids):
        index = len(image_ids) - 1

    image = all_images[index]
    try:
        label_obj = LabeledImage.objects.get(image=image)
        current_label = label_obj.label
    except LabeledImage.DoesNotExist:
        label_obj = None
        current_label = None

    return render(request, 'label.html', {
        'session': session,
        'image': image,
        'classes': class_list,
        'current_index': index,
        'total': len(image_ids),
        'current_label': current_label,
        'is_labeled': label_obj is not None,
    })


@csrf_exempt
def save_label(request):
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        label = request.POST.get('label')
        index = request.POST.get('index', 0)

        try:
            image = UploadedImage.objects.get(id=image_id)
            labeled, created = LabeledImage.objects.get_or_create(image=image)
            labeled.label = label
            labeled.save()
            return redirect(f'/label/{image.session.id}/?index={int(index) + 1}')
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})



import io
import zipfile
from django.http import HttpResponse
from django.utils.text import slugify

def download_zips(request, session_id):
    session = get_object_or_404(UploadSession, id=session_id)
    labeled_images = LabeledImage.objects.filter(image__session=session)

    # Group images by label
    label_groups = {}
    for li in labeled_images:
        label_groups.setdefault(li.label, []).append(li.image)

    # Create an in-memory ZIP file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for label, images in label_groups.items():
            label_folder = slugify(label)
            for img in images:
                img_path = img.image.path
                filename = os.path.basename(img_path)
                arcname = f"{label_folder}/{filename}"
                zipf.write(img_path, arcname)

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename=classified_session_{session.id}.zip'
    return response




from django.db.models import Count

def session_list(request):
    sessions = UploadSession.objects.annotate(
        total_images=Count('images'),
        labeled_images=Count('images__label')
    ).order_by('-created_at')

    return render(request, 'session_list.html', {
        'sessions': sessions
    })


def relabel_view(request, session_id):
    session = get_object_or_404(UploadSession, id=session_id)
    class_list = session.get_class_list()
    labeled_images = LabeledImage.objects.filter(image__session=session).select_related('image')

    if request.method == 'POST':
        new_label = request.POST.get('new_label')
        label_id = request.POST.get('label_id')
        label_obj = get_object_or_404(LabeledImage, id=label_id)
        if new_label in class_list:
            label_obj.label = new_label
            label_obj.save()
        return redirect('relabel', session_id=session_id)

    return render(request, 'relabel.html', {
        'session': session,
        'labeled_images': labeled_images,
        'classes': class_list,
    })


from django.views.decorators.http import require_POST
import shutil

@require_POST
def delete_session(request, session_id):
    session = get_object_or_404(UploadSession, id=session_id)

    # Delete image files from media storage
    session_folder = os.path.join(settings.MEDIA_ROOT, 'sessions', str(session.id))
    if os.path.exists(session_folder):
        shutil.rmtree(session_folder)

    # Delete database entries
    session.delete()
    return redirect('session_list')
