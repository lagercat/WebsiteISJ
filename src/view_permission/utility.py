'''
Created on Feb 13, 2017

@author: roadd
'''
import os
import magic


mime_documents_types = [
    'application/msword', 
    'application/vnd.openxmlformats-officedocument',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.template',
    'application/vnd.openxmlformats-officedocument.presentationml.template',
    'application/vnd.openxmlformats-officedocument.presentationml.slideshow',
    'application/vnd.ms-powerpointtd',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/vnd.openxmlformats-officedocument.presentationml.slide',
    'application/x-tar',
    'text/plain',
    'application/vnd.ms-excel.addin.macroEnabled.12',
    'application/vnd.ms-excel',
    'application/vnd.ms-excel.sheet.binary.macroEnabled.12',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.template',
    'application/xml',
    'application/zip', 
    'application/x-compressed-zip',
    'application/msword',
    'application/x-compressed',
    'multipart/x-gzip',
    'application/vnd.ms-project',
    'application/x-project',
    'application/mspowerpoint',
    'application/vnd.ms-powerpoint',
    'application/powerpoint',
    'application/x-mspowerpoint',
    'text/richtext',
    'text/vnd.rn-realtext',
    'application/rtf',
    'application/x-rtf'
    'application/gnutar',
    'application/msword',
    'application/excel',
    'application/x-excel',
    'application/x-msexcel',
    'application/vnd.ms-excel',
    'application/x-zip-compressed',
    'application/zip',
    'multipart/x-zip',
    'application/rtf',
    'application/pdf',
    "application/x-gzip",
    "application/vnd.oasis.opendocument",
    'application/vnd.openofficeorg',
    'application/x-rar-compressed', 
    'application/octet-stream',
]

def clean_file(file, image=False):
    max_size = 10000000  # 10 MB
    filetype = magic.from_buffer(file.read(), mime=True)
    print (not image and not any(filetype.startswith(mime) for mime in mime_documents_types))
    if file.size > max_size:
        return "Fisierul trece de dimensiunea maxima de %d." % max_size
    
    if filetype.startswith("image/"):
        pass
    elif not image and not any(filetype.startswith(mime) or () for mime in mime_documents_types):
        return "Fisierul nu se incadreaza in mime type-urile acceptate. Se poate ca fisierul sa fie corupt."
    return ""