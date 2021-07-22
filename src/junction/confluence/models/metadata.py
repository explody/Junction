"""Construct page metadata based on a page's front matter

"""

from typing import List, Union, Any, Optional, Generic, TypeVar

from junction.util import DotDict
from junction.confluence.models import ContentMetadata


def construct_metadata(front_matter: DotDict) -> ContentMetadata:

    metadata = {
        "properties": {},
    }

    if front_matter.confluence_editor_version == 2:

        appearance = front_matter.get("appearance", "fixed-width")
        if appearance not in ['full-width', 'fixed-width']:
            appearance = 'fixed-width'

        metadata["properties"]["editor"] = {"key": "editor", "value": "v2"}
        metadata["properties"]["content-appearance-draft"] = {
            "key": "content-appearance-draft",
            "value": appearance,
        }
        metadata["properties"]["content-appearance-published"] = {
            "key": "content-appearance-published",
            "value": appearance,
        }

    return ContentMetadata(**metadata)
