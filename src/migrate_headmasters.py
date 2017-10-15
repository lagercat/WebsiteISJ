import os
import unicodedata

import django
from openpyxl import load_workbook

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from authentication.models import ExtendedUser
from school.models import School

wb = load_workbook('retea.xlsx')

for sheet in wb.get_sheet_names():
    for row in range(2, wb[sheet].max_row):
        school_name_file_row = 'B' + str(row)
        headmaster_name_file_row = 'D' + str(row)
        school_name = wb[sheet][school_name_file_row].value
        headmaster_name = wb[sheet][headmaster_name_file_row].value
        headmaster_splitted = headmaster_name.split(" ")
        username = (headmaster_splitted[0] + "_" +
                    headmaster_splitted[len(headmaster_splitted) - 1]).lower()
        username = unicodedata.normalize(
                "NFKD", username).encode("ascii", "ignore")
        first_name = username.split("_")[1].title()
        last_name = username.split("_")[0].title()
        try:
            school = School.objects.get(name=school_name)
            if ExtendedUser.objects.filter(username=username).count():
                headms = ExtendedUser.objects.get(username=username)
                headms.school = 
            else:
                user = ExtendedUser.objects.create(username=username,
                                                   first_name=first_name,
                                                   last_name=last_name,
                                                   status=1,
                                                   school=school)
                user.set_password("aloha123")
                user.save()
        except School.DoesNotExist:
            print username
