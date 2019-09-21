
# Data Modeling with Postgres

## Purpose and Analytical goals


Sparkify is a startup company with a music streaming app. They have been collecting data on songs and user activity on this new app. They don't have an eacy way to query their data which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.  

The purpose of this database is to optimize queries on song play analysisminorder to meet their analytical goals which involve understanding what songs users are listening to. 
Subsequently, the ETL pipeline needs to be built to load the Songs and Song play log data into the created database (`sparkify`) which will be used by the analytics team for further analysis. 


## Schema for song play analysis

using the song and log datasets, we created a **Star schema** for our queries on song play analysis. This schema makes queries easier and provides fast aggregations . 
This schema included the following tables;

### Fact table

1. **songplays**: records in log data associated with song plays i.e. records with page NextSong
    * songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension tables

They are used to categorize our facts and measures to enable us better answer the business quesitons. 

2. **users**: users in the app
    * user_id, first_name, last_name, gender, level
   
   
3. **songs**: songs in music database
    * song_id, title, artist_id, year, duration
 
 
4. **artists**: artists in music database
    * artist_id, name, location, lattitude, longitude
    
    
5. **time**: timestamps of records in **songplays** broken down into specific units
    * start_time, hour, day, week, month, year, weekday

### ETL pipeline

The ***Step01_create_tables.py*** creates our database and tables based on our queries found in ***Step02_prepare_query.py***. We rerun it each time to reset our tables before running ***Step03_etl_pipline_to_fill_tables.py*** or ***etl_process.ipynb***.

We begin by developing an ETL proecess for each table in ***etl_process.ipynb*** notebook. These results are tested using ***test.ipynb*** to ensure successful creation and insertion of records to the various tables.
 
The **Step03_etl_pipline_to_fill_tables.py** reads and processes files from the song_data and log_data, it then loads them into the respective tables.
1. **Extraction**: data from 2 JSON files (song and log) are extracetd. These files are accessed using the read_json(). 


2. **Transformation**: In this project, the data for the start_time in song play has a source format of milliseconds. This data is then converted to the relevant datetime format and loading to the time table.

3. **Load**: The data extracted and transformed are loaded into the fact and dimension tables while eliminating duplicates using the PRIMARY KEY constraint and upsert logic. 

While loading the files into the database, this is done directly from either song or log JSON file for the dimension tables. However, The fact table (songplays table) takes its data from the log data, song table and artist table. This is because the log file does not specify the song_id and artist_id for each songplay.

So in order to relate the song ID and artist ID for each songplay, a combination of song title, artist name, and song duration time are used in the query below; 

    SELECT s.song_id, a.artist_id
    FROM  songs s
    JOIN artists a ON s.artist_id = a.artist_id
    WHERE s.title = %s AND a.name = %s AND s.duration = %s


