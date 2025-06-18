from flask import Flask, jsonify
from config import Config
from extensions import jwt, cors
from routes.auth_routes import auth_bp
from routes.event_routes import event_bp
from routes.contact_routes import contact_bp
from routes.user_routes import user_bp
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
jwt.init_app(app)
cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(event_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(user_bp)

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error'}), 500

# Health check route
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
