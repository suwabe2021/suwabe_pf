from django.contrib import admin
from django.urls import include, path
from django.urls.conf import include

urlpatterns = [
    path('line_bot/', include('line_bot.urls')),
    #path('admin/', admin.site.urls), #使わないのでコメントアウト
    path('login/', include("account.urls")),
]

from django.conf.urls import handler404
from account.views import custom_404_view

#404はlogin/へ飛ばす
handler404 = custom_404_view