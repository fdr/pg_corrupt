import psycopg2

from pg_corrupt import quoting


def test_quote_ident():
    conn = psycopg2.connect('postgres:///')
    ret = quoting.quote_ident(conn, 'needs some Quoting "')
    assert ret == '"needs some Quoting """'
