Consent Types
=============


.. warning::

  This is a WIP (Work-In-Progress). It's to expand upon some of the
  thoughts that have gone into the design thus-far.


Consent has the following basic factors:

.. glossary::

    Policy
      All your data is subject of a privacy policy. As much as possible, make this short and sweet and in the user's best interest. NOT to cover your own ass. You want to have 1 singular policy and avoid updates to the policy. Don't be like AirBnB.

    Purpose
      When you collect data, you do it with a purpose. Some purpose is obvious and may not even require explicit consent (legitimate interest). And other purposes might be very critical for the user to understand. Make sure to always note the purpose, as it's likely part of your legal obligation. Data should not be collected, much less shared, without having defined and shared the purpose with your user.

    Consent Agreement
      For every purpose, you need an Agreement to collect data. If you share the data, this is even more important (mandatory).
      An Agreement is generic, it's the same Agreement that you present to every user that you need consent from.

    Consent Record
      Consent is obtained through a Consent Record. This records that the user has given their consent to a specific Agreement. The user may withdraw the consent again, in which case the Consent Record would be stored on top of a previous Consent Record to explicitly display the opt-out action.

    Legitimate interest
      You might have heard of legitimate interest. There are many things that you're allowed to do without obtaining explicit consent. But it's a good idea to prepare a Consent Agreement anyways and store a Consent Record to express that this was indeed the case.


Consent Source examples
-----------------------

.. * User signs up as a member of a website/organization :term:`Consent Source`
.. * User signs up for a specific newsletter :term:`Consent`


Users can manage consent
------------------------

There are very few types of consent that users cannot manage. You can probably
imagine exactly those and then make the rest configurable.


Storing changes to consent
--------------------------

You might be looking for one of the following two types of changes:
