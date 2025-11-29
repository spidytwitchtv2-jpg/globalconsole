# Render Deployment Guide

Complete guide for deploying the Console App on Render.com.

## Quick Start

1. **Connect your repository** to Render
2. **Create a new Web Service**
3. **Configure the service** (see below)
4. **Deploy**

## Render Configuration

### Service Settings

- **Name:** `console-app` (or your preferred name)
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Start Command

The start command for Render is:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Important Notes:**
- Render automatically sets the `$PORT` environment variable
- Use `0.0.0.0` as the host (not `127.0.0.1` or `localhost`)
- The `$PORT` variable is required - don't use a fixed port number

### Alternative Start Commands

If you need different options:

**With auto-reload (development only):**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT --reload
```

**With workers (production):**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT --workers 4
```

**With specific log level:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT --log-level info
```

## Using render.yaml (Recommended)

If you use the `render.yaml` file included in the repository:

1. **Connect your repository** to Render
2. **Render will automatically detect** `render.yaml`
3. **Click "Apply"** to create the service
4. **Deploy**

The `render.yaml` file includes:
- Build command
- Start command
- Environment variables
- Python version

## Manual Configuration Steps

### Step 1: Create Web Service

1. Go to Render Dashboard
2. Click **"New +"** → **"Web Service"**
3. Connect your repository
4. Select the repository and branch

### Step 2: Configure Service

**Basic Settings:**
- **Name:** `console-app`
- **Region:** Choose closest to your users
- **Branch:** `main` (or your default branch)
- **Root Directory:** Leave empty (or `app` if your files are in a subdirectory)

**Build & Deploy:**
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Advanced Settings (Optional):**
- **Auto-Deploy:** `Yes` (deploys on every push)
- **Health Check Path:** `/` (or `/api/console-data`)

### Step 3: Environment Variables (Optional)

You can set environment variables in Render:

- `PYTHON_VERSION`: `3.12.11` (or your preferred version)
- Any other custom variables your app needs

### Step 4: Deploy

Click **"Create Web Service"** and Render will:
1. Install dependencies from `requirements.txt`
2. Start your application
3. Provide a URL (e.g., `https://console-app.onrender.com`)

## Important Notes

### Port Configuration

- **Always use `$PORT`** - Render sets this automatically
- **Never hardcode a port** like `8000` or `5000`
- The `$PORT` variable is set by Render's infrastructure

### Database

- SQLite database (`app.db`) will be created automatically
- **Note:** SQLite on Render is ephemeral - data may be lost on redeploy
- For production, consider using Render's PostgreSQL addon

### Static Files

- Static files in the `static/` directory are served by FastAPI
- No additional configuration needed

### CORS

- The app already has CORS configured to allow all origins
- For production, you may want to restrict this to your domain

## Troubleshooting

### Build Fails

**Error:** "Module not found" or "pip install failed"

**Solution:**
- Check `requirements.txt` is in the root directory
- Verify Python version compatibility
- Check build logs for specific errors

### Application Won't Start

**Error:** "Application failed to respond"

**Solution:**
- Verify start command is correct: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Check application logs in Render dashboard
- Ensure `main.py` exists and has the `app` variable

### Port Already in Use

**Error:** "Address already in use"

**Solution:**
- Make sure you're using `$PORT` not a fixed port
- Check start command doesn't have `--port 8000` or similar

### Database Issues

**Error:** "Database file not found" or "Permission denied"

**Solution:**
- SQLite will create the database automatically
- Check file permissions
- Consider using Render PostgreSQL for persistent storage

## Monitoring

### View Logs

1. Go to your service in Render dashboard
2. Click **"Logs"** tab
3. View real-time application logs

### Health Checks

Render automatically checks if your service is responding. You can:
- Set a custom health check path
- Monitor uptime in the dashboard

## Updating Your Application

### Automatic Deploys

If auto-deploy is enabled:
1. Push changes to your repository
2. Render automatically rebuilds and redeploys

### Manual Deploy

1. Go to your service
2. Click **"Manual Deploy"**
3. Select branch and click **"Deploy"**

## Cost Considerations

- **Free tier:** Services sleep after 15 minutes of inactivity
- **Paid plans:** Services stay awake 24/7
- Check Render's pricing for current rates

## Comparison with Namecheap

| Feature | Render | Namecheap |
|---------|--------|-----------|
| Setup | Easy (Git-based) | Manual upload |
| Auto-deploy | Yes | No |
| Free tier | Yes (with limitations) | No |
| Database | PostgreSQL addon | SQLite |
| WSGI/ASGI | Native ASGI support | Requires WSGI adapter |
| Configuration | Simple | More complex |

## Next Steps

After deployment:
1. Test your application at the provided URL
2. Set up custom domain (if needed)
3. Configure environment variables
4. Set up monitoring and alerts
5. Consider upgrading for production use

## Support

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
- Check application logs for debugging

