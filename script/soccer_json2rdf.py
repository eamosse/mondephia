import json
import rdflib
import glob
from rdflib import Literal, BNode, Graph
#from string import capitalize
from pprint import pprint
from rdflib.namespace import XSD

#-- namespaces declaration here -##
## ------------------------------##
RDF = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")
OWL = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = rdflib.Namespace("http://purl.org/dc/terms/")
FOAF = rdflib.Namespace("http://xmlns.com/foaf/0.1/")
ORG = rdflib.Namespace("http://www.w3.org/ns/org#")
SCHEMA = rdflib.Namespace("http://schema.org/")
LODE = rdflib.Namespace("http://linkedevents.org/ontology/")
GEO = rdflib.Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
WD = rdflib.Namespace("http://wikidata.org/entity/")



# dataset namespace
DGI = rdflib.Namespace("http://data.cdp.net/id/skos/dgi/")
SOCEVENT = rdflib.Namespace("http://data.mondeca.com/id/soccer/")
SOCONTO = rdflib.Namespace("http://data.mondeca.com/def/ftb#")


#RDF graphe preparation 
gsoccer = rdflib.ConjunctiveGraph()


# ----- opening the json file --
json_data = open('soccer-event.json')
data = json.load(json_data)

#pprint(data) # for printing the dataset 

###  -- some global settings --

features = data[u'features'] 
print (len(features))
"""
f0 = features[0]
geom = f0[u'geometry']
prop = f0[u'properties']
print (geom)
print (prop)
"""

for i in range(0,len(features)):
	ft = features[i]
	prop = ft[u'properties']
	uri = prop[u'id']
	wdid = prop[u'where:wikidata'] 
	long = prop[u'lon']
	lat = prop[u'lat']
	start = prop[u'start']
	stop = prop[u'stop']
	bn = BNode()
	bt = BNode()
	gsoccer.add((SOCEVENT[uri], RDF["type"], SOCONTO["FootballMatch"]))
	#gsoccer.add((SOCEVENT[uri], DCT["title"], Literal(prop[u'label'], lang=u'fr')))
	gsoccer.add((SOCEVENT[uri], RDF["type"], LODE["Event"]))
	#gsoccer.add((SOCEVENT[uri], LODE["atPlace"], WD[wdid]))
	"""
	gsoccer.add((SOCEVENT[uri], LODE["inSpace"], bn))
	gsoccer.add((bn, GEO["long"], Literal(long, datatype=XSD.float)))
	gsoccer.add((bn, GEO["lat"], Literal(lat, datatype=XSD.float)))
	"""
	gsoccer.add((SOCEVENT[uri], LODE["atTime"], bt))
	gsoccer.add((bt, SOCONTO["startTime"], Literal(start)))
	gsoccer.add((bt, SOCONTO["endTime"], Literal(stop)))




json_data.close()


# ----- OUTPUT FILES -----

print ("Length of gsoccer : ", str(len(gsoccer)))
print ("Nb of tuple facts  in dataset : --->")
print(str(len(list(gsoccer.triples((None, RDF["type"], LODE["Event"]))))))
#print(gsoccer.serialize(format='n3'))
outfile = open("gsoccer.ttl", "w")
gsoccer.serialize(destination='gsoccer.ttl', format='turtle')
outfile.close()

