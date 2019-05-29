# -*- coding: utf-8 -*-

import datetime, logging, os, pathlib, pprint, sys
import django

logging.basicConfig(
    # filename=LOG_PATH,
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s', datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)
log.info( 'log started' )


SOURCE_DIR_PATH = os.environ['ANX_COUNTS__SOURCE_DIR_PATH']


def manage_update():
    """ Manages processing.
        Called by runner(); triggered by cron job. """
    yesterday = datetime.date.today() - datetime.timedelta( days=1 )
    files_list = find_files( yesterday )
    1/0


def find_files( date ):
    """ Returns full paths of files created on or after given date.
        Called by runner(); triggered by cron job.
        Reference: <https://stackoverflow.com/a/539024> """
    entries = os.listdir( SOURCE_DIR_PATH )
    log.debug( 'entries, ```%s```' % pprint.pformat(entries) )
    2/0
    entries = ( os.path.join(SOURCE_DIR_PATH, fn) for fn in os.listdir(SOURCE_DIR_PATH) )
    log.debug( 'entries, ```%s```' % pprint.pformat(entries) )
    entries = ((os.stat(path), path) for path in entries)

    # leave only regular files, insert creation date
    entries = ((stat[ST_CTIME], path)
               for stat, path in entries if S_ISREG(stat[ST_MODE]))


if __name__ == '__main__':
    manage_update()
