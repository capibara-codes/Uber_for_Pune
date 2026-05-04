import GraphDatabase from neo4j

class UberGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def create_trip(self, pickup_id, dropoff_id, fare):
        with self.driver.session() as session:
            session.run("""
                MERGE (p:Location {id: $pickup_id})
                MERGE (d:Location {id: $dropoff_id})
                CREATE (p)-[:TRIP {fare: $fare}]->(d)
            """, pickup_id=pickup_id, dropoff_id=dropoff_id, fare=fare)