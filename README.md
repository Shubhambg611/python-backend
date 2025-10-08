# Convis Labs - Python Backend

Python FastAPI backend for user registration with OTP email verification.

## Features

- User registration with email validation
- Password hashing using bcrypt
- OTP generation and email delivery
- MongoDB integration
- Email retry logic with configurable attempts
- CORS enabled for frontend integration

## Project Structure

```
python-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config/
│   │   ├── __init__.py
│   │   ├── database.py         # MongoDB connection
│   │   └── settings.py         # Environment configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py             # Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   └── register.py         # Registration endpoint
│   └── utils/
│       ├── __init__.py
│       ├── email.py            # Email sending logic
│       └── otp.py              # OTP generation
├── .env.example                # Environment variables template
├── requirements.txt            # Python dependencies
├── run.py                      # Application runner
└── README.md                   # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd python-backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `python-backend` directory:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=convis_db
EMAIL_USER=your_email@zoho.in
EMAIL_PASS=your_email_password
SMTP_HOST=smtp.zoho.in
SMTP_PORT=587
FRONTEND_URL=http://localhost:3000
```

### 3. Start MongoDB

Make sure MongoDB is running on your system:

```bash
# For Ubuntu/Debian
sudo systemctl start mongodb

# For macOS
brew services start mongodb-community

# Or using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### 4. Run the Application

```bash
# From the python-backend directory
python run.py
```

The API will be available at: `http://localhost:8000`

## API Endpoints

### Registration

**POST** `/api/register`

Register a new user and send OTP via email.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "companyName": "Example Corp",
  "phoneNumber": "+1234567890"
}
```

**Success Response (201):**
```json
{
  "message": "User registered successfully. Please check your email for the OTP to verify your account.",
  "userId": "507f1f77bcf86cd799439011"
}
```

**Error Responses:**

- **400 Bad Request:** Email already in use
- **500 Internal Server Error:** Server error

### Health Check

**GET** `/health`

Check if the API is running.

**Response (200):**
```json
{
  "status": "healthy"
}
```

## Integration with Frontend

Update your frontend code to use the Python backend endpoint:

```javascript
// Example: Update your registration form submission
const response = await fetch('http://localhost:8000/api/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: email,
    password: password,
    companyName: companyName,
    phoneNumber: phoneNumber
  })
});

const data = await response.json();

if (response.ok) {
  console.log('Registration successful:', data.message);
  // Redirect to OTP verification page
} else {
  console.error('Registration failed:', data.detail);
}
```

## API Documentation

Once the server is running, you can access:

- **Interactive API Docs (Swagger):** http://localhost:8000/docs
- **Alternative API Docs (ReDoc):** http://localhost:8000/redoc

## Development

### Running in Development Mode

The server runs with auto-reload enabled by default when using `run.py`.

### Testing

You can test the registration endpoint using curl:

```bash
curl -X POST "http://localhost:8000/api/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testPassword123",
    "companyName": "Test Company",
    "phoneNumber": "+1234567890"
  }'
```

## Production Deployment

For production deployment:

1. Set `reload=False` in `run.py`
2. Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

3. Set up environment variables securely
4. Configure reverse proxy (nginx/Apache)
5. Enable HTTPS

## Troubleshooting

### Email Not Sending

- Check SMTP credentials in `.env`
- Verify SMTP host and port
- Check firewall settings
- Review email provider settings (Zoho, Gmail, etc.)

### Database Connection Issues

- Ensure MongoDB is running
- Check `MONGODB_URI` in `.env`
- Verify database permissions

### CORS Errors

- Update allowed origins in `app/main.py`
- Add your frontend URL to `allow_origins`

## License

MIT
