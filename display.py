import json
from pathlib import Path

from beautifultable import BeautifulTable


def format_key(key):
    if len(key) > 6:
        return "\n".join([key[:2], key[2:]])
    return key + "\n"


def to_table(keys_list):
    table = BeautifulTable()
    table.column_widths = [8] * len(keys_list[0])
    for keys in keys_list:
        table.append_row([format_key(key) for key in keys])
    return table


def display(left, right):
    l = left.get_string(recalculate_width=False).split("\n")
    r = right.get_string(recalculate_width=False).split("\n")
    rows = []
    for ls, rs in zip(l, r):
        rows.append(ls + "    " + rs)
    return "\n".join(rows)


if __name__ == "__main__":
    path = Path("layers.json")
    layers_dict = json.load(path.open("r"))
    for layer in layers_dict.keys():
        left, right = layers_dict[layer]["left"], layers_dict[layer]["right"]
        print(f"## {layer}")
        print("```")
        print(display(to_table(left), to_table(right)))
        print("```")
