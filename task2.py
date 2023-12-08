import json
import cv2
import sqlite3
import os
from datetime import datetime
from config import DATABASE_NAME, OUTPUT_JSON_PATH


def gather_frames_and_create_video(timestamp, duration):
    try:
        # Connect Database
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        # Query batch information based on timestamp and duration
        cursor.execute(
            """
            SELECT *
            FROM batch_info
            WHERE timestamp >= ? AND timestamp <= ?
        """,
            (timestamp, timestamp + duration),
        )

        batches = cursor.fetchall()

        if not batches:
            print("No batches found for the specified timestamp and duration.")
            return

        # Create list to store frame information
        frame_info_list = []

        # Iterate through batches and gather frame information
        for batch in batches:
            starting_frame_id = batch[1]
            ending_frame_id = batch[2]

            cursor.execute(
                """
                SELECT *
                FROM frame_info
                WHERE frame_id >= ? AND frame_id <= ?
            """,
                (starting_frame_id, ending_frame_id),
            )

            frame_info_list.extend(cursor.fetchall())

        # Create a metadata file for gathered frame information
        metadata = {
            "timestamp": timestamp,
            "duration": duration,
            "frame_info": frame_info_list,
        }

        metadata_filename = f"metadata_{timestamp}.json"
        with open(metadata_filename, "w") as metadata_file:
            json.dump(metadata, metadata_file, indent=2)

        # Create a video file from the gathered frames
        create_video_from_frames(frame_info_list)

        print(
            f"Metadata file '{metadata_filename}' and video file created successfully."
        )

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the database connection
        if connection:
            connection.close()


def create_video_from_frames(frame_info_list):
    # Create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Use appropriate codec
    video_filename = "output_video.mp4"
    video_writer = cv2.VideoWriter(
        video_filename, fourcc, 25, (640, 480)
    )  # Adjust parameters as needed

    try:
        for frame_info in frame_info_list:
            image_path = frame_info[4]
            frame = cv2.imread(image_path)
            video_writer.write(frame)

    except Exception as e:
        print(f"Error creating video: {str(e)}")

    finally:
        # Release the VideoWriter
        video_writer.release()


if __name__ == "__main__":
    # Get user input for TIMESTAMP and DURATION
    timestamp_str = input("Enter TIMESTAMP (YYYY-MM-DD HH:MM:SS): ")
    duration_str = input("Enter DURATION (in seconds): ")

    try:
        # Convert user input to datetime and duration
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        duration = int(duration_str)

        # Call the main function
        gather_frames_and_create_video(timestamp, duration)

    except ValueError as ve:
        print(f"Invalid input format. {ve}")
