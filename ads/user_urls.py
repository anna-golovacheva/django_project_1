from django.urls import path

from ads.views import UserListView, UsersDetailView, UsersCreateView, \
    UsersUpdateView, UsersDeleteView

urlpatterns = [
    path('', UserListView.as_view()),
    path('<int:pk>/', UsersDetailView.as_view()),
    path('create/', UsersCreateView.as_view()),
    path('<int:pk>/update/', UsersUpdateView.as_view()),
    path('<int:pk>/delete/', UsersDeleteView.as_view()),
]