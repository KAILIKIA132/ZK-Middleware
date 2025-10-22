# Middleware Deployment Checklist

## Pre-deployment Checks

- [ ] Update requirements.txt with compatible versions
- [ ] Verify Dockerfile builds correctly
- [ ] Check environment variable handling
- [ ] Test API endpoints locally
- [ ] Verify configuration files

## Render Deployment Steps

1. **Fork Repository**
   - [ ] Fork the repository to your GitHub account
   - [ ] Verify all files are included in the fork

2. **Create Web Service**
   - [ ] Go to Render Dashboard
   - [ ] Click "New" → "Web Service"
   - [ ] Connect GitHub account
   - [ ] Select your forked repository
   - [ ] Configure:
     - Name: `canteen-middleware`
     - Environment: `Python`
     - Root Directory: `zk_middleware`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn -b 0.0.0.0:10000 app:app`
     - Plan: Free or paid as needed

3. **Configure Environment Variables**
   - [ ] `DEVICE_IP`: IP address of ZKTeco device
   - [ ] `SCHOOL_API_BASE_URL`: School management system API URL
   - [ ] `SCHOOL_API_KEY`: API key for school system (if required)
   - [ ] `PRINTER_HOST`: IP address of thermal printer
   - [ ] `PORT`: 10000 (Render requirement)

4. **Deploy**
   - [ ] Click "Create Web Service"
   - [ ] Wait for build and deployment to complete
   - [ ] Note the assigned URL

5. **Verify Deployment**
   - [ ] Check logs for errors
   - [ ] Test health endpoint: `https://your-url.onrender.com/health`
   - [ ] Test API endpoints

## Troubleshooting

### Common Issues

1. **Gunicorn Version Issues**
   - Use `gunicorn==22.0.0` instead of `22.1.0`
   - Check available versions with `pip index versions gunicorn`

2. **Pip Version Issues**
   - Add `RUN pip install --upgrade pip` to Dockerfile
   - Ensure pip is up to date before installing requirements

3. **Port Configuration**
   - Use `PORT` environment variable from Render
   - Default to 5000 for local development

4. **Dependency Issues**
   - Add system dependencies to Dockerfile (gcc, libc-dev, etc.)
   - Check for architecture-specific requirements

### Testing Commands

```bash
# Test locally
cd zk_middleware
python app.py

# Test Docker build
docker build -t zk-middleware-test .

# Test requirements
pip install --dry-run -r requirements.txt
```

## Post-deployment

- [ ] Update Flutter app with middleware URL
- [ ] Test end-to-end integration
- [ ] Monitor logs for errors
- [ ] Set up alerts if needed