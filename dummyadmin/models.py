#!/usr/bin/env python

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models import signals

# From <a href="http://stackoverflow.com/questions/1466827/">http://stackoverflow.com/questions/1466827/</a> --
#
# Prevent interactive question about wanting a superuser created.  (This code
# has to go in this otherwise empty &quot;models&quot; module so that it gets processed by
# the &quot;syncdb&quot; command during database creation.)
signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser')


# Create our own test user automatically.

def create_testuser(app, created_models, verbosity, **kwargs):
  if not settings.DEBUG:
    return
  try:
    auth_models.User.objects.get(username='admin')
  except auth_models.User.DoesNotExist:
    print '*' * 80
    print 'Creating admin user -- login: admin, password: admin'
    print '*' * 80
    assert auth_models.User.objects.create_superuser('admin', 'admin@localhost.localdomain', 'admin')
  else:
    print 'Test user already exists.'

signals.post_syncdb.connect(create_testuser,
    sender=auth_models, dispatch_uid='common.models.create_testuser')

