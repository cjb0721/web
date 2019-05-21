# -*- coding: utf-8 -*-
# db info
import os
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webmonitors.settings")

DBNAME = settings.BASE_DIR + "/db.sqlite3"

PROJECT_PATH = settings.BASE_DIR
RRD_PATH = PROJECT_PATH + "/rrd"

# print (DBNAME)
# print (RRD_PATH)

