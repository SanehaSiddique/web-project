from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

# Initialize extensions
jwt = JWTManager(app)
CORS(app, resources={r"/api/auth/*": {"origins": "http://localhost:5173"}})
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/eventpro')
client = MongoClient(MONGO_URI)
db = client.eventpro

# Collections
users_collection = db.users
events_collection = db.events
contacts_collection = db.contacts
registrations_collection = db.registrations

# Helper function to serialize MongoDB documents
def serialize_doc(doc):
    if doc is None:
        return None
    # Convert _id to string
    doc['_id'] = str(doc['_id'])
    # Convert datetime objects to ISO format strings
    for key, value in doc.items():
        if isinstance(value, datetime):
            doc[key] = value.isoformat()
        elif isinstance(value, ObjectId):
            doc[key] = str(value)
        elif isinstance(value, dict):
            doc[key] = serialize_doc(value)  # Recursively serialize nested dictionaries
    return doc

def serialize_docs(docs):
    return [serialize_doc(doc) for doc in docs]

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error'}), 500

# Auth Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} is required'}), 400
        
        # Check if user already exists
        if users_collection.find_one({'email': data['email']}):
            return jsonify({'message': 'User already exists with this email'}), 400
        
        # Create new user
        user_data = {
            'name': data['name'],
            'email': data['email'],
            'phone': data.get('phone', ''),
            'password': generate_password_hash(data['password']),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = users_collection.insert_one(user_data)
        
        # Create access token
        access_token = create_access_token(identity=str(result.inserted_id))
        
        # Return user data (without password)
        user_data.pop('password')
        user_data['_id'] = str(result.inserted_id)
        
        return jsonify({
            'message': 'User registered successfully',
            'token': access_token,
            'user': user_data
        }), 201
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email and password are required'}), 400
        
        # Find user
        user = users_collection.find_one({'email': data['email']})
        if not user or not check_password_hash(user['password'], data['password']):
            return jsonify({'message': 'Invalid email or password'}), 401
        
        # Create access token
        access_token = create_access_token(identity=str(user['_id']))
        
        # Return user data (without password)
        user.pop('password')
        user = serialize_doc(user)
        
        return jsonify({
            'message': 'Login successful',
            'token': access_token,
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        user.pop('password')
        return jsonify(serialize_doc(user)), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'Logout successful'}), 200

# Events Routes
@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        events = list(events_collection.find({'status': 'published'}).sort('date', 1))
        return jsonify({'events': serialize_docs(events)}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/events/<event_id>', methods=['GET'])
def get_event(event_id):
    try:
        event = events_collection.find_one({'_id': ObjectId(event_id)})
        if not event:
            return jsonify({'message': 'Event not found'}), 404
        
        # Get registration count
        registration_count = registrations_collection.count_documents({'event_id': ObjectId(event_id)})
        event['registeredCount'] = registration_count
        
        return jsonify({'event': serialize_doc(event)}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/events', methods=['POST'])
@jwt_required()
def create_event():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'date', 'time', 'location']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} is required'}), 400
        
        event_data = {
            'title': data['title'],
            'description': data['description'],
            'date': data['date'],
            'time': data['time'],
            'location': data['location'],
            'venue': data.get('venue', ''),
            'category': data.get('category', 'Event'),
            'price': data.get('price', 0),
            'maxAttendees': data.get('maxAttendees', 100),
            'image': data.get('image', ''),
            'status': data.get('status', 'draft'),
            'organizer_id': ObjectId(user_id),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = events_collection.insert_one(event_data)
        event_data['_id'] = str(result.inserted_id)
        event_data['organizer_id'] = str(event_data['organizer_id'])
        
        return jsonify({
            'message': 'Event created successfully',
            'event': event_data
        }), 201
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/events/<event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Check if event exists and user owns it
        event = events_collection.find_one({
            '_id': ObjectId(event_id),
            'organizer_id': ObjectId(user_id)
        })
        
        if not event:
            return jsonify({'message': 'Event not found or unauthorized'}), 404
        
        # Update event
        update_data = {
            'updated_at': datetime.utcnow()
        }
        
        # Update only provided fields
        allowed_fields = ['title', 'description', 'date', 'time', 'location', 'venue', 
                         'category', 'price', 'maxAttendees', 'image', 'status']
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        events_collection.update_one(
            {'_id': ObjectId(event_id)},
            {'$set': update_data}
        )
        
        return jsonify({'message': 'Event updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/events/<event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    try:
        user_id = get_jwt_identity()
        
        # Check if event exists and user owns it
        result = events_collection.delete_one({
            '_id': ObjectId(event_id),
            'organizer_id': ObjectId(user_id)
        })
        
        if result.deleted_count == 0:
            return jsonify({'message': 'Event not found or unauthorized'}), 404
        
        # Also delete related registrations
        registrations_collection.delete_many({'event_id': ObjectId(event_id)})
        
        return jsonify({'message': 'Event deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/events/<event_id>/register', methods=['POST'])
@jwt_required()
def register_for_event(event_id):
    try:
        user_id = get_jwt_identity()
        
        # Check if event exists
        event = events_collection.find_one({'_id': ObjectId(event_id)})
        if not event:
            return jsonify({'message': 'Event not found'}), 404
        
        # Check if user already registered
        existing_registration = registrations_collection.find_one({
            'event_id': ObjectId(event_id),
            'user_id': ObjectId(user_id)
        })
        
        if existing_registration:
            return jsonify({'message': 'Already registered for this event'}), 400
        
        # Check if event is full
        registration_count = registrations_collection.count_documents({'event_id': ObjectId(event_id)})
        if registration_count >= event.get('maxAttendees', 100):
            return jsonify({'message': 'Event is full'}), 400
        
        # Create registration
        registration_data = {
            'event_id': ObjectId(event_id),
            'user_id': ObjectId(user_id),
            'registered_at': datetime.utcnow(),
            'status': 'confirmed'
        }
        
        registrations_collection.insert_one(registration_data)
        
        return jsonify({'message': 'Successfully registered for event'}), 201
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Contact Routes
@app.route('/api/contact', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} is required'}), 400
        
        contact_data = {
            'name': data['name'],
            'email': data['email'],
            'phone': data.get('phone', ''),
            'eventType': data.get('eventType', ''),
            'eventDate': data.get('eventDate', ''),
            'message': data['message'],
            'submitted_at': datetime.utcnow(),
            'status': 'new'
        }
        
        contacts_collection.insert_one(contact_data)
        
        return jsonify({'message': 'Contact form submitted successfully'}), 201
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# User Routes
@app.route('/api/user/events', methods=['GET'])
@jwt_required()
def get_user_events():
    try:
        user_id = get_jwt_identity()
        
        # Get events created by user
        events = list(events_collection.find({'organizer_id': ObjectId(user_id)}).sort('created_at', -1))
        
        # Add registration count to each event
        for event in events:
            registration_count = registrations_collection.count_documents({'event_id': event['_id']})
            event['registeredCount'] = registration_count
        
        return jsonify({'events': serialize_docs(events)}), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/user/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        update_data = {
            'updated_at': datetime.utcnow()
        }
        
        # Update only allowed fields
        allowed_fields = ['name', 'phone']
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        users_collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
        
        return jsonify({'message': 'Profile updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Health check route
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)