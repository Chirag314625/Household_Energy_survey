# Deployment Guide

This project is ready to deploy as a Flask web service.

## Render

1. Push the latest code to GitHub.
2. Open Render and choose **New > Blueprint**.
3. Select this repository.
4. Render will read `render.yaml`.
5. Add this environment variable in Render:

```env
MONGODB_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/household_energy
```

Do not commit your real `.env` file. It contains your database password.

Render uses:

```bash
pip install -r app/backend/requirements.txt
gunicorn --chdir app/backend app:app
```

## Manual Flask Hosting

Use these commands if your host does not support `render.yaml`:

```bash
pip install -r app/backend/requirements.txt
gunicorn --chdir app/backend app:app
```

Required environment variables:

```env
MONGODB_URI=your_mongodb_atlas_uri
NODE_ENV=production
PORT=5000
```

Some hosts set `PORT` automatically. That is fine.

## Health Check

After deployment, visit:

```text
/health
```

Expected result:

```json
{
  "status": "OK",
  "mongodb": "connected"
}
```
