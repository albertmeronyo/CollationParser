from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://ops.few.vu.nl:8890/world")
sparql.setQuery("""
PREFIX vocab: <http://stcn.data2semantics.org/vocab/resource/>

SELECT ?f
FROM <http://stcn.data2semantics.org>
WHERE {
?p rdf:type vocab:Publicatie;
   vocab:publications_kmc4060 ?f
} LIMIT 100
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for i in results["results"]["bindings"]:
    print i["f"]["value"]
