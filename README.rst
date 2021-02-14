==============
django-consent
==============

.. image:: https://img.shields.io/pypi/v/django_consent.svg
        :target: https://pypi.python.org/pypi/django_consent


.. image:: https://circleci.com/gh/django-denmark/django-consent/tree/main.svg?style=svg
    :target: https://circleci.com/gh/django-denmark/django-consent/tree/main

Manages consent for communication with GDPR in mind

* An app for Django - ``pip install django-consent-temp`` (hoping to takeover django-consent)
* Free software: GNU General Public License v3

Features
--------

* GDPR-friendly models, supporting deletion and anonymization
* Views for unsubscribing
* Utility functions for generating unsubscribe links
* Utility functions for creating consent
* Form mixins for consent


Usage
-----

.. code-block:: console

  # Enable your Python environment (example)
  workon myproject
  # Installation
  pip install django-consent-temp

Now go to your Django project's settings and add:

.. code-block:: python
  INSTALLED_APPS = [
      # ...
      'django_consent',
  ]


To use unsubscribe views, add this to your project's ``urls.py``:

.. code-block:: python

  urlpatterns = [
      # ...
      path('consent/', include('django_consent.urls')),
  ]


Development
-----------

To install an editable version into a project, activate your project's
virtualenv and run this:

.. code-block:: python

  # Installs an editable version of django-consent
  pip install -e .
  # Installs an editable version of django-consent's development requirements
  pip install -e '.[develop]'
  # Enables pre-commit
  pre-commit install
