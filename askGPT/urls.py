from django.contrib import admin
from django.urls import include, path
from django.urls.conf import include

urlpatterns = [
    path('line_bot/', include('line_bot.urls')),
    path('admin/', admin.site.urls),
    path('login/', include("account.urls")),
]