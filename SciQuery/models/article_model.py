from utils.neo4j_driver import Neo4jConnection
import uuid

class ArticleModel:
    def __init__(self):
        self.neo4j = Neo4jConnection().connect()

    def create_article(self, title, content, author_ids, field_id, type):
        cypher_query = """
            UNWIND $author_ids AS author_id
            MATCH (a:Author {id: author_id})
            MATCH (f:Field {id: $field_id})
            WITH collect(a) AS authors, f
            CREATE (p:Article {
                id: $id,
                title: $title,
                content: $content,
                type: $type,
                created_at: datetime()
            })
            FOREACH (author IN authors | CREATE (author)-[:WROTE]->(p))
            CREATE (p)-[:BELONGS_TO]->(f)
            RETURN p
        """
        parameters = {
            "id": str(uuid.uuid4()),
            "title": title,
            "content": content,
            "type": type,
            "author_ids": author_ids,  # Đây là danh sách (list) các author_id
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
            MATCH (p:Article)-[:BELONGS_TO]->(f:Field)
            OPTIONAL MATCH (a:Author)-[:WROTE]->(p)
            RETURN p, collect(DISTINCT a) AS authors, f
        """
        results = self.neo4j.query(cypher_query)
        return results

    def update_article(self, article_id, title, content, author_ids, field_id, type):
        cypher_query = """
            MATCH (p:Article {id: $id})
            OPTIONAL MATCH (p)-[r1:WROTE|BELONGS_TO]-()
            DELETE r1
            WITH p
            MATCH (f:Field {id: $field_id})
            SET p.title = $title, p.content = $content, p.type = $type
            CREATE (p)-[:BELONGS_TO]->(f)
            
            // Tạo mối quan hệ với các tác giả
            WITH p, f, $author_ids AS author_ids  // Pass `f` forward
            UNWIND author_ids AS author_id
            MATCH (a:Author {id: author_id})
            CREATE (a)-[:WROTE]->(p)
            
            RETURN p, COLLECT(a) AS authors, f  // Return `f` now that it's passed along
        """
        
        parameters = {
            "id": article_id,
            "title": title,
            "content": content,
            "type": type,
            "author_ids": author_ids,
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
            RETURN p, collect(a) as authors, f
        """
        results = self.neo4j.query(cypher_query, parameters={"title": title})
        return results if results else None
