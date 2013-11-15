import os
import psycopg2

from pg_corrupt import scan_rel
from pg_corrupt.ctid import Ctid


def test_make_copy_statement():
    conn = psycopg2.connect('postgres:///')
    stmt = scan_rel.make_copy_statement('pg_class', Ctid(0, 0))

    with conn.cursor() as cur, open(os.devnull, 'w') as bitbucket:
        cur.copy_expert(stmt, bitbucket)
