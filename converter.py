import json
from itertools import chain
from pathlib import Path

import click
import jinja2

env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)
env.globals.update(zip=zip)
KEYS = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") + [
    "BSPC",
    "CAPS",
    "DEL",
    "END",
    "ENT",
    "F1",
    "F10",
    "F11",
    "F12",
    "F2",
    "F3",
    "F4",
    "F5",
    "F6",
    "F7",
    "F8",
    "F9",
    "HOME",
    "LALT",
    "LCTL",
    "LGUI",
    "LSFT",
    "PGDN",
    "PGUP",
    "RALT",
    "RCTL",
    "RGUI",
    "RSFT",
    "SPC",
    "TAB",
]
KEY2CODE = {
    "  ": "KC_NO",
    "__": "KC_TRNS",
    "-": "KC_MINS",
    ",": "KC_COMM",
    ";": "KC_SCLN",
    "!": "KC_EXLM",
    ".": "KC_DOT",
    "'": "KC_QUOT",
    "(": "KC_LPRN",
    ")": "KC_RPRN",
    "[": "KC_LBRC",
    "]": "KC_RBRC",
    "@": "KC_AT",
    "*": "KC_ASTR",
    "/": "KC_SLSH",
    "\\": "KC_BSLS",
    "&": "KC_AMPR",
    "#": "KC_HASH",
    "%": "KC_PERC",
    "`": "KC_GRV",
    "^": "KC_CIRC",
    "←": "KC_LEFT",
    "→": "KC_RGHT",
    "↑": "KC_UP",
    "↓": "KC_DOWN",
    "=": "KC_EQL",
    "$": "KC_DLR",
    "かな": "KANA",
    "英数": "EISU",
}
KEY2CODE.update({key: f"KC_{key}" for key in KEYS})


def key_to_code(key):
    ret = KEY2CODE.get(key.upper())
    if ret:
        return ret
    return key


def merge_left_and_right(layers_dict):
    layer_to_keys = {}
    for layer in layers_dict.keys():
        left, right = layers_dict[layer]["left"], layers_dict[layer]["right"]
        keys = [lkc + rkc for (lkc, rkc) in zip(left, right)]
        layer_to_keys[layer] = chain.from_iterable(keys)
    return layer_to_keys


def get_keycodes_list(layer_to_keys):
    return [", ".join(map(key_to_code, keys)) for keys in layer_to_keys.values()]


def main(json_path, template_path, output_path):
    layers_dict = json.load(Path(json_path).open("r"))
    layer_to_keys = merge_left_and_right(layers_dict)
    with open(template_path, "r") as f:
        template = env.from_string(f.read())
    keymap_text = template.render(
        layers=layer_to_keys.keys(), keys_list=get_keycodes_list(layer_to_keys)
    )
    with open(output_path, "w") as f:
        f.write(keymap_text)


@click.command()
@click.argument("dir_path")
@click.option("--template", default="keymap.tmpl.c")
def cmd(dir_path, template):
    main(
        Path(dir_path).joinpath("layers.json"),
        template,
        Path(dir_path).joinpath("keymap.c"),
    )


if __name__ == "__main__":
    cmd()
