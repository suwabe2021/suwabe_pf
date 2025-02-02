from django.urls import path
from . import views

app_name ="line_bot"
urlpatterns = [
    path('', views.index, name='callback'),
]