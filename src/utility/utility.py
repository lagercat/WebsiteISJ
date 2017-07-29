# Copyright 2017 Adrian-Ioan Garovat, Emanuel Covaci, Sebastian-Valeriu Males
#
# This file is part of WebsiteISJ
#
# WebsiteISJ is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WebsiteISJ is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WebsiteISJ.   If not, see <http://www.gnu.org/licenses/>.
import magic

mime_documents_types = [
    'application/msword',
    'application/vnd.openxmlformats-officedocument',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.template',
    'application/vnd.openxmlformats-officedocument.presentationml.template',
    'application/vnd.openxmlformats-officedocument.presentationml.slideshow',
    'application/vnd.ms-powerpointtd',
    'application/vnd.openxmlformats-officedocument.'
    'presentationml.presentation',
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
    if file:
        filetype = magic.from_buffer(file.read(), mime=True)

        if file.size > max_size:
            return "Fisierul trece de dimensiunea "
            "maxima de %d MB." % (max_size / 1000000)

        if filetype.startswith("image/"):
            pass
        elif image and any(filetype.startswith(mime) for mime in mime_documents_types):
            return "Fisierul nu se incadreaza in mime type-urile acceptate. Se poate ca fisierul sa fie corupt."
        elif not any(filetype.startswith(mime) for mime in mime_documents_types):
            return "Fisierul nu se incadreaza in mime type-urile acceptate. Se poate ca fisierul sa fie corupt."
        return ""
