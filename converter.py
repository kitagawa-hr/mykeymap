import json
from itertools import chain
from pathlib import Path

import jinja2

env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)
env.globals.update(zip=zip)


def key_to_code(key):
    KEY2CODE = {
        "  ": "KC_NO",
        "__": "KC_TRNS",
        ";": "KC_SCLN",
        "=": "KC_EQL",
        "-": "KC_MINS",
        "'": "KC_QUOT",
        ".": "KC_DOT",
        ",": "KC_COMM",
        "(": "KC_LPRN",
        ")": "KC_RPRN",
        "[": "KC_LBRC",
        "]": "KC_RBRC",
        "`": "KC_GRV",
        "!": "KC_EXLM",
        "@": "KC_AT",
        "#": "KC_HASH",
        "$": "KC_DLR",
        "%": "KC_PERC",
        "^": "KC_CIRC",
        "&": "KC_AMPR",
        "*": "KC_ASTR",
        "ENTER": "KC_ENT",
        "/": "KC_SLSH",
        "\\": "KC_BSLS",
        "←": "KC_LEFT",
        "↓": "KC_DOWN",
        "↑": "KC_UP",
        "→": "KC_RGHT",
    }
    ret = KEY2CODE.get(key.upper())
    if ret:
        return ret
    elif key.startswith(("MO", "TO", "KC_")):
        return key
    return "KC_" + key


def merge_left_and_right(layers_dict):
    layer_to_keys = {}
    for layer in layers_dict.keys():
        left, right = layers_dict[layer]["left"], layers_dict[layer]["right"]
        keys = [lkc + rkc for (lkc, rkc) in zip(left, right)]
        layer_to_keys[layer] = chain.from_iterable(keys)
    return layer_to_keys


def get_keycodes_list(layer_to_keys):
    return [", ".join(map(key_to_code, keys)) for keys in layer_to_keys.values()]


def main(json_path, template_path, keymap_path):
    layers_dict = json.load(Path(json_path).open("r"))
    layer_to_keys = merge_left_and_right(layers_dict)
    with open(template_path, "r") as f:
        template = env.from_string(f.read())
    keymap_text = template.render(
        layers=layer_to_keys.keys(), keys_list=get_keycodes_list(layer_to_keys)
    )
    with open(keymap_path, "w") as f:
        f.write(keymap_text)


if __name__ == "__main__":
    main("layers.json", "keymap.tmpl.c", "keymap.c")
