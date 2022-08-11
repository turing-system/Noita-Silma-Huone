# -*- coding: utf-8 -*-
""" Gutenberg project is a website where there is a lot of
books in txt/utf-8 format that you can download for free.

A usefull database for texts analysis.

You shouldn't use it. Ask for @Dykoine for direct result.
There is no use to overload their servers.

Here a very simple downloader.
"""
import re
import os
import requests

def generator_book_file_stream():
    """ Yield stream to temporary files of utf-8 text of book
    
    Book are found on the Gutenberg project.

    The generator will attempt to close the previous stream
    on yield the next, then delete the previous file.

    Returns:
        (io.IOBase) Yield stream to book file. Return None when no more book are available.
    """

    book_id_pattern = re.compile(r'https?://www.gutenberg.org/etext/(?P<book_id>[0-9]+)')

    with open('./references/catalog.marc', 'r', encoding='utf-8') as catalog_stream:
        # Reading chunk by chunk and adding then in a buffer to avoid
        # to skip matchs that are in-between chunk.
        size_chunk = 1024
        buffer = ''
        catalog_chunk = catalog_stream.read(size_chunk)
        while len(catalog_chunk) > 0:
            buffer += catalog_chunk

            last_match = None
            for match in book_id_pattern.finditer(buffer):
                last_match = match
                book_id = match.group('book_id')
                
                # Each time we found a match, we generate the URL to the UTF-8 book link and download him.
                try:
                    response = requests.get( f"https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8")
                    with open("./references/gutenberg.temp", "wb") as temp_file:
                        temp_file.write(response.content)

                    with open("./references/gutenberg.temp", "r", encoding="utf-8") as temp_file:
                        # Then yield the file stream
                        # Note it stay "in the with" statement until next()
                        # is call on the generator, allowing such structure.
                        yield temp_file

                    try:
                        # Just cleaning
                        os.remove("./references/gutenberg.temp")
                    except Exception:
                        pass
                except Exception as error:
                    # Shouldn't happen, only for debugging.
                    print(error)

            # Trash used part of the buffer
            if last_match:
                buffer = buffer[last_match.end('book_id'):]

            catalog_chunk = catalog_stream.read(size_chunk)

if __name__ == "__main__":
    print("This file does nothing by himself, it was design to be use by the sentence broker.")
    # for i, a in enumerate(generator_book_file_stream()):
    #     print(a.read(1024))
    #     if i > 3:
    #         break