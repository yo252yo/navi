import os
import shutil
from typing import List, Tuple

from jinja2 import Template

from python.common import LANGUAGES, print_confirmation


def list_books(path: str) -> List[Tuple[str, str]]:
    books = []
    for book in os.listdir(path):
        book_path = os.path.join(path, book)
        if not os.path.isdir(book_path) or not os.path.isdir(os.path.join(book_path, "INPUT")):
            continue
        for lang in LANGUAGES:
            target_dir = os.path.join(book_path, lang)
            if os.path.isdir(target_dir) and os.path.exists(os.path.join(target_dir, "thumbnail.png")):
                books.append((book, lang))
    return sorted(books)

JINJA_VARIABLES = {
    "philsoophy_friends_books": list_books("books/philosophy_friends")
}

def copy_reader_template() -> None:
    for book in os.listdir("books/philosophy_friends"):
        book_path = os.path.join("books/philosophy_friends", book)
        if not os.path.isdir(os.path.join(book_path, "INPUT")):
            continue
        for lang in LANGUAGES:
            target_dir = os.path.join(book_path, lang)
            if os.path.isdir(target_dir):
                shutil.copy("books/reader.template.html", os.path.join(target_dir, "reader.html"))
                print_confirmation(os.path.join(target_dir, "reader.html"))

def handle_template(root, file):
    template_path = os.path.join(root, file)
    output_path = template_path.replace(".template.html", ".html")
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
    template = Template(template_content)
    html_content = template.render(var=JINJA_VARIABLES)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print_confirmation(output_path)

def process_html_templates():
    for root, _, files in os.walk("books"):
        for file in files:
            if file.endswith(".template.html"):
                if file == "reader.template.html":
                    copy_reader_template()
                    continue # We copy this template, we don't compile it.

                handle_template(root, file)


def make_website() -> None:
    process_html_templates()
