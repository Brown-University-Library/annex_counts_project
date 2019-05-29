# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from annex_counts_app import views


admin.autodiscover()


urlpatterns = [

    # -------
    # main
    # -------

    # url( r'^admin/login/', RedirectView.as_view(pattern_name='login_url') ),

    # url( r'^admin/', admin.site.urls ),  # eg host/project_x/admin/

    url( r'^stats/$', views.stats, name='stats_url' ),

    url( r'^updater/$', views.updater, name='updater_url' ),

    # -------
    # helpers
    # -------

    url( r'^info/$', views.info, name='info_url' ),

    url( r'^error_check/$', views.error_check, name='error_check_url' ),

    # url( r'^login/$', views.login, name='login_url' ),

    url( r'^$', RedirectView.as_view(pattern_name='stats_url') ),

    ]
