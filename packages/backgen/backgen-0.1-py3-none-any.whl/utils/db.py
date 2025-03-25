def analyze_performance(cursor):
    """Analyse des performances des requêtes SQL et des index."""
    cursor.execute("EXPLAIN ANALYZE SELECT * FROM your_table LIMIT 10;")
    result = cursor.fetchall()
    print("Performance de la requête SQL : ", result)

    cursor.execute("SELECT * FROM pg_indexes WHERE tablename = 'your_table';")
    indexes = cursor.fetchall()
    print("Index de la table : ", indexes)
