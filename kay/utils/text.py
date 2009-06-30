import re

ustring_re = re.compile(u"([\u0080-\uffff])")

def javascript_quote(s, quote_double_quotes=False):

    def fix(match):
        return r"\u%04x" % ord(match.group(1))

    if type(s) == str:
        s = s.decode('utf-8')
    elif type(s) != unicode:
        raise TypeError, s
    s = s.replace('\\', '\\\\')
    s = s.replace('\r', '\\r')
    s = s.replace('\n', '\\n')
    s = s.replace('\t', '\\t')
    s = s.replace("'", "\\'")
    if quote_double_quotes:
        s = s.replace('"', '&quot;')
    return str(ustring_re.sub(fix, s))
