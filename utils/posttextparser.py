import os
import re
import time
from typing import List

import spacy

from utils.console import print_step
from utils.voice import sanitize_text


# working good
def posttextparser(obj, *, tried: bool = False) -> List[str]:
    """
    The function takes in a string object, replaces newline characters with spaces, and attempts to load
    a spacy model for English language processing. If the model cannot be loaded, it will attempt to
    download it and try again. If it still cannot be loaded, it will print an error message and raise an
    exception. The function returns a list of strings.
    @param obj - The input text that needs to be parsed and processed.
    @param {bool} [tried=False] - A boolean parameter that indicates whether the function has already
    attempted to load the spacy model and failed. It is set to False by default.
    @returns a list of strings.
    """
    text: str = re.sub("\n", " ", obj)
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError as e:
        if not tried:
            os.system("python -m spacy download en_core_web_sm")
            time.sleep(5)
            return posttextparser(obj, tried=True)
        print_step(
            "The spacy model can't load. You need to install it with the command \npython -m spacy download en_core_web_sm ")
        raise e

    doc = nlp(text)

    newtext: list = []

    for line in doc.sents:
        if sanitize_text(line.text):
            newtext.append(line.text)

    return newtext
