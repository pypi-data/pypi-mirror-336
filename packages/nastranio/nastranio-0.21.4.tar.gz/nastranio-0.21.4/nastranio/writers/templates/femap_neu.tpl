{% if com %}
$COM ==== automatically created by NASTRANIO ====
$COM ====     N.Cordier, numeric GmbH    ===={%endif%}
   -1
   100
{{ database_title|default('<NULL>') }}
{{ neutral_version }},
   -1
{% if layers %}
   -1
   413
{{ layers }}
   -1
{% endif %}
{% if groups %}
   -1
   408
{{ groups }}
   -1
{% endif %}
{% if points %}
   -1
   570
{{ points}}
   -1
{% endif %}
{% if curves %}
   -1
   571
{{ curves}}
   -1
{% endif %}
{% if text %}
   -1
   475
{{ text }}
   -1
{% endif %}
{% if referenced_groups %}
   -1
   1008
{{ referenced_groups }}
   -1
{% endif %}
