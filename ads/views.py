import json

from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View, defaults
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Categories, Ads


def ads_start(request):
    return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CatView(View):
    def get(self, request):
        categories = Categories.objects.all()

        response = []
        for category in categories:
            response.append({
                'id': category.id,
                'name': category.name,
            })

        return JsonResponse(response, safe=False, status=200)

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)
        categories = Categories()
        categories.name = category_data['name']
        categories.save()
        return JsonResponse({
            'id': categories.id,
            'name': categories.name
        }, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdsView(View):
    def get(self, request):
        ads = Ads.objects.all()

        response = []
        for ad in ads:
            response.append({
                'id': ad.id,
                'name': ad.name,
                'author': ad.author,
                'price': ad.price,
                'description': ad.description,
                'is_published': ad.is_published
            })

        return JsonResponse(response, safe=False, status=200)

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        ads = Ads()
        ads.name = ad_data['name']
        ads.author = ad_data['author']
        ads.price = ad_data['price']
        ads.description = ad_data['description']
        ads.is_published = ad_data['is_published']
        ads.save()
        return JsonResponse({
            'id': ads.id,
            'name': ads.name,
            'author': ads.author,
            'price': ads.price,
            'description': ads.description,
            'is_published': ads.is_published
        }, status=200)


class CatDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        try:
            category = self.get_object()
        except Http404:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            'id': category.id,
            'name': category.name
        }, status=200)


class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Http404:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            'author': ad.author,
            'price': ad.price,
            'description': ad.description
        }, status=200)






