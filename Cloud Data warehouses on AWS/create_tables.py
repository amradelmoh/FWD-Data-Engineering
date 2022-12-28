import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries

"""
Drops all tables in the database using the drop table queries in drop_table_queries.
:param cur: database cursor
:param conn: database connector
"""
def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

"""
Creates all tables in the database using the create table queries in create_table_queries.
:param cur: database cursor
:param conn: database connector
"""
def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

"""
Reads the database and cluster configuration from dwh.cfg.
Connects to the database, drops all existing tables, and creates new tables using the queries in drop_table_queries and create_table_queries.
"""
        
def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()