# -*- coding: utf-8 -*-

import datetime, logging

from . import settings_app
from django.test import TestCase
# from django.test import SimpleTestCase as TestCase    ## TestCase requires db, so if you're not using a db, and want tests, try this


log = logging.getLogger(__name__)
TestCase.maxDiff = None


class ClientTest( TestCase ):
    """ Checks urls. """

    def test_good_post(self):
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
