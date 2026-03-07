# FreeDomain - DigitalPlat

Free Domain For Everyone

## Description

FreeDomain is a Flask-based web application that provides free domain registration services. The project aims to make internet presence accessible to everyone.

## Features

- Home page with project information
- Domain listing page showing available and taken domains
- Domain registration page to claim available domains
- About page with project details
- RESTful API for domain data
- API endpoint for domain registration

## Routes

| Route | Description |
|-------|-------------|
| `/` | Home page |
| `/domains` | List of available domains |
| `/register` | Register a new domain |
| `/about` | About the project |
| `/api/domains` | API endpoint (JSON) |
| `/api/domains/register` | API endpoint to register domain (POST) |

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

## API Usage

Get all domains:
```bash
curl http://localhost:5000/api/domains
```

## Requirements

- Python 3.8+
- Flask 3.0.0

作者: stlin256的openclaw
