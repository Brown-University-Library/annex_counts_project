# -*- coding: utf-8 -*-

import datetime, logging, pprint

from annex_counts_app import settings_app
from annex_counts_app.models import Counter


log = logging.getLogger(__name__)


class Validator:

    def __init__( self ):
        self.check_val = False
        self.required_keys = [ 'auth_key', 'date', 'hay_accessions', 'hay_refiles', 'non_hay_accessions', 'non_hay_refiles' ]

    def check_validity( self, request ) -> bool:
        """ Manages checks.
            Called by views.updater() """
        try:
            if self.check_keys( list(request.POST.keys()) ) == True:
                if self.check_key_lengths( request.POST ) == True:
                    if request.POST['auth_key'] == settings_app.API_AUTH_KEY:
                        self.check_val = True
        except Exception as e:
            log.error( f'validation failed, exception, ```{e}```' )
        log.debug( f'self.check_val, `{self.check_val}`' )
        return self.check_val

    def check_keys( self, keys: list ) -> bool:
        """ Checks keys.
            Called by check_validity() """
        check = False
        log.debug( f'keys, ```{keys}```' )
        if sorted( keys ) == self.required_keys:
            check = True
        log.debug( f'check, `{check}`' )
        return check

    def check_key_lengths( self, req_post: dict ) -> bool:
        """ Checks for empty keys.
            Called by check_validity() """
        def_check: bool = False
        loop_check: str = 'init'
        key: str
        for key in self.required_keys:
            if len( req_post[key] ) == 0:
                loop_check = 'fail'
                break
        if loop_check == 'init':
            def_check = True
        log.debug( f'def_check, `{def_check}`' )
        return def_check

    ## end class Validator


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
        log.debug( 'record already exists; will be updated' )
    except Exception as e:
        log.debug( f"record for date ```{data['date']}``` not found, message is ```{e}```; will create record" )
        record = Counter()
    if record.date_key:  # means it already existed and was populated
        record.notes = f'{record.notes}\n---\nupdated existing counts with new data: ```{pprint.pformat(data)}```'
    else:
        record.date_key = data['date']
    record.hay_accessions += data['hay_accessions']
    record.hay_refiles += data['hay_refiles']
    record.non_hay_accessions += data['non_hay_accessions']
    record.non_hay_refiles += data['non_hay_refiles']
    record.save()
    return


# def update_db( data: dict ) -> None:
#     """ Updates data for given date.
#         Called by views.updater() """
#     try:
#         record = Counter.objects.get( date_key=data['date'] )
#         log.debug( 'record already exists; not created or updated' )
#     except Exception as e:
#         log.debug( f"record for date ```{data['date']}``` not found, message is ```{e}```; will create counter-record" )
#         record = Counter(
#             date_key = data['date'],
#             hay_accessions = data['hay_accessions'],
#             hay_refiles = data['hay_refiles'],
#             non_hay_accessions = data['non_hay_accessions'],
#             non_hay_refiles = data['non_hay_refiles'],
#         )
#         record.save()
#         log.debug( f'record created, ```{pprint.pformat(record.__dict__)}```' )
#     return
