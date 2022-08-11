# Install

-   Install Python 3.10
-   `pip install venv`
-   `python -m venv env`
    The following _line_ is for windows
-   `./env/Scripts/activate`
-   `pip install -r ./requirements.txt`
-   `python -m nltk.downloader popular`

# Unit tests

`python -m unittest`

# dummy_bruteforce.py

`python dummy_bruteforce.py`

Please note that dummy_bruteforce **can't** solve eyes messages

# sentence_broker.py
The sentence broker is parsing texts files in order to count occurences of words by position and by the previous words.
Use to compute frequencies, usefull for your enigma.

`python ./sentence_broker.py` will parse all texts files in `./references` folder as utf-8 files (you will need to create it and add the files).

If you want to parse Gutenberg project's books → **don't**, ask @Dykoine on the discord and he will give you the result. It's unneeded to overload their servers. 

# Build the dictionnary

`python dictionnary_generator.py`
Please note that dictionnary_generator also include the python function, directly usable inside your code.
