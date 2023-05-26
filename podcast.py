import argparse
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


def _wrap_title(title):
    if len(title) > MAX_LEN:
        index_last_space = title[:MAX_LEN].rfind(" ")
        first_line = title[:index_last_space]
        second_line = title[index_last_space:]
        title = f"{first_line}|{second_line}"
    return title


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
        title = _wrap_title(title)
        yield title


def main(max_num_images=None, podcast_title=None, dry_run=False):
    if podcast_title is not None:
        titles = [_wrap_title(podcast_title)]
    else:
        titles = list(get_titles())

    for i, title in enumerate(titles, start=1):
        if dry_run:
            print(title)
        else:
            create_thumbnail(
                title,
                template=TEMPLATE_IMG,
                output_dir=OUTPUT_DIR,
                font_size=50,
                text_color=TEXT_COLOR,
                start_offset=(50, 100),
                line_spacing=70,
            )
        if max_num_images is not None and max_num_images == i:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make podcast YouTube thumb images.")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-n",
        "--max_num_images",
        type=int,
        help="The maximum number of images working from feed.",
    )
    group.add_argument(
        "-t-", "--podcast_title", type=str, help="The title of the podcast."
    )

    parser.add_argument(
        "-d",
        "--dry_run",
        action="store_true",
        help="Perform a dry run without executing the main function.",
    )

    args = parser.parse_args()
    main(args.max_num_images, args.podcast_title, args.dry_run)
