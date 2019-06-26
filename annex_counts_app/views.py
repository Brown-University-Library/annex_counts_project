# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint
from typing import Tuple

# from annex_counts_app.lib.shib_auth import shib_login  # decorator
from . import settings_app
from annex_counts_app.lib import updater as update_helper
from annex_counts_app.lib import view_info_helper
from annex_counts_app.lib.stats import StatsBuilder
from annex_counts_app.lib.updater import Validator
from django.conf import settings as project_settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet  # just for type-hinting
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


log = logging.getLogger(__name__)


def stats( request ):
    """ Prepares stats for given dates; returns json. """
    log.debug( f'request.__dict__, ```{request.__dict__}```' )
    rq_now = datetime.datetime.now()
    stats_builder = StatsBuilder()
    if stats_builder.check_params( request.GET, request.scheme, request.META['HTTP_HOST'], rq_now ) == False:
        return HttpResponseBadRequest( stats_builder.output_jsn, content_type=u'application/javascript; charset=utf-8' )
    records: QuerySet = stats_builder.run_query()
    data: dict = stats_builder.process_results( records )
    jsn: str = stats_builder.build_response( data, request.GET, request.scheme, request.META['HTTP_HOST'], rq_now )
    return HttpResponse( jsn, content_type='application/javascript; charset=utf-8' )


def updater( request ):
    """ Updates stats db. """
    log.debug( f'request.POST, ```{pprint.pformat(request.POST)}```' )
    validator = Validator()
    if validator.check_validity( request ) is False:
        return HttpResponseBadRequest( '400 / Bad Request' )
    data: dict = update_helper.prep_counts( request )
    update_helper.update_db( data )
    return HttpResponse( '200 / OK' )


def replacer( request ):
    """ Replaces existing record, if found, with incoming data. """
    log.debug( f'request.POST, ```{pprint.pformat(request.POST)}```' )
    validator = Validator()
    if validator.check_validity( request ) is False:
        return HttpResponseBadRequest( '400 / Bad Request' )

    return HttpResponse( 'implementation coming' )

    data: dict = update_helper.prep_counts( request )
    update_helper.replace_data( data )
    return HttpResponse( '200 / OK' )


# -------
# helpers
# -------


def info( request ):
    """ Returns basic data including branch & commit. """
    # log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
    rq_now = datetime.datetime.now()
    commit = view_info_helper.get_commit()
    branch = view_info_helper.get_branch()
    info_txt = commit.replace( 'commit', branch )
    resp_now = datetime.datetime.now()
    taken = resp_now - rq_now
    context_dct = view_info_helper.make_context( request, rq_now, info_txt, taken )
    output = json.dumps( context_dct, sort_keys=True, indent=2 )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


def error_check( request ):
    """ For an easy way to check that admins receive error-emails (in development).
        To view error-emails in runserver-development:
        - run, in another terminal window: `python -m smtpd -n -c DebuggingServer localhost:1026`,
        - (or substitue your own settings for localhost:1026)
    """
    if project_settings.DEBUG == True:
        1/0
    else:
        return HttpResponseNotFound( '<div>404 / Not Found</div>' )


# @shib_login
# def login( request ):
#     """ Handles authNZ, & redirects to admin.
#         Called by click on login or admin link. """
#     next_url = request.GET.get( 'next', None )
#     if not next_url:
#         redirect_url = reverse( settings_app.POST_LOGIN_ADMIN_REVERSE_URL )
#     else:
#         redirect_url = request.GET['next']  # will often be same page
#     log.debug( 'redirect_url, ```%s```' % redirect_url )
#     return HttpResponseRedirect( redirect_url )
