import os
from pathlib import Path
import re
from string import ascii_lowercase, digits
import sys

from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

load_dotenv()

BACKGROUND_IMG = os.environ["THUMB_BACKGROUND_IMAGE"]
OUTPUT_DIR = "images"
FONT_FILE = os.environ["THUMB_FONT_TTF_FILE"]
START_OFFSET_TEXT = (650, 160)
TEXT_COLOR = (255, 255, 255, 255)
LINE_SPACING = 140
SEPARATOR = "|"


def _add_text(image, base, text, offset,
              fontfile=FONT_FILE,
              font_size=100):
    """Adds text on the image canvas"""
    font = ImageFont.truetype(fontfile, font_size)
    draw_context = ImageDraw.Draw(image)
    draw_context.text(offset, text, font=font, fill=TEXT_COLOR)


def _create_output_file_name(text):
    fname = text.replace(SEPARATOR, " ")
    fname = re.sub(f"[^{ascii_lowercase + digits}]", "-", fname.lower())
    fname = f"{fname}.png"
    return fname


def create_thumbnail(text, template=BACKGROUND_IMG):
    base = Image.open(template).convert('RGBA')
    image = Image.new('RGBA', base.size)

    offset = START_OFFSET_TEXT

    for i, line in enumerate(text.split(SEPARATOR)):
        left, top = offset
        top += i * LINE_SPACING
        _add_text(image, base, line, (left, top))

    out = Image.alpha_composite(base, image)

    output_file_path = Path(OUTPUT_DIR) / _create_output_file_name(text)

    out.save(output_file_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} 'text on banner'")
        sys.exit(1)
    create_thumbnail(sys.argv[1])
