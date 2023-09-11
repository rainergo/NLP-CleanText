from . import re_patterns as repat


class CleanText:
    # Tables
    TBL_UMLAUTE: dict = {'ä': 'ae', 'Ä': 'Ae', 'ö': 'oe', 'Ö': 'Oe', 'ü': 'ue', 'Ü': 'Ue', 'ß': 'ss'}
    TBL_ACCENTS: dict = {'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'å': 'a', 'À': 'A', 'Á': 'A', 'Â': 'A',
                         'ç': 'c',
                         'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e', 'ȩ': 'e', 'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E',
                         'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i', 'Î': 'I', 'Ï': 'I',
                         'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'Ô': 'O', 'Ò': 'O', 'Ó': 'O',
                         'ù': 'u', 'ú': 'u', 'û': 'u', 'Ù': 'U', 'Û': 'U'}
    TBL_CURRENCY: dict = {'€': 'EUR', '$': 'USD', '£': 'GBP', '¥': 'JPY'}
    TBL_FANCY_QUOTATION_MARKS: dict[int, int] = {
        ord(x): ord(y) for x, y in
        [("ʼ", "'"), ("‘", "'"), ("’", "'"), ("´", "'"), ("`", "'"), ("“", '"'), ("”", '"'), ("„", "'")]}

    # Substitutions: Replace special character with value in respective TBL
    def sub_umlaute(self, text: str) -> str:
        table = str.maketrans(self.TBL_UMLAUTE)
        return text.translate(table)

    def sub_accent_chars(self, text: str) -> str:
        table = str.maketrans(self.TBL_ACCENTS)
        return text.translate(table)

    def sub_currency(self, text: str) -> str:
        """ Function makes space between curr, amount and unit (i.e. EUR200M -> EUR 200 M) to improve tokenization """
        table = str.maketrans(self.TBL_CURRENCY)
        text = text.translate(table)
        return repat.RE_CURR_AMOUNT.sub(
            repl=lambda m: m.group("curr") + ' ' + m.group("amount") + ' ' + m.group("unit"),
            string=text)

    def sub_measurements(self, text: str) -> str:
        """ Function makes space between amount and unit (i.e. 200km -> 200 km) to improve tokenization """
        return repat.RE_MEASUREMENTS.sub(
            repl=lambda m: m.group("amount") + ' ' + m.group("unit"), string=text)

    def sub_fancy_quot_marks(self, text: str) -> str:
        table = str.maketrans(self.TBL_FANCY_QUOTATION_MARKS)
        return text.translate(table)

    def rem_quot_marks(self, text: str) -> str:
        return repat.RE_QUOTATION_MARKS.sub(repl="", string=text)

    def rem_brackets(self, text: str, curly: bool = True, round: bool = False, square: bool = True) -> str:
        text = repat.RE_BRACKETS_CURLY.sub(repl="", string=text) if curly else text
        text = repat.RE_BRACKETS_ROUND.sub(repl="", string=text) if round else text
        text = repat.RE_BRACKETS_SQUARE.sub(repl="", string=text) if square else text
        return text

    def rem_strange_chars(self, text: str) -> str:
        text = repat.RE_REPEATING_CHARS.sub(repl=" ", string=text)
        text = repat.RE_SUSPICIOUS_CHARS.sub(repl=" ", string=text)
        text = repat.RE_BULLET_POINTS.sub(repl=" ", string=text)
        text = repat.RE_UNICODE_SYMBOLS.sub(repl="", string=text)
        text = repat.RE_STRANGE_DASHES.sub(repl="-", string=text)
        return text

    def mark_end_of_sentence(self, text: str, period: str = ". ") -> str:
        return repat.RE_LOCATION_EXACT_DATE.sub(repl=lambda m: m.group("locationanddate") + period, string=text)

    def split_listed_sentences(self, text: str, hyphen: str = ' - ', hyphen_replacement: str = '. ',
                               min_num_hyphens: int = 3) -> str:
        """ Splits bullet-listed sentences into sentences with period. But Gedankenstriche/pauses such as
        "Hello I am - in between dashes - sentence end." must be left untouched. Required num hyphens in pattern: >= 3.
         Expensive regex-operation, so check if num of hyphens in text is above min_num_hyphens to execute function. """

        def repl_func(matchobj):
            sentence_with_hyphenated_listings: str = matchobj.group(0)
            return repat.RE_HYPHENS_WITH_SPACE.sub(repl=hyphen_replacement, string=sentence_with_hyphenated_listings)

        if text.count(hyphen) >= min_num_hyphens:
            try:
                return repat.RE_SENTS_WITH_LISTINGS.sub(repl=repl_func, string=text)
            except:
                pass  # Todo: Logging here
        else:
            return text

    def sub_empty_lines_for_period(self, text: str, replacement: str = ". ") -> str:
        """ Substitute more than one empty lines with period. """
        return repat.RE_NO_PERIOD_NOR_HYPHEN_THEN_TWO_EMPTY_LINES.sub(repl=replacement, string=text)

    def rem_whitespace(self, text: str) -> str:
        """
        Replace all contiguous zero-width and line-breaking spaces and spaces before a sentence end with an empty
        string, non-line-breaking spaces with a single space and then strip any leading/trailing whitespace.
        """
        text = repat.RE_ZERO_WIDTH_SPACE.sub(repl="", string=text)
        text = repat.RE_LINEBREAK.sub(repl=r" ", string=text)
        text = repat.RE_NONBREAKING_SPACE.sub(repl=" ", string=text)
        text = repat.RE_SPACE_BEFORE_SENT_END.sub(repl="", string=text)
        return text.strip()

    def clean(self, text: str,
              sub_umlaute: bool = True, sub_accent_chars: bool = True, sub_curr: bool = True, sub_measure: bool = True,
              sub_fancy_quot_marks: bool = True, rem_brackets: bool = True, rem_quot_marks: bool = True,
              rem_strange_chars: bool = True, mark_end_of_sent: bool = True, split_listed_sents: bool = True,
              sub_empty_lines: bool = True, rem_whitespace: bool = True) -> str:

        text = self.sub_umlaute(text=text) if sub_umlaute else text
        text = self.sub_accent_chars(text=text) if sub_accent_chars else text
        text = self.sub_currency(text=text) if sub_curr else text
        text = self.sub_measurements(text=text) if sub_measure else text
        text = self.sub_fancy_quot_marks(text=text) if sub_fancy_quot_marks else text
        text = self.rem_quot_marks(text=text) if rem_quot_marks else text  # Should be after sub_fancy_quot_marks !!!
        text = self.rem_strange_chars(text=text) if rem_strange_chars else text
        text = self.rem_brackets(text=text) if rem_brackets else text
        text = self.mark_end_of_sentence(text=text) if mark_end_of_sent else text
        text = self.split_listed_sentences(text=text) if split_listed_sents else text
        text = self.sub_empty_lines_for_period(text=text) if sub_empty_lines else text
        text = self.rem_whitespace(text=text) if rem_whitespace else text  # rem_whitespace should be done last !!!
        return text
