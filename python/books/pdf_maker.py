import math
import subprocess
from typing import cast

from PIL import Image
from reportlab.pdfgen import canvas

from python.common import print_confirmation

BLEED_IN=0.125
PAGE_WIDTH_IN=8.25
PAGE_HEIGHT_IN=8.25
DPI = 300

BLEED=math.ceil(BLEED_IN * DPI)+1
PAGE_WIDTH=math.ceil((PAGE_WIDTH_IN + BLEED_IN) * DPI)+1
PAGE_HEIGHT=math.ceil((PAGE_HEIGHT_IN + 2 * BLEED_IN) * DPI)+1

BLACK_PAGE = "python/resources/black_8.25_8.25.pdf"

def save_pdf(image: Image.Image, output_pdf: str, width: int = PAGE_WIDTH) -> None:
    conversion = 72 / DPI
    c = canvas.Canvas(output_pdf, pagesize=(math.ceil(width * conversion), math.ceil(PAGE_HEIGHT * conversion)))  # Convert to points
    image = image.convert("RGB")
    image_path = output_pdf.replace(".pdf", ".png")
    image.save(image_path, "PNG", quality=100)
    c.drawImage(image_path, 0, 0, math.ceil(width * conversion), math.ceil(PAGE_HEIGHT * conversion))
    c.showPage()
    c.save()

def mage_pages_from_large_image(input_png: str, output_left_pdf: str, output_right_pdf: str) -> None:
    # Open the image
    img = cast(Image.Image, Image.open(input_png))
    total_width = 2 * PAGE_WIDTH
    img = img.resize((total_width, PAGE_HEIGHT), Image.Resampling.LANCZOS)

    # Crop left and right pages with bleed
    left_page = img.crop((0, 0, PAGE_WIDTH, PAGE_HEIGHT))
    right_page = img.crop((PAGE_WIDTH, 0, total_width, PAGE_HEIGHT))

    save_pdf(left_page, output_left_pdf)
    save_pdf(right_page, output_right_pdf)
    print_confirmation(output_left_pdf)
    print_confirmation(output_right_pdf)

def make_pages_for_cover(path: str) -> None:
    input_png = f"{path}/wide_pages/cover.png"
    full_cover_pdf = f"{path}/cover.pdf"
    back_cover_pdf = f"{path}/tmp/back_cover.pdf"
    front_cover_pdf = f"{path}/tmp/front_cover.pdf"

    # Open the image
    img = cast(Image.Image, Image.open(input_png))
    total_width = 2 * PAGE_WIDTH
    img = img.resize((total_width, PAGE_HEIGHT), Image.Resampling.LANCZOS)

    # Crop left and right pages with bleed
    left_page = img.crop((0, 0, PAGE_WIDTH, PAGE_HEIGHT))
    right_page = img.crop((PAGE_WIDTH, 0, total_width, PAGE_HEIGHT))

    save_pdf(img, full_cover_pdf, width=int(2.01 * PAGE_WIDTH))  # 0.01 for the edge
    save_pdf(left_page, back_cover_pdf)
    save_pdf(right_page, front_cover_pdf)

    # Create thumbnail from front cover image
    thumbnail = right_page.resize((256, 256), Image.Resampling.LANCZOS)
    thumbnail_path = f"{path}/thumbnail.png"
    thumbnail.save(thumbnail_path)

    print_confirmation(full_cover_pdf)
    print_confirmation(back_cover_pdf)
    print_confirmation(front_cover_pdf)
    print_confirmation(thumbnail_path)

def make_page_from_image(input_png: str, output_pdf: str) -> None:
    img = cast(Image.Image, Image.open(input_png))
    img = img.resize((PAGE_WIDTH, PAGE_HEIGHT), Image.Resampling.LANCZOS)
    save_pdf(img, output_pdf)
    print_confirmation(output_pdf)

def compress_pdf(path: str) -> None:
    newpath = path.replace(".pdf", "_compressed.pdf")
    subprocess.run([
        "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",  # or /screen, /printer
        "-dNOPAUSE", "-dQUIET", "-dBATCH",
        f"-sOutputFile={newpath}", path
    ], check=True)
    print_confirmation(newpath)
