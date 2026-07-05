from datetime import datetime
from Database import connect_db



def mark_attendance(name):

    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%Y-%m-%d")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM attendance WHERE name=? AND date=?",
        (name, current_date)
    
)

    record = cursor.fetchone()

    if record:
        conn.close()
        return f"{name} already marked today"

    cursor.execute(
        "INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)",
         (name, current_date, current_time)
   
)

    conn.commit()
    conn.close()

    return f"{name} marked at {current_time}"


        














