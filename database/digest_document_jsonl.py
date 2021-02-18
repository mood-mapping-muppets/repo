import duckdb
import json 
import sys
import datetime
import time
from .utils import flush_rows


if __name__ == '__main__':
    conn = duckdb.connect(sys.argv[1])
    conn.begin()
    counter = 0
    rows = []

    for line in sys.stdin:
        counter += 1

        doc = json.loads(line.strip())
        
        canon_url = doc['canon_url']
        date_publish = doc['date_publish']
        language = doc['language']
        title = doc['title']
        country = doc['country']

        rows.append((counter, canon_url, date_publish, language, title, country))

        if counter % 50000 == 0:  # Commit changes every now and then
            flush_rows(conn, rows)
            conn.begin()
            print(counter)

    flush_rows(conn, rows)
    conn.commit()
    conn.close()
