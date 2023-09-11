from funcs.clean import CleanText

messy_text = """This raw and uncleaned text shall be cleaned. The text contains strange listings -
with or without linebreaks - here is another listing - and another one and the
sentence continues after the line break - with that I see trouble ahead

- the listings also contain Umlaute such as äpfel, Mähdrescher and also accents such as Áccent and élise
- or symbols such as the currency signs € 300 and $ 400 that potentially shall be converted to letters.
We might want to treat these listings as separate sentences. But on the other side we might want dashes that highlight 
something import such as - I am important - like this to be untouched


Then above us, there might be unnecessary space we want to get rid of. We also might want 200km to be written as 200 km and 
€300 as Eur 300, otherwise our tokenizers later will have some problems. We might also want to get rid of fancy quotation 
marks such as ´ffffff`. We also might want to get rid of this [parenthesis] and this {curly brackets}
but want to keep this (round one). Do we need strange symbols such as these # < > + | to be removed? No problem. We also want to remove
excessive whitespace like          this to be cleaned. We might. Or we might not. We can set this in the individual 
functions of the class CleanText.
    """

if __name__ == '__main__':
    cleaner = CleanText()
    cleaned_text = cleaner.clean(text=messy_text,
                                 sub_umlaute=True, sub_accent_chars=True, sub_curr=True, sub_measure=True,
                                 sub_fancy_quot_marks=True, rem_brackets=True, rem_quot_marks=True,
                                 rem_strange_chars=True, mark_end_of_sent=True, split_listed_sents=True,
                                 sub_empty_lines=True, rem_whitespace=True)
    print('CLEANED TEXT:\n', cleaned_text)
