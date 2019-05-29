# -*- coding: utf-8 -*-

import datetime, logging, pprint

from annex_counts_app import settings_app
from annex_counts_app.models import Counter


log = logging.getLogger(__name__)


def check_validity( request ) -> bool:
    """ Checks request.
        Called by: views.updater() """
    check_val = False
    required_keys = [ 'auth_key', 'date', 'hay_accessions', 'hay_refiles', 'non_hay_accessions', 'non_hay_refiles' ]
    try:
        if sorted( request.POST.keys() ) == required_keys:
            log.debug( 'keys present' )
            values_check = 'init'
            for key in required_keys:
                if len( request.POST[key] ) == 0:
                    values_check = 'fail'
                    break
            if values_check == 'init':
                log.debug( 'keys have values' )
                if request.POST['auth_key'] == settings_app.API_AUTH_KEY:
                    log.debug( 'auth_key good' )
                    check_val = True
    except Exception as e:
        log.error( f'validation failed, exception, ```{e}```' )
    log.debug( f'check_val, `{check_val}`' )
    return check_val


def prep_counts( request ) -> dict:
    """ Extracts data from params.
        Called by views.updater() """
    extracted_data = {
        'date': datetime.datetime.strptime( request.POST['date'], '%Y-%m-%d' ).date(),
        'hay_accessions': int( request.POST['hay_accessions'] ),
        'hay_refiles': int( request.POST['hay_refiles'] ),
        'non_hay_accessions': int( request.POST['non_hay_accessions'] ),
        'non_hay_refiles': int( request.POST['non_hay_refiles'] )
    }
    log.debug( f'extracted_data, ```{pprint.pformat(extracted_data)}```' )
    return extracted_data


def update_db( data: dict ) -> None:
    """ Updates data for given date.
        Called by views.updater() """
    try:
        record = Counter.objects.get( date_key=data['date'] )
    except Exception as e:
        log.debug( f"record for date ```{data['date']}``` not found, message is ```{e}```; will create counter-record" )
        record = Counter(
            date_key = data['date'],
            hay_accessions = data['hay_accessions'],
            hay_refiles = data['hay_refiles'],
            non_hay_accessions = data['non_hay_accessions'],
            non_hay_refiles = data['non_hay_refiles'],
        )
    record.save()
    log.debug( f'record created, ```{pprint.pformat(record.__dict__)}```' )
    return
