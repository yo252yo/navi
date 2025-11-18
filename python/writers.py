import re

from common import hex_to_rgba, invert_color
from PIL import Image, ImageDraw, ImageFilter, ImageFont


def write_legalese_bottomleft(image, text):
    width, height = image.size
    font = ImageFont.truetype("python/resources/Engine-Regular.otf", 18)  # Smaller font for legal text
    draw = ImageDraw.Draw(image)

    # Calculate text size using textbbox
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]

    # Set the position at the bottom-left corner with a margin
    margin = 100
    text_x = margin  # Left-aligned, with a margin
    text_y = height - text_height - margin  # Position it near the bottom with a margin

    # Draw the text in white at the calculated position
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))  # White color

def write_centered_text(image, text, flipped=False):
    width, height = image.size
    font = ImageFont.truetype("python/resources/Engine-Regular.otf", 100)
    draw = ImageDraw.Draw(image)
    margin = 100
    max_width = width // 2 - 2 * margin
    line_height = font.getmetrics()[0] + font.getmetrics()[1]

    # Split by literal newlines first
    paragraphs = text.split('\\n')
    lines = []

    # Word-wrap each paragraph
    for paragraph in paragraphs:
        words = paragraph.split()
        line = ""
        for word in words:
            test_line = line + (" " if line else "") + word
            test_width, _ = draw.textbbox((0, 0), test_line, font=font)[2:]
            if test_width <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)

    if len(lines) > 6:
        font = ImageFont.truetype("python/resources/Engine-Regular.otf", 80)
        line_height = font.getmetrics()[0] + font.getmetrics()[1]

    # Calculate total height for centering
    total_height = sum(draw.textbbox((0, 0), l, font=font)[3] for l in lines)
    start_y = height // 2 - total_height // 2

    # Draw lines centered horizontally
    offset = 0 if flipped else width // 2
    for line in lines:
        line_width, _ = draw.textbbox((0, 0), line, font=font)[2:]

        text_x = (max_width - line_width) // 2
        draw.text((offset + margin + text_x, start_y), line, font=font, fill=(0, 0, 0, 255))
        start_y += line_height

def write_title(image, text, y_position, color, border_color, text_size):
    width, height = image.size
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("python/resources/Engine-Regular.otf", text_size)

    # Split and measure
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    x_center = width * 3 // 4
    x_text = x_center - text_width // 2
    y_text = y_position

    # Draw black border (stroke)

    fill_color = hex_to_rgba(color, 255)
    stroke_color = hex_to_rgba(border_color, 255)
    draw.text((x_text, y_text), text, font=font, fill=fill_color, stroke_width=6, stroke_fill=stroke_color)

def write_subtitle(image, text, y_position, color):
    width, height = image.size
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("python/resources/Engine-Regular.otf", 50)

    # Split and measure
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    x_center = width * 3 // 4
    x_text = x_center - text_width // 2
    y_text = height - y_position

    # Draw black border (stroke)
    fill_color = hex_to_rgba(color, 255)
    draw.text((x_text, y_text), text, font=font, fill=fill_color)

def write_author(image, text, y_position, color):
    width, height = image.size
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("python/resources/Engine-Regular.otf", 25)

    # Split and measure
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    x_center = width * 3 // 4
    x_text = x_center - text_width // 2
    y_text = height - y_position

    # Draw black border (stroke)
    fill_color = hex_to_rgba(color, 255)
    draw.text((x_text, y_text), text, font=font, fill=fill_color)

def write_summary(image, text, color):
    width, height = image.size
    font = ImageFont.truetype("python/resources/Engine-Regular.otf", 40)
    fill_color = hex_to_rgba(color, 255)
    halo_color = hex_to_rgba(invert_color(color), 255)
    # Wrap text to LEFT HALF
    margin = 100
    max_width = width // 2 - 2 * margin
    line_height = font.getmetrics()[0] + font.getmetrics()[1]

    # Split by newlines first
    paragraphs = text.split('\\n')
    lines = []
    draw_tmp = ImageDraw.Draw(image)
    
    for paragraph in paragraphs:
        words = paragraph.split()
        line = ""
        for word in words:
            test_line = line + (" " if line else "") + word
            w, _ = draw_tmp.textbbox((0, 0), test_line, font=font)[2:]
            if w <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        lines.append(line)
    
    
    # Total height
    total_h = sum(draw_tmp.textbbox((0, 0), l, font=font)[3] for l in lines)
    start_y = height // 2 - total_h // 2
    # Halo layer
    halo_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw_halo = ImageDraw.Draw(halo_layer)
    y = start_y
    for l in lines:
        w, _ = draw_halo.textbbox((0, 0), l, font=font)[2:]

        x = width // 4 - w // 2
        draw_halo.text((x, y), l, font=font, fill=halo_color, stroke_width=8, stroke_fill=halo_color)
        y += line_height
    # Apply Gaussian blur to halo
    halo_layer = halo_layer.filter(ImageFilter.GaussianBlur(5))
    # Composite with 50% opacity
    image.alpha_composite(Image.blend(Image.new("RGBA", image.size, (0,0,0,0)), halo_layer, 0.8))
    # Draw main black text
    y = start_y
    draw_main = ImageDraw.Draw(image)
    for l in lines:
        w, _ = draw_main.textbbox((0, 0), l, font=font)[2:]
        x = width // 4 - w // 2
        draw_main.text((x, y), l, font=font, fill=fill_color, stroke_width=1, stroke_fill=halo_color)
        y += line_height

def write_onomatopae_text(file, instructions, flipped=False):
    match = re.search(r"p(\d+)\.png", file)
    page_num = match.group(1)
    
    for ins in instructions:
        if str(ins.get("page")) != page_num:
            continue

        font = ImageFont.truetype("python/resources/FuturaBQ-DemiBoldOblique.otf", ins["size"])
        image = Image.open(file).convert("RGBA")

        text_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)

        x = ins["x"]
        if flipped:
            x += image.size[0] / 2

        # handle line breaks
        lines = ins["text"].split("\\n")
        line_height = font.getbbox("Hg")[3] - font.getbbox("Hg")[1]
        y = ins["y"]
        for line in lines:
            draw.text((x, y), line, font=font, fill=ins["color"])
            y += line_height

        text_layer = text_layer.rotate(ins["angle"], expand=0, center=(x, ins["y"]))
        result = Image.alpha_composite(image, text_layer)
        result.save(file)

        print(f"* added onomatopae to {file}")
