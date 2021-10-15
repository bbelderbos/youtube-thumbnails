import os
from pathlib import Path

import feedparser

from thumbs import create_thumbnail

PYBITES_FEED = "https://feeds.buzzsprout.com/1501156.rss"
TEMPLATE_IMG = Path("images") / "podcast-template.png"

OUTPUT_DIR = Path("images") / "podcast"
if not OUTPUT_DIR.exists():
    os.mkdir(OUTPUT_DIR)

TEXT_COLOR = (0, 0, 0, 255)


def _get_titles():
    return sorted(
        entry.title.replace("-", "|")
        for entry in feedparser.parse(PYBITES_FEED)["entries"]
        if entry.title.startswith("#")
    )


def main():
    titles = _get_titles()
    for title in titles[:2]:
        print(title)
        create_thumbnail(title, template=TEMPLATE_IMG,
                         output_dir=OUTPUT_DIR,
                         font_size=80,
                         text_color=TEXT_COLOR,
                         start_offset=(50, 50))


if __name__ == "__main__":
    main()
