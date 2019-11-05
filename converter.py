import json
from pathlib import Path
from itertools import chain


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
        "#": "KC_HASH}",
        "$": "KC_DLR",
        "%": "KC_PERC",
        "^": "CIRC",
        "&": "KC_AMPR",
        "*": "KC_ASTR",
        "ENTER": "KC_ENT",
        "/": "KC_SLSH",
        "\\": "KC_BSLS",
    }
    ret = KEY2CODE.get(key.upper())
    if ret:
        return ret
    elif key.startswith(("MO", "TO", "KC_")):
        return key
    return "KC_" + key


def json2keys(layers_dict):
    layer_to_keys = {}
    for layer in layers_dict.keys():
        left, right = layers_dict[layer]["left"], layers_dict[layer]["right"]
        keys = [lkc + rkc for (lkc, rkc) in zip(left, right)]
        layer_to_keys[layer] = chain.from_iterable(keys)
    return layer_to_keys


def create_keymap_c(layer_to_keys):
    INCLUDE = "#include QMK_KEYBOARD_H\n"
    DEFINES_FORMAT = "#define {layer} {index}"
    BODY_START = "\nconst uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {"
    BODY_FORMAT = "    [{layer}] = LAYOUT({keycodes})"
    BODY_EMD = "};"
    lines = [INCLUDE]
    defines = []
    body_contents = []
    index = 0
    for layer, keys in layer_to_keys.items():
        defines.append(DEFINES_FORMAT.format(layer=layer, index=index))
        keycodes = [key_to_code(key) for key in keys]
        body_contents.append(
            BODY_FORMAT.format(layer=layer, keycodes=", ".join(keycodes))
        )
        index += 1
    lines.extend(defines)
    lines.append(BODY_START)
    lines.append(",\n".join(body_contents))
    lines.append(BODY_EMD)
    return "\n".join(lines)


def main(json_path, dest):
    path = Path(json_path)
    layers_dict = json.load(path.open("r"))
    layer_to_keys = json2keys(layers_dict)
    keymap_text = create_keymap_c(layer_to_keys)
    with open(dest, "w") as f:
        f.write(keymap_text)


if __name__ == "__main__":
    main("layers.json", "keymap.c")
