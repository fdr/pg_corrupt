import psycopg2

from pg_corrupt.ctid import Ctid
from pg_corrupt.quoting import quote_ident


def items(conn, qrelname, base_page):
    sql = ("SELECT ctid FROM {0} WHERE ctid >= %s and ctid < %s"
           .format(qrelname))
    params = (base_page, base_page.next_page())
    with conn.cursor() as cur:
        cur.execute(sql, params)
        return [t[0] for t in cur.fetchall()]


def identify_bad_ctid(conn, qrelname, text_tid):
    sql = "SELECT * FROM {0} WHERE ctid = %s".format(qrelname)
    params = (text_tid,)
    with conn.cursor() as cur:
        try:
            cur.execute(sql, params)
            cur.fetchall()
        except psycopg2.Error as e:
            conn.rollback()
            return e

    return None


def scan(postgres_url, relname, page):
    conn = psycopg2.connect(postgres_url)
    qrelname = quote_ident(conn, relname)
    base_page = Ctid(page, 0)

    for item in items(conn, qrelname, base_page):
        err = identify_bad_ctid(conn, qrelname, item)
        if err is not None:
            yield Ctid.parse(bytes(item, 'utf-8')), err
