# Console App

A FastAPI application with SQLite database that provides authentication and console data retrieval capabilities.

## Features

- FastAPI backend with SQLite database
- Token caching system (5-second rule to prevent excessive API calls)
- RESTful API endpoints for authentication and data retrieval
- Modern frontend interface with auto-refresh capabilities
- Compatible with Namecheap hosting and Passenger WSGI

## Prerequisites

- Python 3.7+ (Python 3.8+ recommended)
- pip (Python package installer)

## Local Development

### Installation

1. Navigate to the app directory:
   ```bash
   cd app
   ```

2. Run the installation script:
   ```bash
   install.bat
   ```

   This will:
   - Install all required Python packages
   - Create the SQLite database

### Running the Application

1. Start the application:
   ```bash
   start.bat
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## Production Deployment

For Namecheap hosting deployment, see [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

Quick steps:
1. Upload all files to your Namecheap hosting account
2. Install Python packages (see DEPLOYMENT.md)
3. Ensure Passenger WSGI is configured correctly
4. Restart your Passenger application

## API Endpoints

- `POST /api/login` - Perform initial login
- `GET /api/refresh-token` - Get refreshed authentication token
- `GET /api/console-data` - Retrieve console data

## Configuration

The application uses the following credentials by default:
- Email: Aktermamber.00.7@gmail.com
- Password: Bd55555$

## How It Works

1. On application start, it performs a login using the predefined credentials
2. The authentication token is cached for 5 seconds to prevent excessive API calls
3. The frontend automatically refreshes the token and fetches new data every 5 seconds
4. If a request fails, the frontend continues to display the last successful data

## File Structure

```
app/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies (Python 3.8+)
├── requirements-py37.txt # Python dependencies (Python 3.7)
├── passenger_wsgi.py    # Passenger WSGI configuration
├── install.bat          # Local installation script (Windows)
├── install.sh          # Server installation script (Linux)
├── install_packages.py # Python installer script
├── install_web.py      # Web-based installer script
├── start.bat           # Local startup script
├── README.md           # This file
├── DEPLOYMENT.md       # Deployment guide
└── static/             # Frontend assets
    └── index.html       # Main frontend page
```

## Troubleshooting

For deployment issues, see [DEPLOYMENT.md](DEPLOYMENT.md) for detailed troubleshooting steps.
