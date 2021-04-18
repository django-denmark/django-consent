Consent Types
=============


.. warning::

  This is a WIP (Work-In-Progress). It's to expand upon some of the
  thoughts that have gone into the design thus-far.


Consent has the following basic factors:

.. glossary::

    Consent Source
      The "Source" or the "origin" of consent can be from a direct form input or from an indirect action.

    Consent
      A specfic user consents to something specific expressed in a |Consent Source|

    Direct Consent Source
      A Source can be direct and specific: "Receive a newsletter every month".

    Indirect Consent Source
      A Source can also be indirect: "As a member of an organization, we need to inform you about changes in our statutes, invite you to meetings etc."
      Often these are known as "legitimate interest".


Consent Source examples
-----------------------

A source of consent is a repeatable type of consent. Consider these examples:

* User signs up as a member of a website/organization :term:`Consent Source`
* User signs up for a specific newsletter :term:`Consent`

A direct source can most likely be enabled and disabled directly on the website, while indirect sources are often derived from something else.


Users can manage consent
------------------------

There are very few types of consent that users cannot manage. You can probably
imagine exactly those and then make the rest configurable.


Storing changes to consent
--------------------------

You might be looking for one of the following two types of changes:

* User changes their :term:`Consent` to a specific :term:`Consent Source` - gives or withdraws.
* You change the :term:`Consent Source` - **you cannot do that**.

So the possibilities are actually quite limited. We can log when users give and
withdraw consent to document what has happened.

But under no circumstances should we change anything or add anything to a
Consent Source. We can of course fix a typo. But consent becomes meaningless if
we modify it after it's given.


Refactoring consent
-------------------

If users have given consent and then the Consent is attached to a
:term:`Consent Source` instance, then the source can often be broken down and
replaced by simpler instances of :term:`Direct Consent Source`.
