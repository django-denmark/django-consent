==============
django-consent
==============

.. image:: https://img.shields.io/pypi/v/django_consent.svg
        :target: https://pypi.python.org/pypi/django_consent

.. image:: https://circleci.com/gh/django-denmark/django-consent/tree/main.svg?style=svg
    :target: https://circleci.com/gh/django-denmark/django-consent/tree/main

*Manages consent for email communication with GDPR in mind*

* An app for Django - ``pip install django-consent-temp`` (hoping to takeover django-consent)
* Free software: GNU General Public License v3


Features
--------

* GDPR-friendly models, supporting deletion and anonymization
* Views for unsubscribing
* Utility functions for generating unsubscribe links
* Utility functions for creating consent
* Form mixins for consent
* Abuse-resistent: Someone cannot mass-unsubscribe or otherwise abuse endpoints.
* Denial of Service: Endpoints do not store for instance infinite amounts of
  opt-outs.

Open questions
--------------

* Can or should consent expire? Currently, we are capturing the creation date of
  a consent, but we are not using expiration dates.

* Would some email addresses qualify as non-individual, and thus require
  different types of consent? For instance, should company/customer email
  addresses be stored in a way so that certain consents become optional?
  Currently, all consent is explicit and stored that way.

* Should django-consent also capture purpose and more generic ways of storing
  private data? Currently, we are only capturing email-related consent.

* Do we want to store consent indefinitely? No. If consent is withdrawn, we
  should delete the entire consent. A person would have to create an entirely
  new consent.

* Should we store op-outs indefinitely? Partly. In django-consent, we do this
  because we want opt-outs to remain in effect. But we store a hash of the email
  such that it we don't keep a record of emails. Experience with Mailchimp and
  similar systems tell us that marketing and other eager types will keep
  re-importing consent and forget to care about previous opt-outs. By storing an
  opt-out, we can ensure to some degree that mistakes made will not result in
  clearly non-consensual communication.


Other considerations: Privacy by Design
---------------------------------------

Your application needs the ability to easily delete and anonymize data. Not just
because of GDPR, but because it's the right thing to do.

No matter the usage of django-consent, you still need to consider this:

* Right to be forgotten: Means that at any time, you should be able to
  **delete** the data of any person. Either by request or because the purpose of
  collecting the data is no longer relevant.

* Anonymize data: When your consent to collect data associated to a person
  expires and if you need to keep a statistical record, the data must be
  completely anonymized. For instance, if they made an order in your shop and
  your stored data about shopping cart activity, you'll have to delete or
  anonymize this data.

In any implementation, you should consider how you associate personally
identifiable information. This can be a name, email, IP address, physical
address and unique combinations (employer + job + department).

In order to design a Django project for privacy, consider the following:

* Right to be forgotten:

  * Deletion should be implemented through deletion of a ``User`` instance. Do
    not relate personally identifiable data in other ways.
  * All model relations to ``User.id`` should use ``on_delete=models.CASCADE``

* Anonymization:

  * When a relation to ``User.id`` has ``null=True`` and is nullified, then
  remaining data in the model should not identify the person. You should design
  your models to only allow null values for ``User`` relations when in fact the
  remaining data in the row and its relations cannot be used to identify the
  person from your data.


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
