import os
import shutil

from python.common import LANGUAGES, print_confirmation


def make_website() -> None:
    base_path = "books/philosophy_friends"

    for book in os.listdir(base_path):
        book_path = os.path.join(base_path, book)
        if not os.path.isdir(os.path.join(book_path, "INPUT")):
            continue
        for lang in LANGUAGES:
            target_dir = os.path.join(book_path, lang)
            if os.path.isdir(target_dir):
                shutil.copy("books/reader.html", os.path.join(target_dir, "reader.html"))
                print_confirmation(os.path.join(target_dir, "reader.html"))
