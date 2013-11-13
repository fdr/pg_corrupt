def quote_ident(conn, ident):
    with conn.cursor() as cur:
        cur.execute("SELECT quote_ident(%s)", (ident,))
        return cur.fetchone()[0]
