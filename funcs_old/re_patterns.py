import re
from typing import Pattern

# Brackets
RE_BRACKETS_CURLY_AND_CONTENT: Pattern = re.compile(r"\{[^{}]*?\}")
RE_BRACKETS_ROUND_AND_CONTENT: Pattern = re.compile(r"\([^()]*?\)")
RE_BRACKETS_SQUARE_AND_CONTENT: Pattern = re.compile(r"\[[^\[\]]*?\]")
RE_BRACKETS_CURLY: Pattern = re.compile(r"[{}]")
RE_BRACKETS_ROUND: Pattern = re.compile(r"[()]")
RE_BRACKETS_SQUARE: Pattern = re.compile(r"[\[\]]")

# Linebreaks and spaces
RE_LINEBREAK: Pattern = re.compile(r"(\r\n|[\n\v])+")
RE_NO_PERIOD_NOR_HYPHEN_THEN_TWO_EMPTY_LINES: Pattern = re.compile(r"(?<![.-])(?:\r\n|[\n\v]){2,}")
RE_NONBREAKING_SPACE: Pattern = re.compile(r"[^\S\n\v]+")
RE_ZERO_WIDTH_SPACE: Pattern = re.compile(r"[\u200B\u2060\uFEFF]+")
RE_SPACE_BEFORE_SENT_END: Pattern = re.compile(r"\s+(?=\.)")

RE_HEADLINE: Pattern = re.compile(r"(?P<headline>^\b.+?[^.!?]\b$)",
                                  flags=re.MULTILINE)

RE_SENTS_WITH_LISTINGS: Pattern = re.compile(
    r"(?:(?P<sentstart>^|(?<=\w\b(?:\.|\!|\?)\s)|(?:^|(?<=\w\b(?:\.|\!|\?)\s))*(?:[\w\s;,:/()-]+\w{1,}\.\w{1,}\.(?:\w{1,}\.)*)*)(?P<wordsstart>[\w\s;,:/()-]+?)(?:(?P<hyphen>\s*-*\s+-+\s*-*\s*)(?(hyphen)[\w\s;,:/()-]*)(?P<abbr>\w{1,}\.\w{1,}\.(?:\w{1,}\.)*)*(?(abbr)[\w\s;,:/()-]*)){3,}(?P<endabbr>\w{1,}\.\w{1,}\.(?:\w{1,}\.)*(?=(?:\n{3,}[A-ZÄÖÜ])|$))*(?(endabbr)|(?:\w{1,}\.\w{1,}\.(?:\w{1,}\.)*)*[\w\s;,:/()-]+[.?!]*))",
    flags=re.MULTILINE)

RE_HYPHENS_WITH_SPACE: Pattern = re.compile(
    r"\s*-*\s+-+\s*-*\s*")  # Must be without (named) group. Otherwise split will contain delimiters !!!

# Quotation marks
RE_QUOTATION_MARKS: Pattern = re.compile(r"\'(?!s)|\"")

# Dates
RE_DATE_EXACT: Pattern = re.compile("(%s|%s|%s|%s)" % (
    # day month-name year
    r"\b(?:[0-3]?[0-9][\.\s\/\-]*)(?:jan|feb|m[aä]r|apr|ma[iy]|jun|jul|aug|sep|o[ck]t|nov|de[cz])\w*(?:[\.\s\/\-]*[1|2]?[0|9]?[0-9]{2})\b",
    # month-name year
    r"\b(?:jan|feb|m[aä]r|apr|ma[iy]|jun|jul|aug|sep|o[ck]t|nov|de[cz])\w*(?:\s*[0-3]?[0-9]),\s*[1|2]?[0|9]?[0-9]{2}\b",
    # day month year
    r"\b(?:[0-3]?[0-9][/-/.]+)(?:[0-1][0-9])(?:[/-/.]*[1|2]?[0|9]?[0-9]{2})\b",
    # year month day
    r"\b(?:[1|2][0|9][0-9]{2}[-/.]*)(?:[0-1][0-9])(?:[-/.]*[0-3]?[0-9])\b"), flags=re.IGNORECASE)

RE_LOCATION_EXACT_DATE: Pattern = re.compile(
    r"(?P<locationanddate>[\w\s,]+?,[\w\s,]*"
    + RE_DATE_EXACT.pattern
    + r")(?P<suffix>[\s\-]*)", flags=re.MULTILINE | re.IGNORECASE
)

RE_YEAR_PERIOD = re.compile(r"([1|2][9|0]\d{2}\.)")

