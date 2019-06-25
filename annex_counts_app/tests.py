# -*- coding: utf-8 -*-

import datetime, logging

from . import settings_app
from annex_counts_app.models import Counter
from django.test import TestCase
# from django.test import SimpleTestCase as TestCase    ## TestCase requires db, so if you're not using a db, and want tests, try this


log = logging.getLogger(__name__)
TestCase.maxDiff = None


class ClientTest( TestCase ):
    """ Checks urls. """

    def test_good_post_w_no_existing_data(self):
        """ Checks happy-path handling. """
        params = {
            'auth_key': settings_app.API_AUTH_KEY,
            'date': str( datetime.date.today() ),
            'hay_accessions': '1',
            'hay_refiles': '2',
            'non_hay_accessions': '3',
            'non_hay_refiles': '4'
        }
        response = self.client.post( '/updater/', params )
        self.assertEqual( 200, response.status_code )
        ##
        record = Counter.objects.get( date_key=params['date'] )
        self.assertEqual( record.non_hay_accessions, 3 )

    def test_good_post_WITH_existing_data(self):
        """ Checks happy-path handling. """
        today_str = str( datetime.date.today() )
        params_A = {
            'auth_key': settings_app.API_AUTH_KEY,
            'date': today_str,
            'hay_accessions': '1',
            'hay_refiles': '2',
            'non_hay_accessions': '3',
            'non_hay_refiles': '4'
        }
        response = self.client.post( '/updater/', params_A )
        self.assertEqual( 200, response.status_code )
        ##
        params_B = {
            'auth_key': settings_app.API_AUTH_KEY,
            'date': today_str,
            'hay_accessions': '2',
            'hay_refiles': '3',
            'non_hay_accessions': '4',
            'non_hay_refiles': '5'
        }
        response = self.client.post( '/updater/', params_B )
        self.assertEqual( 200, response.status_code )
        ##
        record = Counter.objects.get( date_key=params_B['date'] )
        self.assertEqual( record.non_hay_accessions, 7 )

    ## end class ClientTest()


class RootUrlTest( TestCase ):
    """ Checks root urls. """

    def test_root_url_no_slash(self):
        """ Checks '/root_url'. """
        response = self.client.get( '' )  # project root part of url is assumed
        self.assertEqual( 302, response.status_code )  # permanent redirect
        redirect_url = response._headers['location'][1]
        self.assertEqual(  '/stats/', redirect_url )

    def test_root_url_slash(self):
        """ Checks '/root_url/'. """
        response = self.client.get( '/' )  # project root part of url is assumed
        self.assertEqual( 302, response.status_code )  # permanent redirect
        redirect_url = response._headers['location'][1]
        self.assertEqual(  '/stats/', redirect_url )

    # end class RootUrlTest()
