from django.urls import path, re_path
from .views import effective_rate, home, fd_effective_rate, fdrate_banks_list, sdrate_banks_info
from rest_framework import routers

urlpatterns =[

    path("", home, name="home"),
    path("effective_rate/", effective_rate, name="effective_rate"),
    path("fdrate_interest/", fd_effective_rate, name="fdrate_interest"),
    path("fdrate_all/", fdrate_banks_list, name="fdrate_all"),
    path("sdrate_all/", sdrate_banks_info, name="sdrate_all"),
]
