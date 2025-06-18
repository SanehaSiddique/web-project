from flask import Blueprint, request, jsonify
from datetime import datetime
from models.collections import contacts_collection

contact_bp = Blueprint('contact', __name__, url_prefix='/api')

@contact_bp.route('/contact', methods=['POST'])
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
