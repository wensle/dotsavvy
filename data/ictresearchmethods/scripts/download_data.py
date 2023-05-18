import pywikibot
import mwparserfromhell
import json
import os
from config import ICT_RESEARCH_METHODS_DATA_DIR


def wikitext_to_plain_text(wikitext):
    parsed_wikitext = mwparserfromhell.parse(wikitext)

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


def sanitize_filename(filename):
    invalid_characters = ["/", "\\", ":", "*", "?", '"', "<", ">", "|", " "]
    for char in invalid_characters:
        filename = filename.replace(char, "_")
    return filename.lower()


def save_page_data(page_data, output_folder=ICT_RESEARCH_METHODS_DATA_DIR):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    sanitized_title = sanitize_filename(page_data["title"])
    file_path = os.path.join(output_folder, f"{sanitized_title}.json")
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(page_data, json_file, ensure_ascii=False, indent=4)


def main(namespaces):
    site = pywikibot.Site(url="https://ictresearchmethods.nl/api.php")

    for namespace in namespaces:
        allpages = site.allpages(namespace=namespace, content=True)

        for page in allpages:
            page_title = page.title()
            plain_text_content = wikitext_to_plain_text(page.text)
            page_full_url = page.full_url()
            page_categories = [cat.title() for cat in page.categories()]
            backlinks = page.backlinks(
                filter_redirects=False, namespaces=None, total=None, content=False
            )
            embeddedin = page.embeddedin(
                filter_redirects=False, namespaces=None, total=None, content=False
            )
            latest_revision_timestamp = page.latest_revision.timestamp

            page_data = {
                "title": page_title,
                "content": plain_text_content,
                "categories": page_categories,
                "full_url": page_full_url,
                "backlinks": [link.title() for link in backlinks],
                "latest_revision_timestamp": latest_revision_timestamp.isoformat(),
                "embeddedin": [link.title() for link in embeddedin],
            }

            save_page_data(page_data)


if __name__ == "__main__":
    namespaces = [
        0,  # Main
        13,  # Category
    ]
    main(namespaces)
