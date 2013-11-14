import psycopg2

from pg_corrupt import scan_page
from pg_corrupt.ctid import Ctid


def test_items():
    conn = psycopg2.connect('postgres:///')
    scan_page.items(conn, 'pg_class', Ctid(0, 0))


def test_scan():
    scan_page.scan('postgres:///', 'pg_class', 0)
