def excise(conn, qrelname, tid):
    with conn.cursor() as cur:
        # Assume 'id' column exists and print that for bookkeeping.
        #
        # TODO: Instead should find unique constraints and print
        # those, or try to print all attributes that are not corrupt.
        sql = 'DELETE FROM {0} WHERE ctid = %s RETURNING id'.format(qrelname)
        params = (tid,)

        cur.execute(sql, params)

        row = cur.fetchone()
        if row:
            return row[0]

        return None
