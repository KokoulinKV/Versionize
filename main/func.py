import os
import zipfile

from django.http import Http404, HttpResponse
from transliterate import translit

from Versionize import settings


def download_some_files(zip_name, document_dir, files_download):
    translit_zip_name = translit(zip_name, language_code='ru', reversed=True)
    zip_path = f'{settings.MEDIA_ROOT}/downloads/{zip_name}'
    archive = zipfile.ZipFile(zip_path, 'w')
    rootdir = os.path.basename(document_dir)

    for root, dir, files in os.walk(document_dir):
        for file in files:
            if file in files_download:
                filepath = os.path.join(root, file)
                parentpath = os.path.relpath(filepath, document_dir)
                arcname = os.path.join(rootdir, parentpath)
                archive.write(filepath, arcname)
    archive.close()

    if os.path.exists(zip_path):
        with open(zip_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/zip", )
            response['Content-Disposition'] = 'inline; filename=' + f'{translit_zip_name}'
            return response
    raise Http404

def download_single_file(path):
    dir, document = path.split('/')
    document_dir = os.path.join(settings.MEDIA_ROOT, dir)
    translit_doc_name= translit(document, language_code='ru', reversed=True)
    zip_name = f'{translit_doc_name}.zip'
    zip_path = f'{settings.MEDIA_ROOT}/downloads/{zip_name}'
    archive = zipfile.ZipFile(zip_path, 'w')
    rootdir = os.path.basename(document_dir)

    for root, dir, files in os.walk(document_dir):
        for file in files:
            if file == document:
                filepath = os.path.join(root, file)
                parentpath = os.path.relpath(filepath, document_dir)
                arcname = os.path.join(rootdir, parentpath)
                archive.write(filepath, arcname)

    archive.close()


    if os.path.exists(zip_path):
        with open(zip_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream", )
            response['Content-Disposition'] = 'inline; filename=' + f'{zip_name}'
            return response
    raise Http404



def ajax_check(request):
    # Проверяем отправлен ли нам post запрос через ajax
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return True
    return False

def _get_form(request, formcls, prefix, user=None):
    if prefix in request.POST:
        data = request.POST
        if request.FILES:
            files = request.FILES
            return formcls(data, files, prefix=prefix)
        elif user:
            return formcls(user, data, prefix=prefix)
    else:
        data = None
    return formcls(data, prefix=prefix)


def clear_form_data(form_data):
    """
    Clears the values of the immutable QueryDict instance
    """
    empty_dict = {'csrfmiddlewaretoken': form_data['csrfmiddlewaretoken']}
    for key in form_data.keys():
        empty_dict[form_data[key]] = ''
    return empty_dict