from pathlib import Path
import re
import sys
from string import ascii_lowercase

from PIL import Image, ImageDraw, ImageFont

BACKGROUND_IMG = "base-thumbnail.png"
OUTPUT_DIR = "images"
FONT_FILE = Path('fonts') / 'Berlin-Sans-FB-Regular.ttf'
START_OFFSET_TEXT = (650, 150)
TEXT_COLOR = (255, 255, 255, 255)
LINE_SPACING = 120
NEW_LINE = "\\n"


def _add_text(image, base, text, offset,
              fontfile=FONT_FILE,
              font_size=100):
    """Adds text on the image canvas"""
    font = ImageFont.truetype(str(fontfile), font_size)
    draw_context = ImageDraw.Draw(image)
    draw_context.text(offset, text, font=font, fill=TEXT_COLOR)


def _create_output_file_name(text):
    fname = text.replace(NEW_LINE, " ")
    fname = re.sub(f"[^{ascii_lowercase}]", "-", fname.lower())
    fname = f"{fname}.png"
    return fname


def create_thumbnail(text, template=BACKGROUND_IMG):
    base = Image.open(template).convert('RGBA')
    image = Image.new('RGBA', base.size)

    offset = START_OFFSET_TEXT

    for i, line in enumerate(text.split(NEW_LINE)):
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
