# -*- coding: utf-8 -*-

import json, os


README_URL = os.environ['ANX_COUNTS__README_URL']

API_AUTH_KEY = os.environ['ANX_COUNTS__API_AUTH_KEY']


## auth
# SUPER_USERS = json.loads( os.environ['ANX_COUNTS__UPER_USERS_JSON'] )
# STAFF_USERS = json.loads( os.environ['ANX_COUNTS__STAFF_USERS_JSON'] )  # users permitted access to admin
# STAFF_GROUP = os.environ['ANX_COUNTS__STAFF_GROUP']  # not grouper-group; rather, name of django-admin group for permissions
# TEST_META_DCT = json.loads( os.environ['ANX_COUNTS__TEST_META_DCT_JSON'] )
# POST_LOGIN_ADMIN_REVERSE_URL = os.environ['ANX_COUNTS__POST_LOGIN_ADMIN_REVERSE_URL']  # tricky; for a direct-view of a model, the string would be in the form of: `admin:APP-NAME_MODEL-NAME_changelist`
