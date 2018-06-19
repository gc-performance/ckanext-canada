#!/usr/bin/env python

"""
Usage: deepl.py strings.csv deepldb.csv SOURCE_LANG TARGET_LANG AUTH_KEY

Use api.deepl.com to update db.csv with translations of strings.csv

strings.csv is a headerless one-column csv containing text in SOURCE_LANG
deepldb.csv is the saved translation database, will be created if it doesn't exist

strings that exist in deepldb.csv won't be re-translated. New translations are
appended to deepldb.csv
"""

import unicodecsv
import sys
import codecs
from datetime import datetime
import requests

try:
    strings, deepldb, source_lang, target_lang, auth_key = sys.argv[1:]
except ValueError:
    sys.stderr.write(__doc__)
    sys.exit(1)

header = (
    codecs.BOM_UTF8 + 'source',
    'text',
    'timestamp',
    'detected_source_language',
    'source_lang',
    'target_lang')

def deepl_query(s):
    resp = requests.post('https://api.deepl.com/v1/translate', {
        'auth_key': auth_key,
        'source_lang': source_lang,
        'target_lang': target_lang,
        'text': s}).json()['translations'][0]
    return (
        s,
        resp['text'],
        unicode(datetime.utcnow()),
        resp['detected_source_language'],
        source_lang,
        target_lang)

seen = set()
try:
    with open(deepldb) as f:
        reader = unicodecsv.reader(f)
        h = next(reader)
        h = tuple(c.encode('utf-8') for c in h)
        assert h == header, ('wrong header', h, header)
        for src, txt, ts, dsl, sl, tl in reader:
            seen.add(src.lower())
except IOError:
    with open(deepldb, 'w') as f:
        unicodecsv.writer(f).writerow(header)

stats = (0, 0)
def update_stats(found, added):
    global stats
    f, a = stats
    stats = f + found, a + added
    sys.stderr.write('\rExisting: %d  Found: %d  Added: %d' % ((len(seen),) + stats))

update_stats(0, 0)

with open(deepldb, 'a') as out_f:
    out = unicodecsv.writer(out_f)
    with open(strings) as in_f:
        reader = unicodecsv.reader(in_f)
        for s, in reader:
            if s.lower() in seen:
                update_stats(1, 0)
                continue
            out.writerow(deepl_query(s))
            update_stats(0, 1)

sys.stderr.write('\n')
