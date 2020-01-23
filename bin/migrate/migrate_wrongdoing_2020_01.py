#!/usr/bin/env python

import unicodecsv
import sys
import codecs


FIELDNAMES = 'ref_number,file_id_number,file_id_date,case_description_en,case_description_fr,findings_conclusions,recommendations_corrective_measures_en,recommendations_corrective_measures_fr,record_created,record_modified,user_modified,owner_org,owner_org_title'.split(',')

assert sys.stdin.read(3) == codecs.BOM_UTF8

in_csv = unicodecsv.DictReader(sys.stdin, encoding='utf-8')
out_csv = unicodecsv.DictWriter(sys.stdout, fieldnames=FIELDNAMES, encoding='utf-8')
out_csv.writeheader()


for line in in_csv:
    line['user_modified'] = '*'  # special "we don't know" value
    out_csv.writerow(line)
