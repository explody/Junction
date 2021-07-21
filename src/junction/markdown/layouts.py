import logging

from typing import Union, Optional

LAYOUTS = {
    'centered': '''
            <ac:structured-macro ac:name="column" ac:schema-version="1">
                <ac:parameter ac:name="width">10%</ac:parameter>
                <ac:rich-text-body></ac:rich-text-body>
            </ac:structured-macro>
            <ac:structured-macro ac:name="column" ac:schema-version="1">
                <ac:parameter ac:name="width">80%</ac:parameter>
                <ac:parameter ac:name="max-width">800px</ac:parameter>
                <ac:rich-text-body>
                    {content}
                </ac:rich-text-body>
            </ac:structured-macro>
            <ac:structured-macro ac:name="column" ac:schema-version="1">
                <ac:parameter ac:name="width">10%</ac:parameter>
                <ac:rich-text-body></ac:rich-text-body>
            </ac:structured-macro>''',
    'wide': '''<ac:structured-macro ac:name="column" ac:schema-version="1">
                <ac:parameter ac:name="width">100%</ac:parameter>
                <ac:rich-text-body>{content}</ac:rich-text-body>
            </ac:structured-macro>''',

}


def apply_layout(content: str, front_matter: dict) -> str:

    layout = front_matter.get('layout')

    if layout not in LAYOUTS:
        return content

    return LAYOUTS[layout].format(content=content)