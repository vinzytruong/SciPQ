from utils.neo4j_driver import Neo4jConnection
import uuid

class AuthorModel:
    def __init__(self):
        self.neo4j = Neo4jConnection().connect()

    def create_author(self, name):
        cypher_query = """
            CREATE (a:Author {id: $id, name: $name})
            RETURN a
        """
        parameters = {"id": str(uuid.uuid4()), "name": name}
        result = self.neo4j.query(cypher_query, parameters)
        return result[0] if result else None
    
    def get_all_authors(self):
        cypher_query = """
            MATCH (f:Author)
            RETURN f
        """
        result = self.neo4j.query(cypher_query)
        return result
    
    def get_author(self, author_id):
        cypher_query = """
            MATCH (a:Author {id: $author_id})
            RETURN a
        """
        result = self.neo4j.query(cypher_query, parameters={"author_id": author_id})
        return result[0] if result else None

    def get_author_by_id(self, author_id):
        # This method fetches the author by their ID
        return self.get_author(author_id)

    def update_author(self, author_id, name):
        cypher_query = """
            MATCH (a:Author {id: $id})
            SET a.name = $name
            RETURN a
        """
        parameters = {"id": author_id, "name": name}
        result = self.neo4j.query(cypher_query, parameters)
        return result[0] if result else None

    def delete_author(self, author_id):
        cypher_query = """
            MATCH (a:Author {id: $id})
            DETACH DELETE a
        """
        self.neo4j.query(cypher_query, parameters={"id": author_id})

    def get_authors_by_similar_name(self, name):
        cypher_query = """
            MATCH (a:Author)
            WHERE a.name CONTAINS $name
            RETURN a
        """
        results = self.neo4j.query(cypher_query, parameters={"name": name})
        return results if results else None
