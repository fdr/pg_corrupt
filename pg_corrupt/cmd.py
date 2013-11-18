#!/usr/bin/env python3
import argparse
import sys


def run(argv):
    parser = argparse.ArgumentParser(
        description='attempt to excise corruption from a PostgreSQL database')

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('POSTGRES_URL', help='target database URL')

    subparsers = parser.add_subparsers(title='actions', dest='action')

    scan_parser = subparsers.add_parser(
        'scan-relation',
        parents=[parent_parser],
        help='attempt to find bad tuples in a relation')
    scan_parser.add_argument('RELATION', help='a relation name to scan.')
    scan_parser.add_argument('--excise',
                             help=('remove bad tuples, reporting the '
                                   '"id" attribute.'))

    args = parser.parse_args(argv[1:])

    if args.action == 'scan-relation':
        import psycopg2

        from pg_corrupt import scan_rel
        from pg_corrupt import excise

        from pg_corrupt.quoting import quote_ident

        with psycopg2.connect(args.POSTGRES_URL) as conn:
            qrelname = quote_ident(conn, args.RELATION)

            for item, err in scan_rel.scan(args.POSTGRES_URL, qrelname):
                print('Bad tuple:', item, err)

                if args.excise:
                    print('Excising: {0}'
                          .format(excise.excise(conn, qrelname, item)))
    else:
        parser.error('No action specified')


def main():
    run(sys.argv)

if __name__ == '__main__':
    main()
