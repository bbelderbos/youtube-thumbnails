import os
from pathlib import Path
import sys

import feedparser

from thumbs import create_thumbnail

PYBITES_FEED = "https://feeds.buzzsprout.com/1501156.rss"
TEMPLATE_IMG = Path("images") / "podcast-template.png"

OUTPUT_DIR = Path("images") / "podcast"
if not OUTPUT_DIR.exists():
    os.mkdir(OUTPUT_DIR)

TEXT_COLOR = (0, 0, 0, 255)
MAX_LEN = 60


def get_titles():
    """Get podcast titles, newest first"""
    entries = sorted(
        feedparser.parse(PYBITES_FEED)["entries"],
        key=lambda x: x.published_parsed,
        reverse=True,
    )
    titles = [
        entry.title.replace("-", "|")
        for entry in entries
        if entry.title.startswith("#")
    ]
    for title in titles:
        # for long titles we need an extra newline (enforced by "|")
        if len(title) > MAX_LEN:
            index_last_space = title[:MAX_LEN].rfind(" ")
            first_line = title[:index_last_space]
            second_line = title[index_last_space:]
            title = f"{first_line}|{second_line}"
        yield title


def main(max_num_images=None):
    titles = list(get_titles())
    for i, title in enumerate(titles, start=1):
        print(title)
        create_thumbnail(title, template=TEMPLATE_IMG,
                         output_dir=OUTPUT_DIR,
                         font_size=50,
                         text_color=TEXT_COLOR,
                         start_offset=(50, 100),
                         line_spacing=70)
        if max_num_images is not None and max_num_images == i:
            break


if __name__ == "__main__":
    if len(sys.argv) == 2:
        max_num_images = int(sys.argv[1])
        main(max_num_images)
    else:
        main()
