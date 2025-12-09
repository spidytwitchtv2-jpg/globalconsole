# Quick Start Guide

## What Changed?

Your app has been refactored from calling external APIs to using a local database with an API endpoint that receives data.

### Old Flow
```
Frontend → Login → Get Token → Fetch External API → Display
```

### New Flow
```
External Source → POST to Local API → Store in DB
Frontend → GET from Local API → Display
```

## Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python main.py
```
The server will start at `http://localhost:8002`

### 3. Post Sample Data
Open a new terminal and run:
```bash
python post_data_example.py
```

### 4. View in Browser
Open your browser and go to:
```
http://localhost:8002
```

You should see the sample data displayed with all the original features:
- List view / Grid view toggle
- Color-coded app names
- Copy to clipboard functionality
- Auto-refresh every 5 seconds

## API Endpoints

### POST /api/console-data
**Send data to the app**

```bash
curl -X POST http://localhost:8002/api/console-data \
  -H "Content-Type: application/json" \
  -d '{
    "meta": {"status": "success"},
    "data": {
      "messages": [
        {
          "app_name": "Facebook",
          "carrier": "236724XXX",
          "sms": "Your code is 123456",
          "time": "2 minutes ago"
        }
      ]
    }
  }'
```

### GET /api/console-data
**Retrieve stored data**

```bash
curl http://localhost:8002/api/console-data
```

## Integration Options

### Option 1: Manual Testing
Use the provided `post_data_example.py` script to post sample data.

### Option 2: Periodic Updates
Set up a cron job or scheduled task to run `integration_example.py` periodically:

**Linux/Mac (crontab):**
```bash
# Run every 5 minutes
*/5 * * * * cd /path/to/app && python integration_example.py
```

**Windows (Task Scheduler):**
Create a task that runs `integration_example.py` every 5 minutes.

### Option 3: Real-time Integration
Modify your existing data source to POST directly to the local API whenever new data arrives.

## What's Preserved?

All the frontend features work exactly as before:
- ✓ List view with animations
- ✓ Grid view with cards
- ✓ Accordion view (grouped by app)
- ✓ Color-coded app names
- ✓ Copy to clipboard
- ✓ Auto-refresh
- ✓ Responsive design
- ✓ All animations and transitions

## What's Removed?

- ✗ External API login
- ✗ Token management
- ✗ External API dependencies
- ✗ Hardcoded credentials

## Troubleshooting

### No data showing?
1. Make sure the server is running: `python main.py`
2. Post sample data: `python post_data_example.py`
3. Refresh your browser

### Port already in use?
Change the port in `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8003)  # Change 8002 to 8003
```

### Database issues?
Delete `app.db` and restart the server. The database will be recreated automatically.

## Next Steps

1. **Test the application** with sample data
2. **Integrate with your data source** using `integration_example.py` as a template
3. **Deploy to production** using the existing deployment guides (DEPLOYMENT.md, RENDER_DEPLOYMENT.md)

## Need Help?

Check these files for more information:
- `API_CHANGES.md` - Detailed documentation of all changes
- `integration_example.py` - Example integration script
- `post_data_example.py` - Simple data posting example
