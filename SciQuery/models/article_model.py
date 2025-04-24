from utils.neo4j_driver import Neo4jConnection
import uuid

class ArticleModel:
    def __init__(self):
        self.neo4j = Neo4jConnection().connect()

    def create_article(self, title, content, author_id, field_id, type):
        cypher_query = """
            MATCH (a:Author {id: $author_id}), (f:Field {id: $field_id})
            CREATE (p:Article {id: $id, title: $title, content: $content, type: $type})
            CREATE (a)-[:WROTE]->(p)
            CREATE (p)-[:BELONGS_TO]->(f)
            RETURN p, a, f
        """
        parameters = {
            "id": str(uuid.uuid4()),
            "title": title,
            "content": content,
            "type": type,
            "author_id": author_id,
            "field_id": field_id
        }
        result = self.neo4j.query(cypher_query, parameters)
        return result[0] if result else None

    def get_article(self, article_id):
        cypher_query = """
            MATCH (p:Article {id: $article_id})
            OPTIONAL MATCH (a:Author)-[:WROTE]->(p)
            OPTIONAL MATCH (p)-[:BELONGS_TO]->(f:Field)
            RETURN p, a, f
        """
        result = self.neo4j.query(cypher_query, parameters={"article_id": article_id})
        return result[0] if result else None

    def get_all_articles(self):
        cypher_query = """
            MATCH (p:Article)
            OPTIONAL MATCH (a:Author)-[:WROTE]->(p)
            OPTIONAL MATCH (p)-[:BELONGS_TO]->(f:Field)
            RETURN p, a, f
        """
        return self.neo4j.query(cypher_query)

    def update_article(self, article_id, title, content, author_id, field_id, type):
        cypher_query = """
            MATCH (p:Article {id: $id})
            OPTIONAL MATCH (p)-[r1:WROTE|BELONGS_TO]-()
            DELETE r1
            WITH p
            MATCH (a:Author {id: $author_id}), (f:Field {id: $field_id})
            SET p.title = $title, p.content = $content, p.type = $type
            CREATE (a)-[:WROTE]->(p)
            CREATE (p)-[:BELONGS_TO]->(f)
            RETURN p, a, f
        """
        parameters = {
            "id": article_id,
            "title": title,
            "content": content,
            "type": type,
            "author_id": author_id,
            "field_id": field_id
        }
        result = self.neo4j.query(cypher_query, parameters)
        return result[0] if result else None

    def delete_article(self, article_id):
        cypher_query = """
            MATCH (p:Article {id: $id})
            DETACH DELETE p
        """
        self.neo4j.query(cypher_query, parameters={"id": article_id})

    def get_articles_by_similar_name(self, title):
        cypher_query = """
            MATCH (p:Article)
            WHERE p.title CONTAINS $title
            OPTIONAL MATCH (a:Author)-[:WROTE]->(p)
            OPTIONAL MATCH (p)-[:BELONGS_TO]->(f:Field)
            RETURN p, a, f
        """
        results = self.neo4j.query(cypher_query, parameters={"title": title})
        return results if results else None
