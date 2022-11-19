import csv
import json

from django.core.management.base import BaseCommand
from ads.models import Ads, Categories, Locations, Users


class Command(BaseCommand):
    models_dict = {
        Locations: ['name', 'lat', 'lng'],
        Categories: ['name'],
        Users: ['first_name', 'last_name', 'username', 'password', 'role', 'age', 'locations'],
        Ads: ['name', 'author', 'price', 'description', 'is_published', 'image', 'category'],
    }

    def read_csv(self, csv_file):
        data = []
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                data.append(row)
        return data

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
        location_data = self.read_csv('location.csv')
        self.upload_data_to_json(location_data, 'location.json')

        with open('location.json', 'r', encoding='utf-8') as file:
            data_for_model = json.load(file)

            for dt in data_for_model:
                loc = Locations(
                    name=dt['name'],
                    lat=dt['lat'],
                    lng=dt['lng']
                )

                loc.save()
                print('insert loc done')

        category_data = self.read_csv('category.csv')
        self.upload_data_to_json(category_data, 'category.json')

        with open('category.json', 'r', encoding='utf-8') as file:
            data_for_model = json.load(file)

            for dt in data_for_model:
                cat = Categories(
                    name=dt['name']
                )

                cat.save()
                print('insert cat done')

        user_data = self.read_csv('user.csv')
        self.upload_data_to_json(user_data, 'user.json')

        with open('user.json', 'r', encoding='utf-8') as file:
            data_for_model = json.load(file)

            for dt in data_for_model:
                location = Locations.objects.filter(id=int(dt['location_id']))
                user = Users(
                    first_name=dt['first_name'],
                    last_name=dt['last_name'],
                    username=dt['username'],
                    password=dt['password'],
                    role=dt['role'],
                    age=dt['age']
                )

                user.save()
                user.locations.add(*location)
                print('insert user done')

        ad_data = self.read_csv('ad.csv')
        self.upload_data_to_json(ad_data, 'ad.json')

        with open('ad.json', 'r', encoding='utf-8') as file:
            data_for_model = json.load(file)

            for dt in data_for_model:
                author = Users.objects.get(id=int(dt['author_id']))
                category = Categories.objects.get(id=int(dt['category_id']))
                ad = Ads(
                    name=dt['name'],
                    author=author,
                    price=dt['price'],
                    description=dt['description'],
                    is_published=bool(dt['is_published']),
                    image=dt['image'],
                    category=category
                )

                ad.save()
                print('insert ad done')
