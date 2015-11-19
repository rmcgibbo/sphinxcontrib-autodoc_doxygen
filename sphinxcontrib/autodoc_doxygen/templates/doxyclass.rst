{{ fullname }}
{{ underline }}

.. autodoxyclass:: {{ objname }}

   {% if methods %}
   .. rubric:: Methods

   .. autodoxysummary::
   {% for item in methods %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}

