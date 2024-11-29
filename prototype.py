#code prototype

import re
import sqlite3

conn = sqlite3.connect("bookings.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS bookings
             (email TEXT NOT NULL,
             time TEXT NOT NULL);
             ''')
conn.commit()
conn.close()

def connect_db():
    return sqlite3.connect("bookings.db")

def show_all_bookings():
    conn = connect_db() #skapar uppkoppling till db
    cursor = conn.cursor() #skapar 'pekar'-objekt
    try:
        cursor.execute("SELECT time, email FROM bookings") #'pekar' på alla tider i db-tabell 
        bookings = cursor.fetchall() #variablen 'bookings' innehåller nu en lista med tider
        if len(bookings) == 0:
            return []
        else:            
            return [{"time": booking[0], "email": booking[1]} for booking in bookings]
    finally:
        cursor.close()
        conn.close()

def show_my_bookings(email):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT time FROM bookings WHERE email = ?", (email,))
        bookings = cursor.fetchall()
        if len(bookings) > 0:
            booking_list = [booking[0] for booking in bookings]
            return booking_list
        else:
            return ["Du har inga bokningar."]
    finally:
        cursor.close()
        conn.close()

def time_is_occupied(time):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT time FROM bookings WHERE time = ?", (time,)) 
        booking = cursor.fetchall()
        if len(booking) > 0:
            return True
        else:
            return False
    finally:
        cursor.close()
        conn.close()

def validate_time(time):
    if re.match(r"^(202[4-9])-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])-(0\d|1\d|2[0-3]):00$", time):
        return True
    else:
        return False
    
def validate_email(email):
    if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return True
    else:
        return False

def add_booking(time, email):
    while True:
        if not validate_time(time):
            print("Ogiltigt format. Ange: yyyy-mm-dd-HH:MM")
            continue
        if time_is_occupied(time):
            print("Tiden redan bokad.")
            continue
        break
    while True:
        if not validate_email(email):
            print("Felaktigt format. Ange e-post på nytt.")
            continue
        break
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings (email, time) VALUES (?, ?)", (email, time))
    conn.commit()
    cursor.close()
    conn.close()
    print("Tiden är bokad!")

def delete_booking():
    email = input("Ange epost för bokningen:")
    time = input("Ange tidpunkt för bokningen:")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE email = ? AND time = ?", (email, time))
    conn.commit()
    if cursor.rowcount == 0:
        print("Du har inga bokningar att ta bort.")
    else:
        print("Din bokning är nu borttagen.")
    cursor.close()
    conn.close()
        
def menu_text():
    print("Visa alla bokningar - tryck 'S'")
    print("Visa dina bokningar - tryck 'M'")
    print("Boka - tryck 'A'")
    print("Avboka - tryck 'D'")
    print("Avsluta - tryck 'E'")
    choice = input().upper()
    return choice

def menu():
    choice = menu_text() 
    while True:
        if choice == "S":
            show_all_bookings()
        elif choice == "M":
            show_my_bookings()
        elif choice == "A":
            add_booking()
        elif choice == "D":
            delete_booking()
        elif choice == "E":
            break
        else:
            print("Felaktigt val.")
        choice = menu_text() 

def main():
    menu()

#main()