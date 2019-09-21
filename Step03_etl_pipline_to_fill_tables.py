import os
import glob
import psycopg2
import pandas as pd
from Step02_prepare_query import *





def process_song_file(cur, filepath):
    """
    It performs ETL on the song_data to create the ["songs"] / ["artists"] dimension tables by:  
     - reading from the song_data, 
     - extracting the data for the first song in the list, 
     - inserting it into the ["songs"] / ["artists"] tables through executing the "song_table_insert" and "artsit_table_insert" queries. 
    
    *arguments:
     - cur: set cursor for excuting queries. 
     - filepath: takes path of the song_data file.
     
    Returns:
     - None
    """
    # open song file
    df_song = pd.read_json(filepath, lines = True)

    # insert song record
    song_data = list(df_song[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0])
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data =list(df_song[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    It performs ETL on the log_data to create the ["time"] / ["users"] dimesion tables as well as the ["songplays"] fact table by:
     - Extracting data from the log_data file and loads into the ["users"] and ["songplays"] tables. 
     - Data for the ["time"] table, however needs to be transformed to get a decent format from <timestamp> to <datetime> using pd.to_datetime.
      
    *arguments:
     - cur: cursor to execute queries. 
     - filepath: where log_data is located. 
     
    Returns:
     - None
    """
    # open log file
    df_log = pd.read_json(filepath, lines = True)

    # filter by NextSong action !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    df_what = df_log.loc[df_log['page'] == 'NextSong']
    df_t = df_what['ts']


    
    
    
    
    ################################################################ for [time]
    # 1. convert timestamp column to datetime
    t = pd.to_datetime(df_t, unit = 'ms')
    
    t_stamp = list(t.dt.time.values)
    hour = list(t.dt.hour.values)
    day = list(t.dt.day.values)
    weekofyear = list(t.dt.week.values)
    weekday = list(t.dt.weekday.values)
    month = list(t.dt.month.values)
    year = list(t.dt.year.values)
    time_df = pd.DataFrame({'start_time': t_stamp, 'hour': hour, 'day': day, 'week': weekofyear, 'month': month, 'year': year, 'weekday': weekday})
    
    
    # 2. insert time records
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

        
          
              
    
    ################################################################ for [users]
    # 1. load user table
    user_df = df_what[['userId', 'firstName', 'lastName', 'gender', 'level']]
    
    user_df.dropna(inplace =True)
    
    
    # 2. insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, list(row))



    ############################################################ for [songpalys]
    # FINALY insert songplay records
    for i, row in df_what.iterrows():
        
        # get songid and artistid from song and artist tables
        results = cur.execute(song_select, (row.song, row.artist, row.length))
        songid, artistid = results if results else None, None

        # insert songplay record
        songplay_data = [row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)


################################################### instead of "get_files()"
def process_data(cur, conn, filepath, func):
    """
    it get all the files from the directory, and finds the number of files found in path
    and process them by allowing the execution of "process_song_file()" and "process_log_file()".   
    
    *arguments:
        cur: cursor for executing queries
        con: establish connection with the sparkify database
        filepath: provides the path for the files to be processed (soang_data, log_data)
        func: this argument calls and allows for the execution of either the process_song_file or process_log_file functions. 
        
    Returns:
     - None
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f)) ##so we have .. "all_files"

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, start=1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))
################################################################################

'''It feeds the [filepaths]'''

def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()


