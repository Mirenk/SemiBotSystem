from django.urls import path
from . import views

app_name = 'matching'

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('<int:pk>/join/', views.Join.as_view(), name='join'),
    path('<int:pk>/cancel/', views.Cancel.as_view(), name='cancel'),
]