
# Video Processing using SQLite

This repository contains a Python implementation of a real-time video analytics pipeline. The pipeline performs frame processing, data storage, and batch creation based on user-provided timestamps and durations. The code includes features such as concurrency for frame processing, error handling, and logging mechanisms.

There were two tasks that this was intended for:

1. Write Python code for a real-time video analytics pipeline that performs the following tasks (For any configurations related tasks create a python config file and must create a SQL Database for storing information)

- Video Stream Ingestion
- Frame Processing
- Batching

2. Write a user driven python program that accepts,

- TIMESTAMP
- DURATION OF THE VIDEO FILE from the user.

Based on the above information, iterate through the batch information in the Database. Create a metadata out of it which will be helpful in gathering the frame information from the json file.
Once the necessary frames are gathered convert them to a mp4 file and present them to the user.

## Set up
1. Install OpenCV-2 python 
```
pip install opencv-python
```
2. Set up the video path using the **config.py** file.
```
VIDEO_SOURCE = "video.mp4"
```
3. To run task1.py use
```
python3 task1.py
```
4. TO run task2.py use
```
python3 task1.py
```

## Output

To run and test this code I used the [Dune 2 Trailer](https://www.youtube.com/watch?v=GMF7wbhBJKY) that I download from YouTube:

![image](https://github.com/omkmorendha/video_processing_to_database/assets/17925053/201c343b-9cd0-4a40-8a28-797aa1bdd580)


After running the task1.py file I got an output.json file, video_analytics.db, video_analytics.log and an output folder containing a frame taken from the video each second.

![image](https://github.com/omkmorendha/video_processing_to_database/assets/17925053/9558a77d-7cc9-42a5-be17-8488e38c5f2a)
![image](https://github.com/omkmorendha/video_processing_to_database/assets/17925053/83d2212d-9326-4143-b9e7-9b8e3074ce9c)
