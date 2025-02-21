import sys
import os
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.core.management import call_command
from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_zen.settings")

User = get_user_model()

@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):

    os.environ["PYTEST_RUNNING"] = "true"
    with django_db_blocker.unblock():
        call_command("migrate")

@pytest.fixture(autouse=True)
def clear_db(django_db_blocker):

    with django_db_blocker.unblock():
        call_command("flush", "--noinput")


@pytest.fixture
def api_client():
    return APIClient()
