# -*- coding: utf-8 -*-

from .models import Counter
from django.contrib import admin


class CounterAdmin(admin.ModelAdmin):

    list_display = [ 'create_datetime', 'date_key', 'hay_accessions', 'hay_refiles', 'non_hay_accessions', 'non_hay_refiles', 'notes' ]
    list_filter = [
        'create_datetime',
        'date_key',
    ]
    ordering = [ '-date_key' ]

    readonly_fields = [ 'create_datetime' ]

    prepopulated_fields = {}

    save_on_top = True

    ## class CounterAdmin()


admin.site.register( Counter, CounterAdmin )
