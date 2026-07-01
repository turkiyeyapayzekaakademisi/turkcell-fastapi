import sqlite3
from pathlib import Path

DB_PATH = Path("courses.db")

def create_database():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        DROP TABLE IF EXISTS courses
        """
    )

    cursor.execute(
        """
        CREATE TABLE courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        level TEXT NOT NULL CHECK(level IN ('beginner', 'intermediate', 'advanced')),
        price REAL NOT NULL CHECK(price >= 0),
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """

    )

    sample_courses = [
        (
            "Yapay Zeka için Python",
            "Yapay zeka ve veri bilimi için Python temelleri",
            "beginner",
            250
        ),
        (
            "Veri Bilimi",
            "Pandas, NumPy, veri analizi ve görselleştirme",
            "intermediate",
            350
        ),
        (
            "Makine Öğrenmesi",
            "Scikit-learn ile makine öğrenmesi modelleri",
            "intermediate",
            450
        )
    ]

    cursor.executemany(
        """
        INSERT INTO courses (title, description, level, price)
        VALUES (?, ?, ?, ?)
        """,sample_courses
    )

    conn.commit()
    conn.close()

    print("veri tabanı başarıyla oluşturuldu.")

if __name__ == "__main__":
    create_database()