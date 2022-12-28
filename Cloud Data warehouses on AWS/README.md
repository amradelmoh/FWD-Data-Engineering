Sparkify Song Play Analysis Database
====================================

Purpose
-------

The purpose of this database is to support the analytical goals of Sparkify, a startup that provides a music streaming service. The database will be used to store and analyze data on song plays, which will allow Sparkify to gain insights on user listening habits and preferences.

Database Schema Design
----------------------

### Fact Table

| Table Name | Description |
| --- | --- |
| `songplays` | Contains records of song plays from the event data, including the start time of the song play, the user who played the song, and the song and artist that were played |

### Dimension Tables

| Table Name | Description |
| --- | --- |
| `staging_events` | Stating table for event data |
| `staging_songs` | Staging table for song data |
| `users` | Contains information on the users of the music streaming service, including their first and last names, gender, and subscription level |
| `songs` | Includes data on the songs in the music database, such as the song's title, artist, and duration |
| `artists` | Contains information on the artists in the music database, including their name and location |
| `time` | Contains timestamps of the records in the `songplays` table, broken down into specific units such as the hour, day, week, month, and year |

## Project instructions
1. Setup a redshift cluster on AWS and insert the connection details in `dwh.cfg`.
2. Create the needed the database structure by executing `create_tables.py`.
3. Process the data from the configured S3 data sources by `executing etl.py`.


ETL Pipeline
------------

1.  Load data from S3 into staging tables on Redshift
2.  Process data from the staging tables into the analytics tables

| Script | Description |
| --- | --- |
| `create_tables.py` | Sets up the necessary tables in Redshift |
| `etl.py` | Handles the ETL process |
| `sql_queries.py` | Contains the SQL statements for creating and dropping tables, as well as for inserting data into the tables |

## Example queries

* Find all users at a certain location: ```SELECT DISTINCT users.user_id FROM users JOIN songplays ON songplays.user_id = users.user_id WHERE songplays.location = <LOCATION>```
* Find all songs by a given artist: ```SELECT songs.song_id FROM songs JOIN artists ON songs.artist_id = artists.artist_id WHERE artist.name = <ARTIST>``

## Conclusion

Overall, the design of this database and ETL pipeline will allow Sparkify to effectively store and analyze data on song plays, enabling them to gain insights on user listening habits and preferences, and ultimately improve their music streaming service.