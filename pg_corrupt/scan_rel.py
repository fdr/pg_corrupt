import subprocess
import tempfile

from pg_corrupt.ctid import Ctid


def make_copy_statement(relname, tid):
    return ("COPY (SELECT ctid, * FROM {0} WHERE ctid >= {1}) TO STDOUT "
            "WITH CSV DELIMITER '|'"
            .format(relname, tid))


def last_gettable_tup(postgres_url, relname, tid):
    copy_stmt = make_copy_statement(relname, tid)

    with tempfile.NamedTemporaryFile() as tf:
        psql = subprocess.Popen(['psql', '-c', copy_stmt, postgres_url],
                                stdout=subprocess.PIPE, stderr=tf)
        tail = subprocess.Popen(['tail', '-n1'], stdin=psql.stdout,
                                stdout=subprocess.PIPE)
        cut = subprocess.Popen(['cut', '-d|', '-f1'], stdin=tail.stdout,
                               stdout=subprocess.PIPE)

        stdout = cut.communicate()[0]

        psql.wait()
        if psql.returncode == 0:
            error = None
        else:
            tf.seek(0)
            error = tf.read()

    return Ctid.parse(stdout) if stdout else tid, error


def scan_rel(postgres_url, relname):
    err = None
    ctid = Ctid(0, 0)

    while True:
        tid, err = last_gettable_tup(postgres_url, relname, ctid)

        if err is None:
            return

        tid = tid.next_item()
        yield tid, err
        tid = tid.next_page()


def scan(postgres_url, relname):
    for tid, err in scan_rel(postgres_url, relname):
        print(tid, err)
