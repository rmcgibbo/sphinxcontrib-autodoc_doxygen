autodoxysummary
===============

Input
-----

Using ``autodoxysummary``, you can generate class-level documentation automatically. ::

  .. autodoxysummary::
     :toctree: generated/

     OpenMM::NonbondedForce
     OpenMM::VerletIntegrator
     OpenMM::CustomIntegrator


This will generate a table to display, but also use the templating engine to generate class-level
documentation for each of the classes which will be added to the toctree. You can also customize the
layout of the generated pages by passing your own template.


------


Output
------

.. autodoxysummary::
   :toctree: generated/

   ~OpenMM::NonbondedForce
   ~OpenMM::VerletIntegrator
   ~OpenMM::CustomIntegrator
   ~OpenMM::System
