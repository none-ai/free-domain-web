# FreeDomain - DigitalPlat

Free Domain For Everyone

## Description

FreeDomain is a Flask-based web application that provides free domain registration services. The project aims to make internet presence accessible to everyone.

## Features

- **Home page** with project information
- **Domain listing page** showing available and taken domains
- **Domain registration page** to claim available domains
- **User authentication** - Register and login functionality
- **User dashboard** - Manage your owned domains
- **DNS management** - Configure DNS records for your domains
- **Admin panel** - View statistics and manage the platform
- **Search & filtering** - Find domains easily
- **RESTful API** for domain data
- **API endpoint** for domain registration
- **User registration API**

## Routes

| Route | Description |
|-------|-------------|
| `/` | Home page |
| `/domains` | List of available domains |
| `/register` | Register a new domain (user registration) |
| `/login` | User login |
| `/logout` | User logout |
| `/dashboard` | User dashboard (requires login) |
| `/dns/<domain>` | DNS management (requires login) |
| `/admin` | Admin panel (requires admin login) |
| `/about` | About the project |
| `/api/domains` | API endpoint (JSON) |
| `/api/domains/register` | API endpoint to register domain (POST) |
| `/api/users/register` | API endpoint to register user (POST) |
| `/api/stats` | API endpoint for statistics (JSON) |
| `/api/domains/batch` | Batch domain operations (POST) |

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open browser at: `http://localhost:5000`

## Default Admin Account

- Username: `admin`
- Password: `admin123`

## API Usage

Get all domains:
```bash
curl http://localhost:5000/api/domains
```

Register a domain via API:
```bash
curl -X POST http://localhost:5000/api/domains/register \
  -H "Content-Type: application/json" \
  -d '{"domain": "mysite"}'
```

Register a user via API:
```bash
curl -X POST http://localhost:5000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "password123"}'
```

Get statistics:
```bash
curl http://localhost:5000/api/stats
```

## Requirements

- Python 3.8+
- Flask 3.0.0
- Flask-Login 0.6.3
- Flask-Bcrypt 1.0.1

## New Features Added

- **User System**: Complete user registration and authentication with secure password hashing
- **Dashboard**: Personal dashboard to manage your domains
- **DNS Management**: Add and manage DNS records (A, AAAA, CNAME, MX, TXT)
- **Admin Panel**: View platform statistics, all domains, and all users
- **Search & Filter**: Search domains by name, filter by availability
- **Enhanced API**: Additional endpoints for user registration and statistics

作者: stlin256的openclaw
