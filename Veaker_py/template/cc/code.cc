#include "{{target}}.h"

void
{{target}}(
{% for arg in args %}    {{arg["type"]}} {{arg["name"]}}{% if not loop.last %},{% endif %}
{% endfor %}) {
#pragma HLS INTERFACE ap_ctrl_none port=return
{% for arg in args %}{% if arg["attribute"] in ["publisher", "subscriber"] %}#pragma HLS INTERFACE axis port={{arg["name"]}}
{% elif arg["attribute"] == "wire" %}#pragma HLS INTERFACE ap_none port={{arg["name"]}}
{% endif %}{% endfor %}    
}
