"""
WSGI config for clamood_gym project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clamood_gym.settings')

application = get_wsgi_application() 