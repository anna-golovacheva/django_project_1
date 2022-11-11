import csv
import json

from django.core.management.base import BaseCommand
from ads.models import Ads, Categories


class Command(BaseCommand):
    def upload_data_to_json(self, data_list, jsonfile):
        list_of_keys = data_list[0].copy()
        del data_list[0]
        list_of_dicts = []
        for lst in data_list:
            d_dict = {k: v for k, v in zip(list_of_keys, lst)}
            list_of_dicts.append(d_dict)

        with open(jsonfile, 'w', encoding='utf-8') as json_file:
            json.dump(list_of_dicts, json_file, ensure_ascii=False)

    def handle(self, *args, **options):
        data_1 = []
        with open('ads.csv', 'r', encoding='utf-8') as a_csv_file:
            reader = csv.reader(a_csv_file, delimiter=',')
            for row in reader:
                data_1.append(row)

        self.upload_data_to_json(data_1, 'ads.json')

        with open('ads.json', 'r', encoding='utf-8') as file:
            data_for_model = json.load(file)

            for dt in data_for_model:
                ad = Ads(
                    name=dt['name'],
                    author=dt['author'],
                    price=dt['price'],
                    description=dt['description'],
                    is_published=dt['is_published'].capitalize()
                )

                ad.save()
                print('insert done')

        data_2 = []
        with open('categories.csv', 'r', encoding='utf-8') as c_csv_file:
            reader = csv.reader(c_csv_file, delimiter=',')
            for row in reader:
                data_2.append(row)

        self.upload_data_to_json(data_2, 'categories.json')

        with open('categories.json', 'r', encoding='utf-8') as file_2:
            data_for_model_2 = json.load(file_2)

            for dt in data_for_model_2:
                category = Categories(
                    name=dt['name']
                )

                category.save()
                print('insert done')


command = Command()
command.handle()
