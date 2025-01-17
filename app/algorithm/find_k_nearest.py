from psycopg2.extensions import connection


def find_k_nearest(
    vector: list[float],
    n_articles: int,
    conn: connection,
    vec_lenght: int,
    lang_to_exclue: str | None = None,
) -> list:
    """
    Function to find K closest vectors in the database given a vector

    vector: list[float]
    k: int

    """

    if len(vector) != vec_lenght:
        raise ValueError("Vector size error")

    if not isinstance(vector, list) or not isinstance(vector[0], float):
        raise ValueError("Vector must be of type list[float]")

    if lang_to_exclue:
        where_stantment = "WHERE doc_langauge != %s"
        query_params = [str(vector), lang_to_exclue, str(n_articles)]
    else:
        where_stantment = ""
        query_params = [str(vector), str(n_articles)]

    query = f"""
        SELECT 
            doc_title, 
            doc_langauge AS doc_language,
            sentence, 
            index_in_doc,
            embedding <=> %s as cosine_distance
        FROM embeddings
        {where_stantment}
        ORDER BY cosine_distance
        LIMIT %s 
    """

    try:
        cur = conn.cursor()
        cur.execute(query, query_params)
        rows = cur.fetchall()
    except Exception as e:
        print(f"Unexpected exception when quering the database: {e}")
    finally:
        cur.close()

    return rows
