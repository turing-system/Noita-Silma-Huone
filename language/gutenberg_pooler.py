# -*- coding: utf-8 -*-
""" Gutenberg project is a website where there is a lot of
books in txt/utf-8 format that you can download for free.

A usefull database for texts analysis.

You shouldn't use it. Ask for @Dykoine for direct result.
There is no use to overload their servers.

If I'm not available, note that this script require
the 'catalog.marc' file that come from the Gutenberg website.

Link to book are in it.

Here a very simple downloader.
"""
import re
import requests


def generator_gutenberg_book_id(skip_to: int = 0) -> str:
    """Yield url of utf-8 text of book.

    Book are found on the Gutenberg project.

    Args:
        skip_to (int): skip the n first links. Mostly for dev purpose.
    Returns:
        (str) Yield url to book file. Return None when no more book are available.
    """

    book_id_pattern = re.compile(
        r"\| eng [^\|]+https?://www.gutenberg.org/etext/(?P<book_id>[0-9]+)[^\|]+\|"
    )

    skip_remain = skip_to

    with open("./references/catalog.marc", "r", encoding="utf-8") as catalog_stream:
        # Reading chunk by chunk and adding then in a buffer to avoid
        # to skip matchs that are in-between chunk.
        size_chunk = 1024
        buffer = ""
        catalog_chunk = catalog_stream.read(size_chunk)
        while len(catalog_chunk) > 0:
            buffer += catalog_chunk

            last_match = None
            for match in book_id_pattern.finditer(buffer):
                last_match = match

                # Apply skip_to
                if skip_remain:
                    skip_remain -= 1
                    continue
                else:
                    yield match.group("book_id")

            # Trash used part of the buffer
            if last_match:
                buffer = buffer[last_match.end("book_id") :]

            catalog_chunk = catalog_stream.read(size_chunk)


if __name__ == "__main__":
    import os
    for i, book_id in enumerate(generator_gutenberg_book_id()):
        book_file_path = f"./references/gutenberg/{book_id}.book.txt"

        # Skip already done
        if os.path.isfile(book_file_path):
            continue

        print(f"Get the book {book_id} (#{i+1}th){" " * 10}", end='\r')
        response = requests.get(f"https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8")
        try:
            response.content.decode("utf8")
            with open(book_file_path, "wb") as book_file:
                book_file.write(response.content)
        except UnicodeError:
            pass
    print()  # force new line