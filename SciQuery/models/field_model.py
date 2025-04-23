from utils.neo4j_driver import Neo4jConnection
import uuid

class FieldModel:
    def __init__(self):
        self.neo4j = Neo4jConnection().connect()

    def create_field(self, name):
        cypher_query = """
            CREATE (f:Field {id: $id, name: $name})
            RETURN f
        """
        parameters = {"id": str(uuid.uuid4()), "name": name}
        result = self.neo4j.query(cypher_query, parameters)
        return result[0] if result else None
    
    def get_all_fields(self):
        cypher_query = """
            MATCH (f:Field)
            RETURN f
        """
        result = self.neo4j.query(cypher_query)
        return result
    
    def get_field(self, field_id):
        cypher_query = """
            MATCH (f:Field {id: $field_id})
            RETURN f
        """
        result = self.neo4j.query(cypher_query, parameters={"field_id": field_id})
        return result[0] if result else None

    def update_field(self, field_id, name):
        cypher_query = """
            MATCH (f:Field {id: $id})
            SET f.name = $name
            RETURN f
        """
        parameters = {"id": field_id, "name": name}
        result = self.neo4j.query(cypher_query, parameters)
        return result[0] if result else None

    def delete_field(self, field_id):
        cypher_query = """
            MATCH (f:Field {id: $id})
            DETACH DELETE f
        """
        self.neo4j.query(cypher_query, parameters={"id": field_id})

    def get_field_by_name(self, name):
        cypher_query = """
            MATCH (f:Field {name: $name})
            RETURN f
        """
        result = self.neo4j.query(cypher_query, parameters={"name": name})
        return result[0] if result else None