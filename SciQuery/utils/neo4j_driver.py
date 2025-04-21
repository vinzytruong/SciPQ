from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

class Neo4jConnection:
    def __init__(self):
        self.driver = None
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "12345678")

    def connect(self):
        if self.driver is None:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        return self

    def close(self):
        if self.driver:
            self.driver.close()
            self.driver = None

    def query(self, query, parameters=None):
        if self.driver is None:
            self.connect()
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record for record in result]