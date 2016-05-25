import cStringIO, csv, codecs


class UnicodeDictWriter(object):

    def __init__(
        self,
        stream,
        fieldnames,
        dialect=csv.excel,
        encoding="utf-8",
        **kwds
    ):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(
            self.queue, fieldnames,
            dialect=dialect, **kwds
        )
        self.stream = stream
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, D):
        try:
            self.writer.writerow(
                {
                    k: v.encode("utf-8", errors="replace") if isinstance(
                        v, unicode
                    ) else v
                    for k, v in D.items()
                }
            )
        except UnicodeEncodeError:
            pass
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for D in rows:
            self.writerow(D)

    def writeheader(self):
        self.writer.writeheader()
