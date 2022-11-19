import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View, defaults
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, \
    DeleteView

from ads.models import Categories, Ads, Users, Locations
from djangoProject_1.settings import TOTAL_ON_PAGE


def ads_start_view(request):
    return JsonResponse({"status": "ok"}, status=200)


# Views for Categories
class CatListView(ListView):
    model = Categories

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by('name')

        paginator = Paginator(self.object_list, 5)
        page_num = request.GET.get('page')
        page_objects = paginator.get_page(page_num)

        categories_list = []
        for category in page_objects:
            categories_list.append({
                'id': category.id,
                'name': category.name
            })

        return JsonResponse(categories_list, safe=False, status=200)


class CatDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        cat_object = Categories.objects.get(pk=kwargs['pk'])

        return JsonResponse({
                'id': cat_object.id,
                'name': cat_object.name
            },
            status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CatCreateView(CreateView):
    model = Categories

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        cat = Categories(
            name=data['name']
        )
        cat.save()

        return JsonResponse({"id": cat.id, "name": cat.name}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CatUpdateView(UpdateView):
    model = Categories
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        self.object.name = data['name']

        self.object.save()

        return JsonResponse({"id": self.object.id, "name": self.object.name}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CatDeleteView(DeleteView):
    model = Categories
    success_url = 'cat/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=200)


# Views for Ads
class AdsListView(ListView):
    model = Ads

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.select_related('category').select_related('author').all().order_by('-price')

        total_ads = self.object_list.count()
        paginator = Paginator(self.object_list, 5)
        page_num = request.GET.get('page')
        page_objects = paginator.get_page(page_num)

        ads_list = []
        for ads in page_objects:
            ads_list.append(
                {
                    'id': ads.id,
                    'name': ads.name,
                    'author': ads.author.username,
                    'price': ads.price,
                    'description': ads.description,
                    'is_published': ads.is_published,
                    'image': ads.image.url if ads.image else None,
                    'category': ads.category.name,
                    })

        return JsonResponse({'items': ads_list, 'total': total_ads,
                    'num_pages': TOTAL_ON_PAGE}, safe=False, status=200)


class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):

        ads_object = Ads.objects.select_related('category').select_related('author').get(pk=kwargs['pk'])

        return JsonResponse({
                'id': ads_object.id,
                'name': ads_object.name,
                'author': ads_object.author.username,
                'price': ads_object.price,
                'description': ads_object.description,
                'is_published': ads_object.is_published,
                'image': ads_object.image.url if ads_object.image else None,
                'category': ads_object.category.name
            },
            status=200
        )


@method_decorator(csrf_exempt, name="dispatch")
class AdsCreateView(CreateView):
    model = Ads
    fields = ['id', 'name', 'author', 'price', 'description', 'is_published',
              'category']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        author_obj, _ = Users.objects.get_or_create(username=data['author'])

        category_obj, _ = Categories.objects.get_or_create(name=data['category'])

        ad = Ads(
            name=data['name'],
            price=data['price'],
            description=data['description'],
            is_published=data['is_published'],
            author=author_obj,
            category=category_obj
        )

        ad.save()

        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            'author': ad.author.username,
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'image': ad.image.url if ad.image else None,
            'category': ad.category.name
        },
            status=200
        )


@method_decorator(csrf_exempt, name='dispatch')
class AdsUpdateView(UpdateView):
    model = Ads
    fields = ['id', 'name', 'author', 'price', 'description', 'is_published',
              'category']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        author_obj, _ = Users.objects.get_or_create(username=data['author'])


        self.object.name = data['name']
        self.object.author = author_obj
        self.object.price = data['price']
        self.object.description = data['description']
        self.object.is_published = data['is_published']

        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author': self.object.author.username,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'image': self.object.image.url if self.object.image else None,
            'category': self.object.category.name
        },
            status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsDeleteView(DeleteView):
    model = Ads
    success_url = '/ads/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageUpdateView(UpdateView):
    model = Ads
    fields = ['id', 'name', 'author', 'price', 'description', 'is_published', 'image', 'category']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        self.object = self.get_object()
        self.object.image = request.FILES['image']
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author': self.object.author.username,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'category': self.object.category.name,
            'image': self.object.image.url if self.object.image else None
            }, status=200)


# View for Users
class UserListView(ListView):
    model = Users

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.prefetch_related('locations').annotate(published_ads=Count('ads')).filter(ads__is_published=True).order_by('username')
        total_users = self.object_list.count()
        paginator = Paginator(self.object_list, 5)
        page_num = request.GET.get('page')
        page_objects = paginator.get_page(page_num)

        users_list = []
        for users in page_objects:
            users_list.append(
                {
                    'id': users.id,
                    'first_name': users.first_name,
                    'last_name': users.last_name,
                    'username': users.username,
                    'password': users.password,
                    'role': users.role,
                    'age': users.age,
                    'locations': list(map(str, users.locations.all())),
                    'published_ads': users.published_ads
                    })

        return JsonResponse({'items': users_list, 'total': total_users,
                    'num_pages': TOTAL_ON_PAGE}, safe=False, status=200)


class UsersDetailView(DetailView):
    model = Users

    def get(self, request, *args, **kwargs):

        user_object = Users.objects.prefetch_related('locations').get(pk=kwargs['pk'])

        return JsonResponse({
                'id': user_object.id,
                'first_name': user_object.first_name,
                'last_name': user_object.last_name,
                'username': user_object.username,
                'password': user_object.password,
                'role': user_object.role,
                'age': user_object.age,
                'locations': list(map(str, user_object.locations.all()))
            },
            status=200
        )


@method_decorator(csrf_exempt, name="dispatch")
class UsersCreateView(CreateView):
    model = Users
    fields = ['id', 'first_name', 'last_name', 'username', 'password', 'role',
              'age', 'locations']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        locations = Locations.objects.filter(name__in=data['locations'])
        user = Users(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            password=data['password'],
            role=data['role'],
            age=data['age'],
        )

        user.save()
        user.locations.add(*locations)

        return JsonResponse({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'password': user.password,
            'role': user.role,
            'age': user.age,
            'locations': list(map(str, user.locations.all()))
        },
            status=200
        )


@method_decorator(csrf_exempt, name='dispatch')
class UsersUpdateView(UpdateView):
    model = Users
    fields = ['id', 'first_name', 'last_name', 'username', 'password', 'role',
              'age', 'locations']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        locations = Locations.objects.filter(name__in=data['locations'])

        self.object.first_name = data['first_name']
        self.object.last_name = data['last_name']
        self.object.username = data['username']
        self.object.password = data['password']
        self.object.role = data['role']
        self.object.age = data['age']
        self.object.locations.add(*locations)
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'username': self.object.username,
            'password': self.object.password,
            'role': self.object.role,
            'age': self.object.age,
            'locations': list(map(str, self.object.locations.all()))
        },
            status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UsersDeleteView(DeleteView):
    model = Users
    success_url = '/users/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=200)