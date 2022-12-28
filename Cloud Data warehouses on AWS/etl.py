import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

"""
Loads data from S3 into the staging tables using the copy queries in copy_table_queries.
:param cur: database cursor
:param conn: database connector
"""
def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()

"""
Inserts data from the staging tables into the analytics tables using the insert queries in insert_table_queries.
:param cur: database cursor
:param conn: database connector
"""
def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()

"""
Connects to the database, loads data from S3 into the staging tables, and inserts data from the staging tables into the analytics tables.
Reads the database and cluster configuration from dwh.cfg.
"""
def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()