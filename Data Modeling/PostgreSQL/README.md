### Introduction
A company by the name of Sparkify wants to analyze the information they've been gathering on songs and user activity on their brand-new music streaming service. The analytics team is very interested in knowing which music users are listening to. They now want a simple way to query their data, which is stored in directories containing JSON logs on user activity on the app and JSON information on the songs in their app.

They want a data engineer to build tables in a Postgres database that can optimise searches for song play analysis. My responsibility is to design an ETL pipeline and database structure for this investigation.

### Data Model
I've used a star schema as my data model. Here are the tables:
#### Fact Table

**Table songplays**

| COLUMN  	| TYPE  	| CONSTRAINT  	|
|---	|---	|---	|	
|   songplay_id	| SERIAL  	|   PRIMARY KEY	| 
|   start_time	|   bigint	|   NOT NULL	| 
|   user_id	|   int	|   NOT NULL	| 
|   level	|   varchar |   	| 
|   song_id	|   varchar	|   	| 
|   artist_id	|   varchar	|   	| 
|   session_id	|   int	|   	| 
|   location	|   text	|   	| 
|   user_agent	|   text	|   	| 
 
 #### Dimensions Tables
 
 **Table users**
 
 | COLUMN  	| TYPE  	| CONSTRAINT  	|
|---	|---	|---	|	
|   user_id	| int  	|   PRIMARY KEY	| 
|   first_name	|   varchar	|  	| 
|   last_name	|   varchar	|  	| 
|   gender	|   varchar(1) |   	| 
|   level	|   varchar	|   	| 


**Table songs**

 | COLUMN  	| TYPE  	| CONSTRAINT   	|
|---	|---	|---	|	
|   song_id	| varchar  	|   PRIMARY KEY	| 
|   title	|   text	|  NOT NULL 	| 
|   artist_id	|   varchar	|   	| 
|   year	|   int |   	| 
|   duration	|   numeric	|  NOT NULL 	| 



**Table artists**

 | COLUMN  	| TYPE  	| CONSTRAINT   	|
|---	|---	|---	|	
|   artist_id	| varchar  	|   PRIMARY KEY	| 
|   name	|   varchar	|  NOT NULL 	| 
|   location	|   text	|   	| 
|   latitude	|   double precision	|   	| 
|   longitude	|   double precision |   	| 



**Table time**
 
 | COLUMN  	| TYPE  	| CONSTRAINT   	|
|---	|---	|---	|	
|   start_time	| timestamp  	|   PRIMARY KEY	| 
|   hour	|   int	|   	| 
|   day	|   int	|   	| 
|   week	|   int	|   	| 
|   month	|   int	|   	| 
|   year	|   int	|   	| 
|   weekday	|   varchar	|   	| 


### Files
#### ETL Pipeline

The ETL is in the file **etl.py** and works as follows:

1. Connecting to the database first.
2. Go through the *song* folders.
    - Add song data to the **songs** table.
    - Add artist data to the **artists** table.
3. Go through the *log* files.
    - Add the unix timestamp (ts) to the **time** table.
    - We can extract the year, day, hour, week, month, and day of the week from the field **ts**.
    - Add user data to the **users** table.
4. Add songplay records to the table "songplays." In this instance, a second select is required to retrieve the song id and artist id.
5. Cut the connection and end.
    
#### sql_queries.py

All of the database queries are contained in this file.

1. All of the DROP statements for all of the tables are contained in this file.
2. All of the CREATE clauses for each table.
3. Each and every INSERT clause for each table.
4. Use the SELECT command to retrieve the artist id and song id needed to populate the songplays table.