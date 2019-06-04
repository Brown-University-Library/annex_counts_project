# -*- coding: utf-8 -*-

""" Manages db query & response. """

import datetime, json, logging, pprint, random

from annex_counts_app.models import Counter
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet  # for type-hinting
from django.http.request import QueryDict  # for type-hinting


log = logging.getLogger(__name__)


class StatsBuilder:
    """ Handles stats-api queries. """

    def __init__( self ):
        self.date_start = None  # set by check_params()
        self.date_end = None  # set by check_params()
        self.output_dct = {
            'request': {
                'timestamp': '',
                'url': '',
                },
            'response': {
                'count_total': '',
                'count_detail': { 'Hay_Accessions': 0, 'Hay_Refiles': 0, 'Non-Hay_Accessions': 0, 'Non-Hay_Refiles': 0 },
                'period_begin_timestamp': '',
                'period_end_timestamp': '',
                'elapsed_time': ''
                }
            }
        self.output_jsn = ''

    def check_params( self, get_params: QueryDict, scheme: str, host: str, stopwatch_start: datetime.datetime ) -> bool:
        """ Checks parameters; returns boolean.
            Called by views.stats() """
        if 'start_date' not in get_params or 'end_date' not in get_params:  # not valid
            self._handle_bad_params( scheme, host, get_params, stopwatch_start )
            return False
        else:  # valid
            self.date_start = '%s 00:00:00' % get_params['start_date']
            self.date_end = '%s 23:59:59' % get_params['end_date']
            return True

    def run_query( self ) -> QuerySet:
        """ Queries db.
            Called by views.stats_api() """
        records = Counter.objects.filter(
            create_datetime__gte=self.date_start).filter(create_datetime__lte=self.date_end)
        log.debug( f'number of records, ```{len(records)}```' )
        return records

    def process_results( self, records: QuerySet ) -> dict:
        """ Extracts desired data from resultset.
            Called by views.stats() """
        for record in records:
            self.output_dct['response']['count_detail']['Hay_Accessions'] += record.hay_accessions
            self.output_dct['response']['count_detail']['Hay_Refiles'] += record.hay_refiles
            self.output_dct['response']['count_detail']['Non-Hay_Accessions'] += record.non_hay_accessions
            self.output_dct['response']['count_detail']['Non-Hay_Refiles'] += record.non_hay_refiles
        log.debug( f'self.output_dct, ```{pprint.pformat(self.output_dct)}```' )
        return self.output_dct

    def build_response( self, data: dict, get_params: QueryDict, scheme: str, host: str, stopwatch_start: datetime.datetime ) -> str:
        """ Builds json response.
            Called by views.() """
        self.output_dct['request']['timestamp'] = str( stopwatch_start )
        self.output_dct['request']['url'] = '%s://%s%s%s' % ( scheme, host, reverse('stats_url'), self._prep_querystring(get_params) )
        self.output_dct['response']['elapsed_time'] = str( datetime.datetime.now() - stopwatch_start )
        self.output_dct['response']['count_total'] = 0
        for key in [ 'Hay_Accessions', 'Hay_Refiles', 'Non-Hay_Accessions', 'Non-Hay_Refiles' ]:
            self.output_dct['response']['count_total'] += self.output_dct['response']['count_detail'][key]
        self.output_dct['response']['period_begin_timestamp'] = self.date_start
        self.output_dct['response']['period_end_timestamp'] = self.date_end
        log.debug( f'self.output_dct, ```{pprint.pformat(self.output_dct)}```' )
        jsn = json.dumps( self.output_dct, sort_keys=True, indent=2 )
        return jsn

    def _handle_bad_params( self, scheme: str, host: str, get_params: QueryDict, stopwatch_start: datetime.datetime ) -> None:
        """ Prepares bad-parameters data and json.
            Json saved to instance attribute; not returned.
            Called by check_params() """
        self.output_dct['request']['timestamp'] = str( stopwatch_start )
        self.output_dct['request']['url'] = '%s://%s%s%s' % ( scheme, host, reverse('stats_url'), self._prep_querystring(get_params) )
        self.output_dct['response']['status'] = '400 / Bad Request'
        self.output_dct['response']['message'] = 'example url: %s://%s%s?start_date=2019-01-01&end_date=2019-01-31' % ( scheme, host, reverse('stats_url') )
        self.output_dct['response']['elapsed_time'] = str( datetime.datetime.now() - stopwatch_start )
        for key in [ 'count_detail', 'count_total', 'period_begin_timestamp', 'period_end_timestamp' ]:
            del( self.output_dct['response'][key] )
        log.debug( f'self.output_dct after bad-param-handling, ```{pprint.pformat(self.output_dct)}```' )
        self.output_jsn = json.dumps( self.output_dct, sort_keys=True, indent=2 )
        return

    def _prep_querystring( self, get_params: QueryDict ) -> str:
        """ Makes querystring from params.
            Called by _handle_bad_params() """
        querystring: str
        if get_params:
            querystring = '?%s' % get_params.urlencode()  # get_params is a django QueryDict object, which has a urlencode() method! yay!
        else:
            querystring = ''
        log.debug( f'querystring, ```{querystring}```' )
        return querystring

    # def generate_dummy_output( self, get_params, scheme, host, stopwatch_start ):
    #     """ Temp output generator.
    #         Called by views.stats() """
    #     self.output_dct['request']['timestamp'] = str( stopwatch_start )
    #     self.output_dct['request']['url'] = '%s://%s%s%s' % ( scheme, host, reverse('stats_url'), self._prep_querystring(get_params) )
    #     for key in [ 'Hay_Accessions', 'Hay_Refiles', 'Non-Hay_Accessions', 'Non-Hay_Refiles' ]:
    #         self.output_dct['response']['count_detail'][key] = random.randint( 1000, 9999 )
    #     self.output_dct['response']['elapsed_time'] = str( datetime.datetime.now() - stopwatch_start )
    #     self.output_dct['response']['count_total'] = 0
    #     for key in [ 'Hay_Accessions', 'Hay_Refiles', 'Non-Hay_Accessions', 'Non-Hay_Refiles' ]:
    #         self.output_dct['response']['count_total'] += self.output_dct['response']['count_detail'][key]
    #     self.output_dct['response']['period_begin_timestamp'] = self.date_start
    #     self.output_dct['response']['period_end_timestamp'] = self.date_end
    #     log.debug( 'jdct, ```%s```' % pprint.pformat(self.output_dct) )
    #     jsn = json.dumps( self.output_dct, sort_keys=True, indent=2 )
    #     return jsn

    # end class StatsBuilder
