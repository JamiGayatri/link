import os
import sqlite3
import openai
from dotenv import load_dotenv
from datetime import datetime
import uuid

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Setup the database and tables
def setup_database():
    conn = sqlite3.connect('museum_chatbot.db')
    cursor = conn.cursor()

    # Create tickets table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        ticket_id TEXT NOT NULL UNIQUE,
        booking_time TEXT NOT NULL,
        ticket_type TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )
    ''')

    # Create museums table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS museums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        museum_name TEXT NOT NULL UNIQUE,
        description TEXT NOT NULL,
        best_visiting_time TEXT NOT NULL,
        rating REAL NOT NULL
    )
    ''')

    # Insert sample data into museums table
    cursor.execute('''
    INSERT OR IGNORE INTO museums (museum_name, description, best_visiting_time, rating)
    VALUES 
    ("Renaissance Art Museum", "Explore works by masters like Leonardo da Vinci and Michelangelo.", "10:00 AM - 12:00 PM", 4.8),
    ("Modern Art Museum", "Features works from the 20th century, including pieces by Picasso and Dalí.", "2:00 PM - 4:00 PM", 4.5),
    ("Ancient Egypt Museum", "Discover the secrets of the pyramids, the Sphinx, and the Rosetta Stone.", "9:00 AM - 11:00 AM", 4.9)
    ''')

    conn.commit()
    conn.close()

def get_museum_info(museum_name):
    conn = sqlite3.connect('museum_chatbot.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT description, best_visiting_time, rating FROM museums WHERE museum_name = ?
    ''', (museum_name,))

    result = cursor.fetchone()
    conn.close()

    if result:
        description, best_visiting_time, rating = result
        return {"description": description, "best_visiting_time": best_visiting_time, "rating": rating}
    return None

def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error communicating with GPT-3: {e}")
        return "An error occurred. Please try again later."

def process_user_input(user_input):
    # Use GPT-3.5 to understand and categorize user input
    prompt = f"User says: '{user_input}'\nWhat is the user's intent? Provide a response and action steps."
    response = chat_with_gpt(prompt)
    return response

def book_ticket(user_name, ticket_type, quantity):
    ticket_id = str(uuid.uuid4())
    booking_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ticket_details = {
        "user_name": user_name,
        "ticket_id": ticket_id,
        "booking_time": booking_time,
        "ticket_type": ticket_type,
        "quantity": quantity
    }

    # Save ticket details to the database
    conn = sqlite3.connect('museum_chatbot.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO tickets (user_name, ticket_id, booking_time, ticket_type, quantity)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_name, ticket_id, booking_time, ticket_type, quantity))

    conn.commit()
    conn.close()

    return ticket_details

def retrieve_ticket(user_name):
    conn = sqlite3.connect('museum_chatbot.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT ticket_id FROM tickets WHERE user_name = ?
    ''', (user_name,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    return None

def museum_chatbot():
    print("Welcome to the Museum Guide Chatbot!")
    setup_database()  # Ensure the database is set up before starting

    while True:
        try:
            user_input = input("You: ").strip().lower()

            if "museum" in user_input:
                museum_name = user_input.split("museum")[-1].strip()
                museum_info = get_museum_info(museum_name)

                if museum_info:
                    print(f"Chatbot: {museum_name}\nDescription: {museum_info['description']}\nBest Visiting Time: {museum_info['best_visiting_time']}\nRating: {museum_info['rating']}")
                else:
                    print("Chatbot: Museum not found. Please enter a valid museum name.")
                continue

            response = process_user_input(user_input)

            if "book ticket" in response:
                user_name = input("Please enter your name: ").strip()
                ticket_type = input("Choose ticket type (adult, student): ").strip().lower()
                quantity = int(input("Enter the number of tickets: "))
                ticket_details = book_ticket(user_name, ticket_type, quantity)
                if ticket_details:
                    print(f"Chatbot: Your ticket has been booked successfully!\nName: {ticket_details['user_name']}\nTicket ID: {ticket_details['ticket_id']}\nBooking Time: {ticket_details['booking_time']}\nTicket Type: {ticket_details['ticket_type']}\nQuantity: {ticket_details['quantity']}")
                break  # Exit after booking

            elif "check ticket" in response:
                user_name = input("Please enter your name to check your ticket: ").strip()
                ticket_id = retrieve_ticket(user_name)
                if ticket_id:
                    print(f"Chatbot: Ticket found!\nName: {user_name}\nTicket ID: {ticket_id}")
                else:
                    print("Chatbot: No ticket found for this name.")
                break  # Exit after checking ticket

            else:
                print(f"Chatbot: {response}")
                
        except ValueError:
            print("Chatbot: Invalid input. Please enter a valid value.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    museum_chatbot()
