#!/usr/bin/env python3
import argparse
import sys

from pg_corrupt import scan_rel


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
    scan_parser.add_argument('RELATION', help='a relation name to scan')

    args = parser.parse_args(argv[1:])

    if args.action == 'scan-relation':
        scan_rel.scan(args.POSTGRES_URL, args.RELATION)
    else:
        parser.error('No action specified')


def main():
    run(sys.argv)

if __name__ == '__main__':
    main()
