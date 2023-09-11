# NLP: Clean raw and messy text with regular expressions

## Background
This code is part of a larger NLP Machine Learning project. To train/finetune a Machine Learning model or to make predictions with it,
the input text first needs to be cleaned before it can be tokenized and used.

## General Info
The code can be used to clean and preprocess raw, unprocessed and messy text and mostly uses regular 
expressions (Python re package, Python 3.11) to do that. 
In "**main.py**", there is a messy sample text to be cleaned. The methods in the class CleanText in "**funcs/clean.py**" transform 
those parts of the text that are found by the compiled re objects/patterns defined in "**funcs/re_patterns.py**". 
These patterns and functions can be adjusted to specific needs. 
In addition to the Python re package, some other Python string functions (such as "maketrans", etc) are used.


## Setup
The **main.py** script contains sample text in the variable "*messy_text*". 

1. Go to **main.py** and paste the text you want to be cleaned into the variable "*messy_text*". Then run it. The cleaned text will be printed.
1. Adjust the class methods in "**funcs/clean.py**" and the regular expressions in "**funcs/re_patterns.py**" according to your needs.