import logging
import os
import pathlib


def apply_layout(content: str, front_matter: dict) -> str:

    layouts_dir = os.path.join(pathlib.Path(__file__).parent.resolve(), "layouts")
    layout = front_matter.get('layout', None)
    layout_file = None

    if layout:
        layout_file = os.path.join(layouts_dir, "{}.html".format(layout))

    if not os.path.exists(layout_file):
        return content

    with open(layout_file, "r") as layout_fh:
        template = layout_fh.read()

    return template.format(content=content)