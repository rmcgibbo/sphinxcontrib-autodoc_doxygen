=============
autodoxyclass
=============

Input
=====

The ``autodoxyclass`` directive will insert the docstring of the class: ::

    .. autodoxyclass:: OpenMM::Force

which produces something like ::

  .. :cpp:class:: OpenMM::Force

     Force's documentation.

If you want to automatically document members, there is a members option: ::

    .. autodoxyclass:: OpenMM::Force
       :members:

which will automatically insert documentation for each of the members.

You can also add content to the directive which will appear after the class docstring
but before the methods, like a summary table. ::

    .. autodoxyclass:: OpenMM::Force
       :members:

       .. rubric:: Methods

       .. autodoxysummary::

         ~OpenMM::Force::getForceGroup
         ~OpenMM::Force::setForceGroup
         ~OpenMM::Force::usesPeriodicBoundaryConditions


------

Output
======


::

  .. autodoxyclass:: OpenMM::Platform

.. autodoxyclass:: OpenMM::Platform

-----

::

  .. autodoxyclass:: OpenMM::Integrator
     :members:

.. autodoxyclass:: OpenMM::Integrator
   :members:

------

::

  .. autodoxyclass:: OpenMM::Force
     :members:

     .. rubric:: Methods

     .. autodoxysummary::

       ~OpenMM::Force::getForceGroup
       ~OpenMM::Force::setForceGroup
       ~OpenMM::Force::usesPeriodicBoundaryConditions

.. autodoxyclass:: OpenMM::Force
   :members:

   .. rubric:: Methods

   .. autodoxysummary::

     ~OpenMM::Force::getForceGroup
     ~OpenMM::Force::setForceGroup
     ~OpenMM::Force::usesPeriodicBoundaryConditions