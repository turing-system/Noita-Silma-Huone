# General notes

You will find more details about this project and the enigma of Noita's Eyes messages here : https://docs.google.com/document/d/1HRgOw1Lkhqds-hS51HEMnYJPnTWXiXYn2EdyBA0CDVY

Please note that most of scripts also include the python function that correspond to their job, directly usable inside your code.

# Install

-   Install Python 3.10
-   `pip install venv`
-   `python -m venv env`
    The following _line_ is for windows
-   `./env/Scripts/activate`
-   `pip install -r ./requirements.txt`
-   `python -m nltk.downloader popular`

# dummy_bruteforce.py
Will run a stupid bruteforce that will test a few set of possibilities (~1M) and output in a file values that have at last a half of a word in it.

Just run over an fixed sized shift Alberti.

Output file are build as following: `f.write(f"{i}\t{shift_initial}\t{shift_step}\t{shift_stall}\t{word_found_count}\n")`

As:
-   `i` the iteration of the loop (allow to build the key from the rest of initial parameters)
-   `shift_initial` the initial shift for the Alberti cipher
-   `shift_step` the step of each shift for the Alberti cipher
-   `shift_stall` the stall of shift for the Alberti cipher

Use the following command to generate the txt file:
`python dummy_bruteforce.py`

Please note that dummy_bruteforce **can't** solve eyes messages. (c.f. @codewarrior0 work)

# sentence_broker.py
The sentence broker is parsing texts files in order to count occurences of words by position and by the previous words.
Use to compute frequencies, usefull for your enigma.

It will parse all texts files in `./references/gutenberg` folder as utf-8 files (you will need to create it and add the files).

Use the following command to generate the json file:
`python ./sentence_broker.py`

If you want to parse Gutenberg project's books → **don't**, ask @Dykoine on the discord and he will give you the result. It's unneeded to overload their servers. 

# dictionnary_generator.py
Will build a list of words.

Use the following command to generate the txt file:
`python dictionnary_generator.py`


# Run unit tests
`python -m unittest`
