import pytest
from pytest import fail
import usfmtc
import xml.etree.ElementTree as et
import re, io

def asusfm(root):
    grammar = usfmtc.Grammar()
    with io.StringIO() as fh:
        usfmtc.usx2usfm(fh, root, grammar)
        res = fh.getvalue()
    return res

def _dousfm(s):
    doc = usfmtc.readFile(s, informat="usfm")
    doc.canonicalise()
    r = doc.getroot()
    et.dump(r)
    f = asusfm(r)
    print(f)
    return (doc, f)

def test_hardspaces():
    usfm = r"""\id TST testing hardspaces
\c 1 \p \v 1 This{0}has a hard{0}space\f + \fr 1:1{0}\ft And here\f*""".format("\u00A0")
    doc, f = _dousfm(usfm)
    r = doc.getroot()
    e = r.find('.//char[@style="fr"]')
    t = e.text
    if not t.endswith("\u00A0"):
        fail("No hard space after fr in usx")
    if not re.search("\u00A0\\\\ft", f):
        fail("No hard space after fr in usfm")

def test_glossary():
    usfm = r"""\id TST glossary in text
\c 1 \p \v 1 We have \w glossary\w* words to deal with"""
    doc, f = _dousfm(usfm)
    if not re.search(" \\w", f):
        fail("No space before glossary word")
