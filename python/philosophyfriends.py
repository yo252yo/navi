import os

from common import print_confirmation
from pdf_maker import (BLACK_PAGE, compress_pdf, mage_pages_from_large_image,
                       make_page_from_image, make_pages_for_cover)
from PIL import Image
from pypdf import PdfWriter
from writers import (write_author, write_centered_text,
                     write_legalese_bottomleft, write_onomatopae_text,
                     write_subtitle, write_summary, write_title)

IMAGE_DIMENSIONS = (2048, 1024)

def generate_legalese_page(path, version):
    legal_path = f"{path}/INPUT/{version}_legal.txt"

    if os.path.exists(legal_path):
        with open(legal_path, "r", encoding="utf-8") as file:
            text = file.read()
    else:
        print(f"!! NO LEGALESE FOR {legal_path} — USING EMPTY STRING.")
        text = ""

    width, height = IMAGE_DIMENSIONS
    black = Image.new("RGBA", (width // 2, height), (0, 0, 0, 255))
    write_legalese_bottomleft(black, text)
    black.save(f"{path}/{version}/tmp/legal_page.png")

    print_confirmation(f"{path}/{version}/tmp/legal_page.png")

    make_page_from_image(f"{path}/{version}/tmp/legal_page.png", f"{path}/{version}/tmp/legal_page.pdf")

def generate_wide_page(path, version, image_name, text, flipped=False):
    image = Image.open(f"{path}/raw_images/" + image_name).convert("RGBA")
    width, height = image.size

    overlay = Image.new("RGBA", (width // 2, height), (255, 255, 255, int(255 * 0.75)))

    offset = width // 2
    if flipped:
        offset = 0
    image.paste(overlay, (offset, 0), overlay)

    write_centered_text(image, text, flipped)
    image.save(f"{path}/{version}/wide_pages/{image_name}")
    print_confirmation(f"{path}/{version}/wide_pages/{image_name}")

def parse_onomatopae(path, version):
    instructions = []
    fullpath = f"{path}/INPUT/{version}_onomatopae.txt"
    if not os.path.exists(fullpath):
        return instructions

    with open(fullpath, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            page_part, pos_part, angle_part, color_part, size_part, text_part = line.split(":", 5)
            x, y = map(int, pos_part.split(","))
            instructions.append({
                "page": page_part.strip(),
                "x": x,
                "y": y,
                "angle": float(angle_part),
                "color": color_part.strip(),
                "size": int(size_part.strip()),
                "text": text_part.strip(),
            })
    return instructions

def resize_wide_image(path, image_name):
    image = Image.open(f"{path}/INPUT/{image_name}").convert("RGBA")
    resized = image.resize(IMAGE_DIMENSIONS, Image.Resampling.LANCZOS)

    resized.save(f"{path}/raw_images/{image_name}")
    print_confirmation(f"{path}/raw_images/{image_name}")

def make_inside(path, version, file):
    onomatopae = parse_onomatopae(path, version)
    pages_count = 0
    for line in file:
        pages_count += 1
        index = pages_count - 1
        image_name = "p" + str(pages_count)
        resize_wide_image(path, f"{image_name}.png")
        generate_wide_page(path, version, f"{image_name}.png", line, index % 2 == 1)
        write_onomatopae_text(f"{path}/{version}/wide_pages/{image_name}.png", onomatopae, index % 2 == 1)
        mage_pages_from_large_image(f"{path}/{version}/wide_pages/{image_name}.png", f"{path}/{version}/split_pages/{image_name}_left.pdf", f"{path}/{version}/split_pages/{image_name}_right.pdf")

    written_pages = pages_count

    pdf = PdfWriter()
    pages = 1
    pdf.append(f"{path}/{version}/tmp/legal_page.pdf")
    for i in range(1, written_pages + 1): # +1 because range excludes upper limit
        pdf.append(f"{path}/{version}/split_pages/p" + str(i) + "_left.pdf")
        pdf.append(f"{path}/{version}/split_pages/p" + str(i) + "_right.pdf")
        pages += 2

    while ((pages % 4 > 0) or (pages < 24)):
        pdf.append(BLACK_PAGE)
        pages += 1

    pdf.write(f"{path}/{version}/inside.pdf")
    pdf.close()
    print_confirmation(f"{path}/{version}/inside.pdf")

def make_cover(path, version):
    resize_wide_image(path, "cover.png")
    image = Image.open(f"{path}/raw_images/cover.png").convert("RGBA")

    with open(f"{path}/INPUT/{version}_cover.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    extra = {}
    for line in lines[2:]:
        if "=" in line:
            key, value = line.strip().split("=", 1)
            extra[key.strip()] = value.strip()

    subtitle = "La philosophie avec tous mes amis!"
    intro = "POUR LES PLUS GRANDS:\\n-\\n"
    author = "Georges Jeanres"
    if version == "EN":
        subtitle = "My philosopher friends"
        intro = "FOR GROWN UPS:\\n-\\n"

    write_title(image, lines[0].strip(), int(extra.get("title_y", 50)), extra.get("title_color", "#FFFFFF"), extra.get("title_border_color", "#000000"), int(extra.get("title_size", "120")))
    write_subtitle(image, subtitle, int(extra.get("subtitle_y", 150)), extra.get("subtitle_color", "#000000"))
    write_author(image, author, int(extra.get("author_y", 90)), extra.get("author_color", "#000000"))
    write_summary(image, intro + lines[1].strip(), extra.get("summary_color", "#FFFFFF"))

    image.save(f"{path}/{version}/wide_pages/cover.png")
    print_confirmation(f"{path}/{version}/wide_pages/cover.png")
    make_pages_for_cover(f"{path}/{version}")

def merge_covers(path, version):
    pdf = PdfWriter()
    pdf.append(f"{path}/{version}/tmp/front_cover.pdf")
    pdf.append(f"{path}/{version}/inside.pdf")
    pdf.append(f"{path}/{version}/tmp/back_cover.pdf")
    pdf.write(f"{path}/{version}/ebook.pdf")
    pdf.close()
    print_confirmation(f"{path}/{version}/ebook.pdf")

def make_folders(path, version):
    os.makedirs(f"{path}/raw_images", exist_ok=True)
    os.makedirs(f"{path}/{version}", exist_ok=True)
    os.makedirs(f"{path}/{version}/wide_pages", exist_ok=True)
    os.makedirs(f"{path}/{version}/tmp", exist_ok=True)
    os.makedirs(f"{path}/{version}/split_pages", exist_ok=True)

def make_pdf(book, version):
    print(f"### GENERATING {book} / {version}")
    path = f"books/philosophy_friends/{book}"

    make_folders(path, version)
    generate_legalese_page(path, version)

    with open(f"{path}/INPUT/{version}.txt", "r", encoding="utf-8") as file:
        make_inside(path, version, file)

    make_cover(path, version)
    merge_covers(path, version)
    compress_pdf(f"{path}/{version}/ebook.pdf")

def make_books():
    base_path = "books/philosophy_friends"
    pairs = []

    # Collect all valid (book, lang) pairs
    for book in os.listdir(base_path):
        book_input = os.path.join(base_path, book, "INPUT")
        if not os.path.isdir(book_input):
            continue
        for lang in ["FR", "EN"]:
            lang_file = os.path.join(book_input, f"{lang}.txt")
            if os.path.exists(lang_file):
                pairs.append((book, lang))

    # Show menu
    print("Do you want to regenerate:")
    for i, (book, lang) in enumerate(pairs, 1):
        print(f"{i}. {book}/{lang}")
    choice = input("Enter number to regenerate only that one, or press Enter for all: ").strip()

    # Execute
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(pairs):
            book, lang = pairs[idx]
            make_pdf(book, lang)
            return

    # Default: regenerate all
    for book, lang in pairs:
        make_pdf(book, lang)
