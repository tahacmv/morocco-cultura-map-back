from flask import Flask, request, jsonify
import rdflib
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Load your RDF data
RDF_DATA = 'B:\\work\\CultureMarocaineBack\\cultureFinal.ttl'

g = rdflib.Graph()
g.parse(RDF_DATA, format=rdflib.util.guess_format(RDF_DATA))

def get_local_name(uri):
    # Extracts the portion after the last '#' or '/' in a URI
    return uri.split('#')[-1] if '#' in uri else uri.split('/')[-1]

# Example endpoint for querying "Legume"
@app.route('/query-legume', methods=['GET'])
def query_legume():
    query_str = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ont: <http://www.semanticweb.org/tmmot/ontologies/2024/1/untitled-ontology-29#>

SELECT ?legume
WHERE {
  ?legume rdf:type ont:Legume .
}
    """
    
    print(query_str)

    qres = g.query(query_str)

    results = [
        get_local_name(str(row[0]))
     for row in qres]
    
    return results


@app.route('/query-viande', methods=['GET'])
def query_viande():
    
    query_str = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ont: <http://www.semanticweb.org/tmmot/ontologies/2024/1/untitled-ontology-29#>

SELECT ?item
WHERE {
  {
    ?item rdf:type ont:Viande .
  } UNION {
    ?item rdf:type ont:Poisson .
  }
}
    """
    
    print(query_str)

    qres = g.query(query_str)

    results = [
        get_local_name(str(row[0]))
     for row in qres]
    
    return results

@app.route('/query-fruit-sec', methods=['GET'])
def queryfruitsec():
    
    query_str = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ont: <http://www.semanticweb.org/tmmot/ontologies/2024/1/untitled-ontology-29#>

SELECT ?item
WHERE {
  ?item rdf:type ont:FruitSec .
}
    """
    
    print(query_str)

    qres = g.query(query_str)

    results = [
        get_local_name(str(row[0]))
     for row in qres]
    
    return results

@app.route('/query-pate', methods=['GET'])
def querypate():
    
    query_str = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ont: <http://www.semanticweb.org/tmmot/ontologies/2024/1/untitled-ontology-29#>

SELECT ?item
WHERE {
  ?item rdf:type ont:Pate .
}
    """
    
    print(query_str)

    qres = g.query(query_str)

    results = [
        get_local_name(str(row[0]))
     for row in qres]
    
    return results


@app.route('/query-epice', methods=['GET'])
def queryepice():
    
    query_str = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ont: <http://www.semanticweb.org/tmmot/ontologies/2024/1/untitled-ontology-29#>

SELECT ?item
WHERE {
  ?item rdf:type ont:Epice .
}
    """
    
    print(query_str)

    qres = g.query(query_str)

    results = [
        get_local_name(str(row[0]))
     for row in qres]
    
    return results

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json  # Get JSON data sent from React app

    # Base part of the query
    base_query = """
    PREFIX ont: <http://www.semanticweb.org/tmmot/ontologies/2024/1/untitled-ontology-29#>
    
    SELECT ?plat
    WHERE {
      ?plat rdf:type ont:Plat .
    """
    print(type(data.get('question1')))
    
    # Dynamically add conditions based on the input
    if data.get('question1'):
        if len(data.get('question1')) > 0: 
            Viandes  = data['question1']
            Viandes_str = ' '.join('ont:%s ' % viande for viande in Viandes)
            viande_condition = """?plat ont:hasViande ?viande \n.VALUES ?viande {%s}"""%Viandes_str
            base_query += viande_condition

    if  data.get('question2'):
        if len(data.get('question2')) > 0:
            legumes = data['question2']
            legumes_str = ' '.join('ont:%s ' % legume for legume in legumes)
            legume_conditions = """?plat ont:hasLegume ?legume \n.VALUES ?legume {%s}"""%legumes_str
            base_query += legume_conditions

    if data.get('question3') :
        if len(data.get('question3')) > 0:
            fruits_sec = data['question3']
            fruits_sec_str = ' '.join('ont:%s ' % fruit_sec for fruit_sec in fruits_sec)
            fruitSec_conditions = """?plat ont:hasFruit ?fruit \n.VALUES ?fruit {%s}"""%fruits_sec_str
            base_query += fruitSec_conditions

    if 'question4' in data and data['question4']:  # Semoule
        # Add condition directly if Semoule is true, adjust as necessary
        base_query += "  {?plat ont:hasObjetComestible ont:Semoule .}"

    if data.get('question5'):
        if len(data.get('question5')) > 0:
            epices = data['question5']
            epices_str = ' '.join('ont:%s ' % epice for epice in epices)
            epice_conditions = """?plat ont:hasEpice ?epice \n.VALUES ?epice {%s}"""%epices_str
            base_query += epice_conditions

    if 'question6' in data and data['question6']:
        if len(data['question6']) > 0:
            pates = data['question6']
            pates_str = ' '.join('ont:%s ' % pate for pate in pates)
            pates_conditions = """?plat ont:hasPate ?pate \n.VALUES ?pate {%s}"""%pates_str
            base_query += pates_conditions

    # Close the WHERE clause
    base_query += "\n}"

    # For demonstration, print the query. In practice, you'd execute this query against your SPARQL endpoint.
    print(base_query)
    
    qres = g.query(base_query)

    results = [
        get_local_name(str(row[0]))
     for row in qres]
    
    return results

if __name__ == '__main__':
    app.run(debug=True)
