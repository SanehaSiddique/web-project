# EventPro Backend

A Flask-based backend API for the EventPro event management application.

## Features

- User authentication (register, login, logout)
- Event management (CRUD operations)
- Event registration system
- Contact form handling
- User dashboard with analytics
- MongoDB integration
- JWT token-based authentication
- CORS support for frontend integration

## Setup Instructions

### Prerequisites

- Python 3.8+
- MongoDB (local or cloud instance)
- pip (Python package manager)

### Installation

1. **Clone the repository and navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env` if needed
   - Update the MongoDB URI and JWT secret key in `.env`

5. **Start MongoDB:**
   - Make sure MongoDB is running on your system
   - Default connection: `mongodb://localhost:27017/eventpro`

6. **Seed the database with sample data:**
   ```bash
   python seed_data.py
   ```

7. **Run the application:**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/profile` - Get user profile

### Events
- `GET /api/events` - Get all published events
- `GET /api/events/<id>` - Get specific event
- `POST /api/events` - Create new event (authenticated)
- `PUT /api/events/<id>` - Update event (authenticated, owner only)
- `DELETE /api/events/<id>` - Delete event (authenticated, owner only)
- `POST /api/events/<id>/register` - Register for event (authenticated)

### Contact
- `POST /api/contact` - Submit contact form

### User
- `GET /api/user/events` - Get user's events (authenticated)
- `PUT /api/user/profile` - Update user profile (authenticated)

### Health
- `GET /api/health` - Health check endpoint

## Sample Login Credentials

After running the seed script, you can use these credentials:

- **Admin:** admin@eventpro.com / admin123
- **User 1:** john@example.com / password123
- **User 2:** jane@example.com / password123

## Database Schema

### Users Collection
```json
{
  "_id": "ObjectId",
  "name": "string",
  "email": "string",
  "phone": "string",
  "password": "hashed_string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Events Collection
```json
{
  "_id": "ObjectId",
  "title": "string",
  "description": "string",
  "date": "string",
  "time": "string",
  "location": "string",
  "venue": "string",
  "category": "string",
  "price": "number",
  "maxAttendees": "number",
  "image": "string",
  "status": "string",
  "organizer_id": "ObjectId",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Registrations Collection
```json
{
  "_id": "ObjectId",
  "event_id": "ObjectId",
  "user_id": "ObjectId",
  "registered_at": "datetime",
  "status": "string"
}
```

### Contacts Collection
```json
{
  "_id": "ObjectId",
  "name": "string",
  "email": "string",
  "phone": "string",
  "eventType": "string",
  "eventDate": "string",
  "message": "string",
  "submitted_at": "datetime",
  "status": "string"
}
```

## Development

- The application runs in debug mode by default
- CORS is configured to allow requests from `http://localhost:5173` (Vite dev server)
- JWT tokens expire after 7 days
- All passwords are hashed using Werkzeug's security functions

## Production Deployment

1. Set `FLASK_ENV=production` in your environment
2. Use a strong, unique JWT secret key
3. Configure MongoDB with proper authentication
4. Use a production WSGI server like Gunicorn
5. Set up proper CORS origins for your domain
6. Enable HTTPS