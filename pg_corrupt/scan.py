import subprocess
import tempfile


class Ctid:
    def __init__(self, page, item):
        self.page = page
        self.item = item

    @classmethod
    def parse(cls, string):
        page, item = [int(x) for x in string.strip(b'()\n').split(b',')]
        return cls(page, item)

    def __str__(self):
        return '({0}, {1})'.format(self.page, self.item)

    def next_page(self):
        return self.__class__(self.page + 1, 0)

    def next_item(self):
        return self.__class__(self.page, self.item + 1)


def make_copy_statement(relname, ctid):
    return ("COPY (SELECT ctid, * FROM {0} WHERE ctid >= '{1}') TO STDOUT "
            "WITH CSV DELIMITER '|'"
            .format(relname, ctid))


def last_gettable_tup(postgres_url, relname, ctid):
    copy_stmt = make_copy_statement(relname, ctid)

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

    return Ctid.parse(stdout) if stdout else ctid, error


def scan_loop(postgres_url, relname):
    err = None
    ctid = Ctid(0, 0)

    while True:
        ctid, err = last_gettable_tup(postgres_url, relname, ctid)

        if err is None:
            return

        ctid = ctid.next_item()
        yield ctid, err
        ctid = ctid.next_page()


def scan(postgres_url, relname):
    for ctid, err in scan_loop(postgres_url, relname):
        print(ctid, err)
