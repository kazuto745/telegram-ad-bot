import sqlite3

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cooldown (
    user_id INTEGER PRIMARY KEY,
    last_post INTEGER
)
""")

conn.commit()


def get_last_post(user_id):
    cursor.execute(
        "SELECT last_post FROM cooldown WHERE user_id=?",
        (user_id,)
    )
    row = cursor.fetchone()
    return row[0] if row else None


def update_last_post(user_id, timestamp):
    cursor.execute(
        "REPLACE INTO cooldown (user_id, last_post) VALUES (?, ?)",
        (user_id, timestamp)
    )
    conn.commit()