import json
import os
from pathlib import Path
from typing import Any, Generator, Optional, Sequence, Union

import mwparserfromhell
import pywikibot
from mwparserfromhell.wikicode import Wikicode
from pywikibot import BaseSite, Page

from config import ICT_RESEARCH_METHODS_BASE_DIR

# Constants
_OUTPUT_FOLDER: Path = ICT_RESEARCH_METHODS_BASE_DIR / "raw_data"
_ICTRESEARCHMETHODS_API_URL = "https://ictresearchmethods.nl/api.php"
_WIKI_NAMESPACES: set[int] = {
    0,  # Main
    13,  # Category
}


def wikitext_to_plain_text(wikitext) -> str:
    parsed_wikitext: Wikicode = mwparserfromhell.parse(wikitext)
    if not isinstance(parsed_wikitext, Wikicode):
        raise ValueError(
            "Expected parsed_wikitext to be of type Wikicode, but got "
            f"{type(parsed_wikitext)}."
        )

    # Remove file/image links and "Category:" prefixes
    for node in parsed_wikitext.ifilter():
        if isinstance(node, mwparserfromhell.nodes.tag.Tag):
            if node.tag.lower() in ("gallery", "imagemap", "img", "file"):
                parsed_wikitext.remove(node)
        elif isinstance(node, mwparserfromhell.nodes.wikilink.Wikilink):
            if node.title.lower().startswith("category:"):
                parsed_wikitext.remove(node)
        elif isinstance(node, mwparserfromhell.nodes.template.Template):
            if node.name.lower().startswith("category:"):
                parsed_wikitext.remove(node)
        elif isinstance(node, mwparserfromhell.nodes.text.Text):
            if "250px|right" in node.value:
                parsed_wikitext.remove(node)

    return parsed_wikitext.strip_code()


def sanitize_filename(filename: str) -> str:
    invalid_characters: list[str] = ["/", "\\", ":", "*", "?", '"', "<", ">", "|", " "]
    for char in invalid_characters:
        filename = filename.replace(char, "_")
    return filename.lower()


def save_as_json_file(
    page_data: dict[str, str | list[str]],
    output_folder: Optional[Union[str, Path]] = None,
) -> None:
    output_folder = output_folder or _OUTPUT_FOLDER
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    sanitized_title: str = sanitize_filename(page_data["title"])
    file_path: str = os.path.join(output_folder, f"{sanitized_title}.json")
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(page_data, json_file, ensure_ascii=False, indent=4)


def main(namespaces: Optional[Sequence[int]] = None, url: Optional[str] = None) -> None:
    namespaces = namespaces or _WIKI_NAMESPACES
    url = url or _ICTRESEARCHMETHODS_API_URL

    site: BaseSite = pywikibot.Site(url=url)

    for namespace in namespaces:
        allpages: Generator[Page] = site.allpages(namespace=namespace, content=True)

        for page in allpages:
            page_title: str = page.title()
            plain_text_content: str = wikitext_to_plain_text(page.text)
            page_full_url: str = str(page.full_url())
            page_categories: list[str] = [cat.title() for cat in page.categories()]
            backlinks: Any = page.backlinks(
                filter_redirects=False, namespaces=None, total=None, content=False
            )
            embeddedin: Any = page.embeddedin(
                filter_redirects=False, namespaces=None, total=None, content=False
            )
            latest_revision_timestamp = str(page.latest_revision.timestamp.isoformat())

            page_data: dict[str, Union[str, list[str]]] = {
                "title": page_title,
                "content": plain_text_content,
                "categories": page_categories,
                "full_url": page_full_url,
                "backlinks": [str(link.title()) for link in backlinks],
                "latest_revision_timestamp": latest_revision_timestamp,
                "embeddedin": [str(link.title()) for link in embeddedin],
            }

            save_as_json_file(page_data)


if __name__ == "__main__":
    main()
