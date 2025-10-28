from rdflib import Graph

# --- CONFIGURACIÓN ---
# 1. Carga el archivo RDF generado por Morph-KGC.
# NOTA: Asegúrate de que el archivo 'output.tttl.txt' esté en la misma ubicación que el script.
g = Graph()
g.parse("rdf/output.ttl", format="turtle")
print(f"Triples loaded: {len(g)}")

# Define los namespaces necesarios para las consultas
query_ns = {
    'ns': 'http://bcn-mobility-air.org/ontology/',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
}

# --------------------------------------------------------------------------
# CONSULTAS DE VALIDACIÓN: Usamos 'ns:name' en lugar del tradicional 'rdfs:label'
# --------------------------------------------------------------------------

# 1. Contar recursos con la propiedad ns:name (Equivalente a rdfs:label)
print("\n1. Resources with names (ns:name) defined:")
q1 = """
SELECT (COUNT(DISTINCT ?s) AS ?withName)
WHERE { ?s ns:name ?name . }
"""
for row in g.query(q1, initNs=query_ns):
    print(row)

# 2. Muestrear nombres por clase (para verificar la asignación de tipos)
print("\n2. Sample names by class (Checking ns:name assignment):")
q2 = """
SELECT ?class ?name
WHERE {
  ?s a ?class ;
     ns:name ?name .
}
LIMIT 10
"""
for row in g.query(q2, initNs=query_ns):
    print(row)

# 3. Contar individuos sin la propiedad ns:name
# Excluimos clases que por diseño (RoadSegments, Measurements, Locations) no llevan ns:name.
print("\n3. Individuals without names (Excluding Measurements and Locations):")
q3 = """
SELECT (COUNT(DISTINCT ?s) AS ?withoutName)
WHERE {
  ?s a ?class .
  FILTER NOT EXISTS { ?s ns:name ?name }
  # Excluimos recursos que NO deberían tener ns:name, según nuestra ontología
  FILTER (?class != <http://www.w3.org/2003/01/geo/wgs84_pos#Point>)
  FILTER (?class != ns:Measurement)
  FILTER (?class != ns:RoadSegment)
}
"""
for row in g.query(q3, initNs=query_ns):
    print(row)

# 4. Distribución de nombres por clase
print("\n4. Name distribution by class (Count of named entities):")
q4 = """
SELECT ?class (COUNT(DISTINCT ?s) AS ?count)
WHERE {
  ?s a ?class ;
     ns:name ?name .
}
GROUP BY ?class
ORDER BY DESC(?count)
"""
for row in g.query(q4, initNs=query_ns):
    print(row)

# 5. Comprobar legibilidad del nombre (buscando una cadena común, 'Sant')
print("\n5. Sample names containing 'Sant' (Readability check):")
q5 = """
SELECT ?s ?name
WHERE {
  ?s ns:name ?name .
  FILTER(CONTAINS(LCASE(STR(?name)), "sant"))
}
LIMIT 5
"""
for row in g.query(q5, initNs=query_ns):
    print(row)