import pytest
from pytest import fail
import usfmtc
import xml.etree.ElementTree as et
import re, io

def asusfm(root, grammar=None):
    if grammar is None:
        grammar = usfmtc.Grammar()
    with io.StringIO() as fh:
        usfmtc.usx2usfm(fh, root, grammar)
        res = fh.getvalue()
    return res

def _dousfm(s, grammar=None):
    doc = usfmtc.readFile(s, informat="usfm", grammar=grammar)
    doc.canonicalise()
    r = doc.getroot()
    et.dump(r)
    f = asusfm(r, grammar=grammar)
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
        fail("No space before glossary word in {f}")

def test_chap():
    usfm = r"""\id TST chapters followed by space
\c 3\p^97 \v 1 This is tight"""
    doc, f = _dousfm(usfm)
    if not re.search(r" 3\s", f, flags=re.S):
        fail("No space after chapter number in {f}")

def test_vp():
    usfm = r"""\id TST publishable verses
\c 3
\cp 3a\cp*
\p
\v 1 \vp (23)\vp* This is the text"""
    doc, f = _dousfm(usfm)
    if 'vp*' not in f:
        fail("vp not closed in {f}")
    if 'cp*' in f:
        fail("Found cp* in {f}")

def test_headms():
    grammar = usfmtc.usfmparser.Grammar()
    grammar.marker_categories['zlabel'] = 'milestone'
    grammar.attribmap['zlabel'] = 'id'
    usfm = r"""\id GEN A test
\zlabel|GEN\*
\h Genesis
\toc1 Genesis
\c 1
\p
\v 1 In the beginning God"""
    doc, f = _dousfm(usfm, grammar=grammar)
    if "\n\\zlabel" not in f:
        fail("zlabel escaped in {f}")

