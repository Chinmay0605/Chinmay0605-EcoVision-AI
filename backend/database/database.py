import sqlite3
from pathlib import Path
from datetime import datetime


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "database"

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATABASE_PATH = DATABASE_DIR / "ecovision.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# CREATE TABLE
# ============================================================

def init_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS scans (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT NOT NULL,

            stored_filename TEXT NOT NULL,

            waste_type TEXT NOT NULL,

            category TEXT,

            material TEXT,

            confidence REAL,

            recyclable INTEGER,

            recommended_bin TEXT,

            disposal_instruction TEXT,

            handling_instruction TEXT,

            eco_tip TEXT,

            created_at TEXT NOT NULL

        )
        """
    )

    connection.commit()

    connection.close()


# ============================================================
# SAVE SCAN
# ============================================================

def save_scan(
    filename,
    stored_filename,
    waste_type,
    category,
    material,
    confidence,
    recyclable,
    recommended_bin,
    disposal_instruction,
    handling_instruction,
    eco_tip
):

    connection = get_connection()

    cursor = connection.cursor()

    created_at = datetime.now().isoformat(
        timespec="seconds"
    )

    cursor.execute(
        """
        INSERT INTO scans (
            filename,
            stored_filename,
            waste_type,
            category,
            material,
            confidence,
            recyclable,
            recommended_bin,
            disposal_instruction,
            handling_instruction,
            eco_tip,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            filename,
            stored_filename,
            waste_type,
            category,
            material,
            confidence,
            1 if recyclable else 0,
            recommended_bin,
            disposal_instruction,
            handling_instruction,
            eco_tip,
            created_at
        )
    )

    connection.commit()

    scan_id = cursor.lastrowid

    connection.close()

    return scan_id


# ============================================================
# GET SCAN HISTORY
# ============================================================

def get_scan_history(limit=50):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM scans
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    connection.close()

    history = []

    for row in rows:

        item = dict(row)

        item["recyclable"] = bool(
            item["recyclable"]
        )

        history.append(item)

    return history


# ============================================================
# GET STATISTICS
# ============================================================

def get_statistics():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_scans,

            SUM(
                CASE
                    WHEN recyclable = 1
                    THEN 1
                    ELSE 0
                END
            ) AS recyclable_scans,

            SUM(
                CASE
                    WHEN recyclable = 0
                    THEN 1
                    ELSE 0
                END
            ) AS non_recyclable_scans,

            AVG(confidence) AS average_confidence

        FROM scans
        """
    )

    row = cursor.fetchone()

    connection.close()

    total_scans = row["total_scans"] or 0

    recyclable_scans = row["recyclable_scans"] or 0

    non_recyclable_scans = row["non_recyclable_scans"] or 0

    average_confidence = (
        row["average_confidence"] or 0
    )

    return {
        "total_scans": total_scans,

        "recyclable_scans": recyclable_scans,

        "non_recyclable_scans": non_recyclable_scans,

        "average_confidence": round(
            average_confidence,
            2
        )
    }


# ============================================================
# DELETE ALL HISTORY
# ============================================================

def delete_all_scans():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM scans"
    )

    connection.commit()

    connection.close()

    return True

# ============================================================
# DELETE SPECIFIC SCAN HISTORY
# ============================================================
def delete_scan(scan_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM scans WHERE id = ?",
        (scan_id,)
    )

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted