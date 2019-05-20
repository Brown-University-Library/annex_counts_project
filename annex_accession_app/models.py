# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint
from django.conf import settings as project_settings
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect


log = logging.getLogger(__name__)


class Counter(models.Model):
    create_datetime = models.DateTimeField(auto_now_add=True, null=True)
    date_key = models.DateField(unique=True)
    hay_accessions = models.IntegerField()
    hay_refiles = models.IntegerField()
    non_hay_accessions = models.IntegerField()
    non_hay_refiles = models.IntegerField()
    notes = models.TextField(null=True)
