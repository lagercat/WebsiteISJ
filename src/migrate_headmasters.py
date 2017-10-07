import os

import django
from openpyxl import load_workbook

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from authentication.models import ExtendedUser

wb = load_workbook('retea.xlsx')

for sheet in wb.get_sheet_names():
    for row in range(2, wb[sheet].max_row):
        eliminating_word = ''
        school_name_file_row = 'B' + str(row)
        headmaster_name_file_row = 'C' + str(row)
        school_name = wb[sheet][school_name_file_row].value
        head_master_name = wb[sheet][headmaster_name_file_row]
        """
        for word in to_eliminate:
            if word in school_name:
                eliminating_word = word
                break
        if eliminating_word:
            school_name = school_name.split(eliminating_word)[0]
        """
        ExtendedUser.objects.create(name=school_name)
