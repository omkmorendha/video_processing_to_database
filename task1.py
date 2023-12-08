import cv2
import json
import sqlite3
import os
from datetime import datetime
from config import VIDEO_SOURCE, FPS, OUTPUT_IMAGE_PATH, OUTPUT_JSON_PATH, DATABASE_NAME, VIDEO_DURATION_SECONDS

class VideoAnalyticsPipeline:
    def __init__(self):
        self.cap = cv2.VideoCapture(VIDEO_SOURCE)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.current_frame = 0
        self.batch_id = 1
        self.frames_per_batch = int(FPS * VIDEO_DURATION_SECONDS)

        # Database setup
        self.connection = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.connection.cursor()

        # Create a table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS frame_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                camera_id INTEGER,
                frame_id INTEGER,
                geo_location TEXT,
                image_path TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

    def process_frame(self, frame):
        # Extract relevant information from the frame
        frame_info = {
            "camera_id": 1,  # Example camera ID
            "frame_id": self.current_frame,
            "geo_location": "your_geo_location",
            "image_path": f"{OUTPUT_IMAGE_PATH}frame_{self.current_frame}.jpg"
        }

        # Write the frame as an image file (every second)
        if self.current_frame % FPS == 0:
            cv2.imwrite(frame_info["image_path"], frame)

        # Write frame information to the database
        self.cursor.execute('''
            INSERT INTO frame_info (camera_id, frame_id, geo_location, image_path)
            VALUES (?, ?, ?, ?)
        ''', (frame_info["camera_id"], frame_info["frame_id"], frame_info["geo_location"], frame_info["image_path"]))

        return frame_info

    def run(self):
        while True:
            ret, frame = self.cap.read()

            if not ret:
                break

            frame_info = self.process_frame(frame)
            self.current_frame += 1

            # Check if it's time to create a batch
            if self.current_frame % self.frames_per_batch == 0 or self.current_frame == self.frame_count:
                self.create_batch(frame_info)

        self.cap.release()
        self.connection.commit()
        self.connection.close()

    def create_batch(self, last_frame_info):
        batch_info = {
            "batch_id": self.batch_id,
            "starting_frame_id": self.current_frame - self.frames_per_batch,
            "ending_frame_id": last_frame_info["frame_id"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Save batch information to JSON file
        with open(OUTPUT_JSON_PATH, "a") as json_file:
            json.dump(batch_info, json_file, indent=2)
            json_file.write("\n")  # Add a newline for each batch

        self.batch_id += 1

if __name__ == "__main__":
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_IMAGE_PATH, exist_ok=True)

    # Run the video analytics pipeline
    pipeline = VideoAnalyticsPipeline()
    pipeline.run()