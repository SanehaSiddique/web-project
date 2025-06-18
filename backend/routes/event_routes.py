from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime
from models.collections import events_collection, registrations_collection
from helpers.serializer import serialize_doc, serialize_docs

event_bp = Blueprint('events', __name__, url_prefix='/api')

@event_bp.route('/events', methods=['GET'])
def get_events():
    try:
        events = list(events_collection.find({'status': 'published'}).sort('date', 1))
        return jsonify({'events': serialize_docs(events)}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@event_bp.route('/events/<event_id>', methods=['GET'])
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

@event_bp.route('/events', methods=['POST'])
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

@event_bp.route('/events/<event_id>', methods=['PUT'])
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

@event_bp.route('/events/<event_id>', methods=['DELETE'])
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

@event_bp.route('/events/<event_id>/register', methods=['POST'])
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
