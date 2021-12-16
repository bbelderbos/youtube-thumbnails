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
MAX_LEN = 60


def get_titles():
    titles = sorted(
        entry.title.replace("-", "|")
        for entry in feedparser.parse(PYBITES_FEED)["entries"]
        if entry.title.startswith("#")
    )
    for title in titles:
        # for long titles we need an extra newline (enforced by "|")
        if len(title) > MAX_LEN:
            index_last_space = title[:MAX_LEN].rfind(" ")
            first_line = title[:index_last_space]
            second_line = title[index_last_space:]
            title = f"{first_line}|{second_line}"
        yield title


def main():
    titles = list(get_titles())
    for title in titles:
        print(title)
        create_thumbnail(title, template=TEMPLATE_IMG,
                         output_dir=OUTPUT_DIR,
                         font_size=50,
                         text_color=TEXT_COLOR,
                         start_offset=(50, 100),
                         line_spacing=70)


if __name__ == "__main__":
    main()
