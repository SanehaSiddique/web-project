from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime
from models.collections import users_collection, events_collection, registrations_collection
from helpers.serializer import serialize_docs

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

@user_bp.route('/events', methods=['GET'])
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

@user_bp.route('/profile', methods=['PUT'])
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
