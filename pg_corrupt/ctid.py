import psycopg2


class Ctid:
    def __init__(self, page, item):
        self.page = page
        self.item = item

    @classmethod
    def parse(cls, string):
        page, item = [int(x) for x in string.strip(b'()\n').split(b',')]
        return cls(page, item)

    def __str__(self):
        return "'({0}, {1})'".format(self.page, self.item)

    def next_page(self):
        return self.__class__(self.page + 1, 0)

    def next_item(self):
        return self.__class__(self.page, self.item + 1)

psycopg2.extensions.register_adapter(Ctid, psycopg2.extensions.AsIs)
