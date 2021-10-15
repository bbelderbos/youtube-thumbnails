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

# TODO: this is not scalable but works for now
replacements = ["software planning", "decision fatigue",
                "Creativity as a Developer", "with Andrew", "to Open",
                "the Classroom", "COVID World", "Ryan Austin",
                "content provider", "Marketer to", "Partners",
                "Software Architect"]


def get_titles():
    titles = sorted(
        entry.title.replace("-", "|")
        for entry in feedparser.parse(PYBITES_FEED)["entries"]
        if entry.title.startswith("#")
    )
    for title in titles:
        for term in replacements:
            title = title.replace(term, f"| {term}")
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
