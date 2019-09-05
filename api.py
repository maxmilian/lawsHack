# -*- coding: utf-8 -*-

from flask import Flask
from py2neo import Graph,Node,Relationship

NEO4J_PASSWORD = "neo4j"
DEBUG = True

app = Flask(__name__)

@app.route('/', methods=['GET'])
def welcome():
    return "<h1>Flask Home</h1>"

@app.route('/rest/count_node', methods=['GET'])
def count_node():
    graph = Graph("http://localhost:7474/db/data/", password=NEO4J_PASSWORD)
    result = graph.evaluate("MATCH (n) RETURN count(n)")
    return {"count": result}

@app.route('/rest/count_relation', methods=['GET'])
def count_relation():
    graph = Graph("http://localhost:7474/db/data/", password=NEO4J_PASSWORD)
    result = graph.evaluate("MATCH ()-->() RETURN count(*)")
    return {"count": result}

if __name__ == '__main__':
    app.run(debug=DEBUG)
