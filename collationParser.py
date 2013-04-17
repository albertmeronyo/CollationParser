#!/usr/bin/python
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON
import re

g = {
"A": 1,
"B": 2,
"C": 3,
"D": 4,
"E": 5,
"F": 6,
"G": 7,
"H": 8,
"I": 9,
"K": 10,
"L": 11,
"M": 12,
"N": 13,
"O": 14,
"P": 15,
"Q": 16,
"R": 17,
"S": 18,
"T": 19,
"U": 20,
"V": 21,
"X": 22,
"Y": 23,
"Z": 24
}

sparql = SPARQLWrapper("http://ops.few.vu.nl:8890/sparql")
sparql.setQuery("""
PREFIX vocab: <http://stcn.data2semantics.org/vocab/resource/>

SELECT ?f
FROM <http://stcn.data2semantics.org>
WHERE {
?p rdf:type vocab:Publicatie;
   vocab:publications_kmc4060 ?f ;
   vocab:drukker ?drukker .
   FILTER (?drukker IN (<http://stcn.data2semantics.org/drukker/304650463>, <http://stcn.data2semantics.org/drukker/207234116>, <http://stcn.data2semantics.org/drukker/16196141x>, <http://stcn.data2semantics.org/drukker/111952999>, <http://stcn.data2semantics.org/drukker/075573539>, <http://stcn.data2semantics.org/drukker/075573520>, <http://stcn.data2semantics.org/drukker/075570882>, <http://stcn.data2semantics.org/drukker/075553422>, <http://stcn.data2semantics.org/drukker/075547740>, <http://stcn.data2semantics.org/drukker/332485722>, <http://stcn.data2semantics.org/drukker/328745081>, <http://stcn.data2semantics.org/drukker/186624611>, <http://stcn.data2semantics.org/drukker/143840789>))
} LIMIT 100
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

#results = ["A-G`SUP`12`LO` H`SUP`6`LO` (lacks H6, blank?)", "`SUP`8`LO` (*1+Û1) A-2C`SUP`8`LO` 2D`SUP`4`LO`", "`SUP`8`LO` A-L`SUP`8`LO` M`SUP`6`LO`"]

for r in results["results"]["bindings"]:
#for r in results:
    f = r["f"]["value"]
    #f = r
    print "Formula:", f.encode('utf8')
    prog = re.compile('''
                      (.(?P<cover_sheet>>[0-9]))?                                  # Cover sheet
                      (\`SUP\`(?P<pren>[0-9]+)\`LO\`\s*(?P<pre>(\(.*\)\s*))?)?     # Preface sheets
                      (?P<start_sheet>[A-Z])(-(?P<end_sheet_n>[0-9]*)(?P<end_sheet>[A-Z]))?\`SUP\`(?P<sheet_count>[0-9]+)(\/[0-9])?\`LO\`\s*                                                                     # Main block sheets
                      ((?P<remain>[0-9]*[A-Z])\`SUP\`(?P<remain_n>[0-9]+)\`LO\`)?  # Remaining sheets
                      .*                                                           # Trail
                      '''
                      , re.VERBOSE)
    matches = prog.search(f)
    if matches:
        if matches.group("cover_sheet"):
            cover_sheet = int(matches.group("cover_sheet"))
        else:
            cover_sheet = 0
        start_sheet = matches.group("start_sheet")
        end_sheet = matches.group("end_sheet")
        if matches.group("end_sheet_n"):
            end_sheet_n = int(matches.group("end_sheet_n"))
        else:
            end_sheet_n = 1
        sheet_count = int(matches.group("sheet_count"))
        remain_sheet = matches.group("remain")
        if matches.group("remain_n"):
            remain_n = int(matches.group("remain_n"))
        else:
            remain_n = 0
        if matches.group("pren"):
            pren = int(matches.group("pren"))
        else:
            pren = 0
    else:
        print "Regexp does not recognise this formula!"
        print
        continue
    print start_sheet, end_sheet
    sheets = pren + ((end_sheet_n - 1) * len(g) + g[end_sheet] - g[start_sheet] + 1) * sheet_count + remain_n
    pages = sheets * 2
    #print pren, " + ((", end_sheet_n, "- 1 ) * ", len(g)," + ", g[end_sheet], " - ", g[start_sheet], " + 1) *", sheet_count, " + ", remain_n
    print "Sheets:", sheets
    print "Pages:", pages
    print
    
