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
   vocab:publications_kmc4060 ?f
} LIMIT 1
""")

sparql.setReturnFormat(JSON)
# results = sparql.query().convert()
results = ["A-G`SUP`12`LO` H`SUP`6`LO` (lacks H6, blank?)"]

#for r in results["results"]["bindings"]:
for r in results:
    #f = r["f"]["value"]
    f = r
    print f
    regexp = r'(?P<sheets>[A-Z](-[0-9]*[A-Z])?)\`SUP\`(?P<sheetsn>[0-9]+)\`LO\`\s*((?P<remain>[0-9]*[A-Z])\`SUP\`(?P<remainn>[0-9]+)\`LO\`)?\w*'
    matches = re.search(regexp, f)
    if matches:
        start_sheet = matches.group("sheets").split('-')[0]
        end_sheet = matches.group("sheets").split('-')[1]
        sheet_n = matches.group("sheetsn")
        remain_sheet = matches.group("remain")
        remain_n = matches.group("remainn")
    sheets = (g[end_sheet] - g[start_sheet] + 1)* int(sheet_n) + int(remain_n)
    pages = sheets * 2
    print sheets
    print pages
    
    
        