# Strange chars
RE_SUSPICIOUS_CHARS: Pattern = re.compile(r"(?:^|\s*)[\\#<>+|~]{1,}(?:\s*|$)")
RE_REPEATING_CHARS: Pattern = re.compile(r"(?:^|\s)[\\\-=+]{2,}(?:\s|$)")
RE_UNICODE_SYMBOLS: Pattern = re.compile(r"([\u00ab\u00BB\u00AE])")
RE_STRANGE_DASHES: Pattern = re.compile(r"([\u2010-\u2015\uFF0D\uFE63\u2043\u1680\u002D\u2043\u1806])")
RE_BULLET_POINTS: Pattern = re.compile(
    # require bullet points as first non-whitespace char on a new line, like a list
    r"((^|\n)\s*?)"
    r"([\u2022\u2023\u2043\u204C\u204D\u2219\u25aa\u25CF\u25E6\u29BE\u29BF\u30fb])",
)

RE_CURR_SYMBOL: Pattern = re.compile(r"[$¢£¤¥ƒ֏؋৲৳૱௹฿៛ℳ元円圆圓﷼\u20A0-\u20C0]")
RE_CURR_AMOUNT: Pattern = re.compile(r"(?P<curr>EUR|USD|GBP|JPY)(?:\s{0,})(?P<amount>[\,\.\d]+)(?P<unit>\s*\w{1,}\.?)",
                                     flags=re.IGNORECASE)

RE_MEASUREMENTS: Pattern = re.compile(r"(?P<amount>\d+)\s*(?P<unit>(?:mm|cm|m|km|km2)(?:2|3)?)",
                                      flags=re.IGNORECASE)

RE_MEASUREMENTS_PERIOD: Pattern = re.compile(r"(?P<unit>(?:mm|cm|m|km)(?:2|3)?)\.",
                                             flags=re.IGNORECASE)

# Emojis
RE_EMOJI: Pattern = re.compile(
    r"[\u2600-\u26FF\u2700-\u27BF\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF\U0001FA70-\U0001FAFF]",
    flags=re.IGNORECASE,
)

# Internet and Email
RE_URL: Pattern = re.compile(
    r"(?:^|(?<![\w/.]))"
    # protocol identifier
    # r"(?:(?:https?|ftp)://)"  <-- alt?
    r"(?:(?:https?://|ftp://|www\d{0,3}\.))"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?"
    r"(?:"
    # IP address exclusion
    # private & local networks
    r"(?!(?:10|127)(?:\.\d{1,3}){3})"
    r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
    r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    r"|"
    # host name
    r"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9])"
    # domain name
    r"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9])*"
    # TLD identifier
    r"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
    r")"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:/\S*)?"
    r"(?:$|(?![\w?!+&/]))",
    flags=re.IGNORECASE,
)

RE_SHORT_URL: Pattern = re.compile(
    r"(?:^|(?<![\w/.]))"
    # optional scheme
    r"(?:(?:https?://)?)"
    # domain
    r"(?:\w-?)*?\w+(?:\.[a-z]{2,12}){1,3}"
    r"/"
    # hash
    r"[^\s.,?!'\"|+]{2,12}"
    r"(?:$|(?![\w?!+&/]))",
    flags=re.IGNORECASE,
)

RE_EMAIL: Pattern = re.compile(
    r"(?:mailto:)?"
    r"(?:^|(?<=[^\w@.)]))([\w+-](\.(?!\.))?)*?[\w+-]@(?:\w-?)*?\w+(\.([a-z]{2,})){1,3}"
    r"(?:$|(?=\b))",
    flags=re.IGNORECASE,
)

RE_PHONE_NUMBER: Pattern = re.compile("(%s|%s)" % (
    # Intl.
    r"(?:\+(?:1|44|90)[\-\s]+[0-9]{3}([\-\s0-9]{4,11}(?:$|\s)))|(?:\+[0-9]{2,3}[\-\s]+\(?[0-9]{2,5}\)?[\/\-\s0-9]{4,11}(?:$|\s))",
    # National
    r"(?P<nat1>0|\+)?(?(nat1)[0-9]{2,5}|\(0?[0-9]{2,5}\))[\s\-\/]([\-\s\d]{3,11})($|\s+)"),
                                      flags=re.IGNORECASE)

RE_ABBREVIATION: Pattern = re.compile(r"(?<!-)\b[a-zA-Z]{1,7}\.\-{0,1}(?:[a-zA-Z]{1,4}\.){0,2}", flags=re.IGNORECASE)


if __name__ == '__main__':
    # Print pattern of any compiled object:
    print(RE_SENTS_WITH_LISTINGS.pattern)
