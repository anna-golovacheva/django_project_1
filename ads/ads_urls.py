from django.urls import path

from ads.views import AdsListView, AdsDetailView, AdsCreateView, AdsUpdateView, \
    AdsDeleteView, AdImageUpdateView

urlpatterns = [
    path('', AdsListView.as_view()),
    path('<int:pk>/', AdsDetailView.as_view()),
    path('create/', AdsCreateView.as_view()),
    path('<int:pk>/update/', AdsUpdateView.as_view()),
    path('<int:pk>/delete/', AdsDeleteView.as_view()),
    path('<int:pk>/upload_image/', AdImageUpdateView.as_view()),
]