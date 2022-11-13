import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
     ''' Process the songs files and insert data into dimension tables: songs and artists.
    :param cur: connection cursor to insert the data in DB.
    :param filepath: path/to/the/song/file.'''
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data =  df[['song_id','title','artist_id','year','duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    ''' Process the log files and insert data into dimension tables: time and users..
    :param cur: connection cursor to insert the data in DB.
    :param filepath: path/to/the/log/file.'''
    # open log file
    df = pd.read_json(filepath,lines=True)

    # filter by NextSong action
    df = df.loc[df['page']=='NextSong']

    ''' Add more time elements to a dataframe from a UNIX timestamp in milliseconds.
    :param df: pandas dataframe to add time fields.
    :param ts_field: name of the timestamp field field.
    :return: pandas dataframe with more time fields.'''
    # convert timestamp column to datetime
    df['datetime'] = pd.to_datetime(df['ts'], unit='ms')
    t = df['datetime']
    
    # insert time data records
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['day'] = df['datetime'].dt.day
    df['hour'] = df['datetime'].dt.hour
    df['weekday_name'] = df['datetime'].dt.weekday_name
    df['week'] = df['datetime'].dt.week
    time_data = ('datetime', 'hour', 'day', 'week', 'month', 'year', 'weekday_name')
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = df[['datetime', 'hour', 'day', 'week', 'month', 'year', 'weekday_name']]

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.itemInSession, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
        """
    Process all the data, either songs files or logs files
    :param cur: connection cursor to insert the data in DB.
    :param conn: connection to the database to do the commit.
    :param filepath: path/to/data/type/directory
    :param func: function to process, transform and insert into DB the data.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()