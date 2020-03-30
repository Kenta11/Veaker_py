#ifndef {{target.upper()}}_H
#define {{target.upper()}}_H

{% for header in headers %}#include "{{header}}"
{% endfor %}
void
{{target}}(
{% for arg in args %}    {{arg["type"]}} {{arg["name"]}}{% if not loop.last %},{% endif %}
{% endfor %});

#endif // {{target.upper()}}_H
