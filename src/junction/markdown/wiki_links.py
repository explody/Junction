from typing import Tuple, Optional, Any
from markdown import Markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import LinkInlineProcessor
import xml.etree.ElementTree as etree
import html
import re

V2_URL = "{}/wiki/pages/createpage.action?spaceKey={}&title={}&linkCreation=true"


class WikiLinkExtension(Extension):
    """Markdown extension for rendering links prefixed with '&' as links to other pages
    in Confluence.  Links in Confluence are based on page titles e.g. `&[Display Text](Target Page Name)`
    """

    def __init__(self, **kwargs):
        self.config = {
            "confluence_version": ["0", "Confluence link version to use"],
            "confluence_space": ["", "Confluence space key to use in links"],
            "confluence_url": ["", "Base URL of this confluence instance"],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        md.inlinePatterns.add("wiki-link", WikiLinkPattern(md, ext=self), "<reference")


class WikiLinkPattern(LinkInlineProcessor):
    def __init__(self, *args: Any, **kwargs: Any):
        self.ext = kwargs.pop("ext")
        super().__init__(r"\&\[", *args, **kwargs)

    def handleMatch(
        self, m: re.Match, data: str
    ) -> Tuple[Optional[etree.Element], Optional[int], Optional[int]]:
        text, index, handled = self.getText(data, m.end(0))

        if not handled:
            return None, None, None

        href, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        # Check if the "link" has a space key prepended
        space_match = re.match("(?:([A-Z]{2,5}):)?(.+)", href)
        page = space_match.group(2)

        confluence_url = self.ext.getConfig("confluence_url")
        confluence_space = self.ext.getConfig("confluence_space")
        confluence_version = self.ext.getConfig("confluence_version")

        if space_match.group(1):
            space = space_match.group(1)
        else:
            space = confluence_space

        if int(confluence_version) == 2:
            link = etree.Element("a")
            link.text = text
            link.set(
                "href",
                V2_URL.format(confluence_url, space, html.escape(page, quote=False)),
            )
        else:
            element_props = {
                "ri:content-title": html.escape(page, quote=False),
                "ri:version-at-save": "1",
            }
            if space:
                element_props["ri:space-key"] = space

            link = etree.Element("ac:link", {"ac:card-appearance": "inline"})
            etree.SubElement(
                link,
                "ri:page",
                element_props,
            )
            etree.SubElement(
                link, "ac:plain-text-link-body"
            ).text = "<![CDATA[{}]]>".format(text)

        return link, m.start(0), index


def makeExtension(**kwargs: Any) -> WikiLinkExtension:
    return WikiLinkExtension(**kwargs)
