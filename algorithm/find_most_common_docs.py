
from psycopg2.extensions import connection


def find_most_common_docs(
    vectors: list[list[float]],
    n_closest: int,
    conn,
    vec_length: int,
    lang_to_exclude: str | None = None,
) -> list:
    """
    Function to find the most common document titles grouped by language closest to a list of vectors.

    vectors: list[list[float]] - A list of vectors to compare with the database embeddings.
    n_closest: int - The number of closest sentences to consider for each vector.
    conn: connection - Database connection object.
    vec_length: int - Length of each vector.
    lang_to_exclude: str | None - Language to exclude from the results, if any.
    
    Returns:
        A list of the most common document titles grouped by language closest to the input vectors.
    """
    # Validate input vectors
    print("Validating input vectors...")
    if not all(len(vector) == vec_length for vector in vectors):
        raise ValueError("All vectors must have the specified length.")

    if not all(isinstance(vector, list) and all(isinstance(v, float) for v in vector) for vector in vectors):
        raise ValueError("Each vector must be a list of floats.")
    print("Input vectors validation passed.")

    # Prepare the WHERE clause and query parameters
    print("Preparing query parameters and WHERE clause...")
    lang_condition = "AND doc_language != %s" if lang_to_exclude else ""
    query_params = [f'[{", ".join(map(str, vector))}]' for vector in vectors]
    if lang_to_exclude:
        query_params.append(lang_to_exclude)
    query_params.append(n_closest)

    vectors_string = "\n".join(["%s::vector," for _ in range(len(vectors))])


    # Construct the SQL query
    query = f"""
        WITH input_vectors AS (
        {vectors_string}
        ),
        closest_matches AS (
            SELECT
                e.doc_title,
                e.doc_langauge AS doc_language,
                e.sentence,
                e.index_in_doc,
                e.embedding <=> iv.vector::vector AS cosine_distance
            FROM embeddings e,
                 input_vectors iv
            WHERE e.embedding <=> iv.vector IS NOT NULL
            {lang_condition}
            ORDER BY iv.vector, cosine_distance ASC
            LIMIT %s
        )
        SELECT
            c.doc_title,
            c.doc_language,
            COUNT(*) AS occurrences
        FROM closest_matches c
        GROUP BY c.doc_title, c.doc_language
        ORDER BY occurrences DESC;
    """
    print("Query constructed successfully.")

    try:
        # Execute the query
        print("Executing the query...")
        cur = conn.cursor()
        cur.execute(query, query_params)
        rows = cur.fetchall()
        print(f"Query executed successfully. Rows fetched: {len(rows)}")
    except Exception as e:
        print(f"Unexpected exception when querying the database: {e}")
        rows = []
    finally:
        print("Closing the database cursor.")
        cur.close()

    return rows
