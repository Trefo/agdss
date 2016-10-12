from __future__ import absolute_import

# This will make sure the apps bel;ow are always imported when
# Django starts so that shared_task will use these apps.
from .celery import app as celery_app  # noqa