import sqlite3
import base64
from flask import g


class DatabaseManager:
    def __init__(self, db_name="mydatabase.db"):
        self.db_name = db_name

    def get_db(self):
        db = getattr(g, "_database", None)
        if db is None:
            db = g._database = sqlite3.connect(self.db_name)
        return db

    def initialize_db(self):
        try:
            with self.get_db() as db:
                db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        phone_number TEXT NOT NULL,
                        image BLOB NOT NULL
                    );
                """
                )

                initial_users = [
                    ("7165470385", self.image_to_blob("/Users/sandy/Downloads/705_IoT_Project/face_OTP_API/OwnerData/pinkuan.jpg")),
                    ("7165470136", self.image_to_blob("/Users/sandy/Downloads/705_IoT_Project/face_OTP_API/OwnerData/madhavi.jpg")),
                    ("7165479219", self.image_to_blob("/Users/sandy/Downloads/705_IoT_Project/face_OTP_API/OwnerData/sandeep.jpg"))
                    # Add more users if needed
                ]

                for user in initial_users:
                                phone_number, image_data = user
                                cursor = db.execute("SELECT 1 FROM users WHERE phone_number = ?", (phone_number,))
                                if not cursor.fetchone():  # if the data is not in the table, then insert it
                                    db.execute("INSERT INTO users (phone_number, image) VALUES (?, ?);", (phone_number, image_data))

                db.commit()
        except Exception as e:
            print(f"Error initializing the database: {e}")

    def image_to_blob(self, image_path):
        try:
            with open(image_path, "rb") as img_file:
                blob_data = img_file.read()
            return blob_data
        except Exception as e:
            print(f"Error converting image to blob: {e}")
            return None

    def insert_user(self, phone_number, image_data):
        with self.get_db() as db:
            db.execute(
                "INSERT INTO users (phone_number, image) VALUES (?, ?);",
                (phone_number, image_data),
            )
            db.commit()

    def get_all_users(self):
        with self.get_db() as db:
            cursor = db.execute("SELECT image, phone_number FROM users;")
            return cursor.fetchall()
