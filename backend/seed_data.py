from pymongo import MongoClient
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/eventpro')
client = MongoClient(MONGO_URI)
db = client.eventpro

# Clear existing data
print("Clearing existing data...")
db.users.delete_many({})
db.events.delete_many({})
db.contacts.delete_many({})
db.registrations.delete_many({})

# Create sample users
print("Creating sample users...")
users = [
    {
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '+1 (555) 123-4567',
        'password': generate_password_hash('password123'),
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'name': 'Jane Smith',
        'email': 'jane@example.com',
        'phone': '+1 (555) 987-6543',
        'password': generate_password_hash('password123'),
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'name': 'EventPro Admin',
        'email': 'admin@eventpro.com',
        'phone': '+1 (555) 555-5555',
        'password': generate_password_hash('admin123'),
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
]

user_results = db.users.insert_many(users)
user_ids = user_results.inserted_ids

# Create sample events
print("Creating sample events...")
events = [
    {
        'title': 'Tech Innovation Summit 2025',
        'description': 'Join industry leaders and innovators for a day of cutting-edge technology discussions and networking. This premier event brings together the brightest minds in tech to explore the future of innovation.',
        'date': (datetime.utcnow() + timedelta(days=30)).strftime('%Y-%m-%d'),
        'time': '9:00 AM - 6:00 PM',
        'location': 'San Francisco, CA',
        'venue': 'Moscone Center',
        'category': 'Conference',
        'price': 299,
        'maxAttendees': 500,
        'image': 'https://images.pexels.com/photos/2833037/pexels-photo-2833037.jpeg?auto=compress&cs=tinysrgb&w=800',
        'status': 'published',
        'organizer_id': user_ids[2],
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Annual Corporate Gala',
        'description': 'An elegant evening celebrating achievements and fostering corporate relationships. Join us for dinner, awards, and networking.',
        'date': (datetime.utcnow() + timedelta(days=45)).strftime('%Y-%m-%d'),
        'time': '7:00 PM - 11:00 PM',
        'location': 'New York, NY',
        'venue': 'Grand Ballroom',
        'category': 'Corporate',
        'price': 150,
        'maxAttendees': 300,
        'image': 'https://images.pexels.com/photos/1190298/pexels-photo-1190298.jpeg?auto=compress&cs=tinysrgb&w=800',
        'status': 'published',
        'organizer_id': user_ids[2],
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Startup Networking Event',
        'description': 'Connect with fellow entrepreneurs and investors in the thriving startup ecosystem. Perfect for founders, investors, and startup enthusiasts.',
        'date': (datetime.utcnow() + timedelta(days=20)).strftime('%Y-%m-%d'),
        'time': '6:00 PM - 9:00 PM',
        'location': 'Austin, TX',
        'venue': 'Innovation Hub',
        'category': 'Networking',
        'price': 75,
        'maxAttendees': 150,
        'image': 'https://images.pexels.com/photos/3183197/pexels-photo-3183197.jpeg?auto=compress&cs=tinysrgb&w=800',
        'status': 'published',
        'organizer_id': user_ids[1],
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Digital Marketing Workshop',
        'description': 'Master the latest digital marketing strategies and tools in this hands-on workshop. Learn from industry experts and get practical experience.',
        'date': (datetime.utcnow() + timedelta(days=60)).strftime('%Y-%m-%d'),
        'time': '10:00 AM - 4:00 PM',
        'location': 'Los Angeles, CA',
        'venue': 'Marketing Center',
        'category': 'Workshop',
        'price': 199,
        'maxAttendees': 100,
        'image': 'https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?auto=compress&cs=tinysrgb&w=800',
        'status': 'published',
        'organizer_id': user_ids[1],
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Leadership Excellence Conference',
        'description': 'Develop leadership skills with renowned speakers and interactive sessions. Perfect for managers and aspiring leaders.',
        'date': (datetime.utcnow() + timedelta(days=75)).strftime('%Y-%m-%d'),
        'time': '8:00 AM - 5:00 PM',
        'location': 'Chicago, IL',
        'venue': 'Conference Center',
        'category': 'Conference',
        'price': 349,
        'maxAttendees': 400,
        'image': 'https://images.pexels.com/photos/3184338/pexels-photo-3184338.jpeg?auto=compress&cs=tinysrgb&w=800',
        'status': 'published',
        'organizer_id': user_ids[2],
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Summer Social Mixer',
        'description': 'Unwind and network in a relaxed beachside setting with great food and music. Perfect for casual networking and fun.',
        'date': (datetime.utcnow() + timedelta(days=90)).strftime('%Y-%m-%d'),
        'time': '5:00 PM - 10:00 PM',
        'location': 'Miami, FL',
        'venue': 'Beachside Resort',
        'category': 'Social',
        'price': 89,
        'maxAttendees': 200,
        'image': 'https://images.pexels.com/photos/1774931/pexels-photo-1774931.jpeg?auto=compress&cs=tinysrgb&w=800',
        'status': 'published',
        'organizer_id': user_ids[0],
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
]

event_results = db.events.insert_many(events)
event_ids = event_results.inserted_ids

# Create sample registrations
print("Creating sample registrations...")
registrations = [
    {
        'event_id': event_ids[0],
        'user_id': user_ids[0],
        'registered_at': datetime.utcnow(),
        'status': 'confirmed'
    },
    {
        'event_id': event_ids[0],
        'user_id': user_ids[1],
        'registered_at': datetime.utcnow(),
        'status': 'confirmed'
    },
    {
        'event_id': event_ids[1],
        'user_id': user_ids[0],
        'registered_at': datetime.utcnow(),
        'status': 'confirmed'
    },
    {
        'event_id': event_ids[2],
        'user_id': user_ids[1],
        'registered_at': datetime.utcnow(),
        'status': 'confirmed'
    }
]

db.registrations.insert_many(registrations)

print("Sample data created successfully!")
print("\nSample login credentials:")
print("Email: admin@eventpro.com, Password: admin123")
print("Email: john@example.com, Password: password123")
print("Email: jane@example.com, Password: password123")