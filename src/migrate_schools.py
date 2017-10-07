import os

import django
from openpyxl import load_workbook
from geopy.geocoders import Nominatim


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from school.models import School

wb = load_workbook('retea.xlsx')

to_eliminate = ['MUN', 'COM', 'ORAS']

for sheet in wb.get_sheet_names():
    for row in range(2, wb[sheet].max_row):
        eliminating_word = ''
        geolocator = Nominatim()
        name_file_row = 'B' + str(row)
        address_file_row = 'C' + str(row)
        school_name = wb[sheet][name_file_row].value
        school_adress = wb[sheet][address_file_row].value
        """
        for word in to_eliminate:
            if word in school_name:
                eliminating_word = word
                break
        if eliminating_word:
            school_name = school_name.split(eliminating_word)[0]
        """
        address_partitioned = school_adress.split(",")
        address_partitioned.pop(0)
        address_partitioned.pop(0)
        address_partitioned.pop(len(address_partitioned) - 1)
        for i in range(0, len(address_partitioned) - 1):
            address_partitioned[i] += " "
        school_adress = "".join(address_partitioned)
        try:
            school_location = geolocator.geocode(school_adress)
            school_coordinates = str(school_location.latitude) + "," + str(school_location.longitude)
            School.objects.create(name=school_name,
                                  address=school_location.address,
                                  geolocation=school_coordinates)
        except AttributeError:
            print school_adress + "\n"
