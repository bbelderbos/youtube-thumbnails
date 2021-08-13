from thumbs import create_thumbnail


def _get_titles():
    with open("data/videos.txt") as f:
        for title in f.readlines():
            yield title.rstrip()


def main():
    titles = _get_titles()
    for title in titles:
        create_thumbnail(title)


if __name__ == "__main__":
    main()
