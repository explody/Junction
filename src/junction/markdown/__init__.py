import logging

from typing import Union, Optional

from markdown import Markdown
from markdown.extensions.sane_lists import SaneListExtension
from markdown.extensions.tables import TableExtension
from mdx_superscript import SuperscriptExtension
from mdx_subscript import SubscriptExtension
from mdx_emdash import EmDashExtension
from mdx_urlize import UrlizeExtension

from junction.confluence import Confluence
from junction.markdown.layouts import apply_layout
from junction.markdown.checklists import ChecklistExtension
from junction.markdown.codeblocks import CodeBlockExtension
from junction.markdown.status import StatusExtension
from junction.markdown.toc import TableOfContentsExtension
from junction.markdown.children import ChildrenExtension
from junction.markdown.info_panels import InfoPanelExtension
from junction.markdown.wiki_links import WikiLinkExtension


logger = logging.getLogger(__name__)


def markdown_to_storage(
    api_cient: Confluence,
    text: Optional[Union[str, bytes]],
    front_matter: Optional[dict] = {},
) -> str:

    junctionMarkdown = Markdown(
        extensions=[
            SaneListExtension(),
            SuperscriptExtension(),
            SubscriptExtension(),
            EmDashExtension(),
            # UrlizeExtension(),
            ChecklistExtension(),
            CodeBlockExtension(),
            StatusExtension(),
            TableOfContentsExtension(),
            ChildrenExtension(),
            InfoPanelExtension(),
            WikiLinkExtension(
                confluence_version=front_matter["confluence_editor_version"],
                confluence_space=api_cient.space_key,
                confluence_url=api_cient.confluence_url,
            ),
            TableExtension(),
        ],
    )

    if text is None:
        return ""
    elif isinstance(text, bytes):
        text = text.decode("utf-8", "ignore")

    logger.debug("Compiling markdown to Confluence storage format: %s", text)
    result = junctionMarkdown.convert(text)
    junctionMarkdown.reset()
    logger.debug("Applying content to layout: %s", text)

    if front_matter.get("layout"):
        logger.debug("Applying page layout: %s", front_matter["layout"])
        result = apply_layout(result, front_matter)

    with open("out.html", "w") as outfile:
        outfile.write(result)

    return result
