#include QMK_KEYBOARD_H

{% for layer in layers %}
#define {{layer}} {{loop.index0}}
{% endfor %}

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
{% for layer, keys in zip(layers, keys_list) %}
    [{{layer}}] = LAYOUT({{keys}}){{"," if not loop.last}}
{% endfor %}
};
