# DEPLOYMENT GUIDE

## 🚀 Deployment Options

Choose the best option for your needs:

---

## Option 1: Streamlit Cloud (Easiest - FREE)

### Prerequisites
- GitHub account with repository
- Streamlit account (free)

### Steps

#### Step 1: Push Code to GitHub
```bash
git add .
git commit -m "Deploy to Streamlit Cloud"
git push origin main
```

#### Step 2: Sign Up for Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Click "Sign up"
3. Sign in with GitHub
4. Authorize Streamlit

#### Step 3: Deploy App
1. Click "New app"
2. Select repository: `Alvin-creator-ai/afrifin-ai-cfo`
3. Select branch: `main`
4. Select file: `app.py`
5. Click "Deploy"

#### Step 4: Configure Secrets
1. In Streamlit Cloud dashboard, go to your app settings
2. Click "Secrets"
3. Add your environment variables:
```toml
OPENAI_API_KEY = "sk-your-api-key-here"
DATABASE_PATH = "./data/afrifin.db"
```

#### Step 5: Access Your App
- Your app will be live at: `https://afrifin-ai-cfo.streamlit.app`
- Share link with team members

**Cost:** FREE
**Setup time:** 10 minutes
**Best for:** Small teams, prototyping

---

## Option 2: Heroku (Reliable - $7/month)

### Prerequisites
- Heroku account
- Heroku CLI installed
- GitHub repository

### Steps

#### Step 1: Create Heroku App
```bash
# Install Heroku CLI
# macOS: brew tap heroku/brew && brew install heroku
# Linux: curl https://cli-assets.heroku.com/install.sh | sh

# Login to Heroku
heroku login

# Create app
heroku create afrifin-ai-cfo
```

#### Step 2: Create Required Files

**Procfile:**
```
web: streamlit run app.py --logger.level=error --client.showErrorDetails=false
```

**runtime.txt:**
```
python-3.13.0
```

#### Step 3: Add Dependencies
```bash
# Ensure requirements.txt is complete
pip freeze > requirements.txt
```

#### Step 4: Set Environment Variables
```bash
heroku config:set OPENAI_API_KEY=sk-your-api-key-here
heroku config:set DATABASE_PATH=./data/afrifin.db
```

#### Step 5: Deploy
```bash
# Add files
git add Procfile runtime.txt requirements.txt
git commit -m "Add Heroku deployment files"

# Deploy to Heroku
git push heroku main
```

#### Step 6: Access App
```bash
# Open app in browser
heroku open

# View logs
heroku logs --tail
```

**Cost:** $7-50/month
**Setup time:** 20 minutes
**Best for:** Production apps, custom domains

---

## Option 3: Railway (Modern - $5/month)

### Prerequisites
- Railway account
- GitHub connected

### Steps

#### Step 1: Connect to Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `afrifin-ai-cfo`

#### Step 2: Configure Environment
1. Go to "Variables"
2. Add:
   - `OPENAI_API_KEY`: Your API key
   - `DATABASE_PATH`: `./data/afrifin.db`

#### Step 3: Add Build Command
1. Go to "Settings"
2. Build command:
```bash
pip install -r requirements.txt
```

3. Start command:
```bash
streamlit run app.py
```

#### Step 4: Deploy
- Railway auto-deploys on git push
- Wait for build to complete

#### Step 5: Access App
- Your domain will be shown in Railway dashboard
- Share with team

**Cost:** $5-50/month
**Setup time:** 15 minutes
**Best for:** Modern deployments, easy scaling

---

## Option 4: AWS (Scalable - $50+/month)

### Prerequisites
- AWS account
- AWS CLI configured
- Docker installed (optional)

### Steps

#### Step 1: Create EC2 Instance
```bash
# Launch Ubuntu 22.04 LTS instance
# t3.micro or t3.small recommended

# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip
```

#### Step 2: Install Dependencies
```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and required packages
sudo apt-get install -y python3.13 python3-pip
sudo apt-get install -y tesseract-ocr

# Install git
sudo apt-get install -y git
```

#### Step 3: Clone Repository
```bash
cd /home/ubuntu
git clone https://github.com/Alvin-creator-ai/afrifin-ai-cfo.git
cd afrifin-ai-cfo
```

#### Step 4: Set Up Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

#### Step 5: Configure Environment
```bash
cp .env.example .env
nano .env
# Add OPENAI_API_KEY
```

#### Step 6: Use Systemd for Auto-Start
```bash
# Create service file
sudo nano /etc/systemd/system/afrifin.service
```

Add:
```ini
[Unit]
Description=AfriFin AI CFO
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/afrifin-ai-cfo
Environment="PATH=/home/ubuntu/afrifin-ai-cfo/venv/bin"
ExecStart=/home/ubuntu/afrifin-ai-cfo/venv/bin/streamlit run app.py --server.port 8501

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable afrifin
sudo systemctl start afrifin
```

#### Step 7: Set Up Nginx Reverse Proxy
```bash
sudo apt-get install -y nginx

# Create nginx config
sudo nano /etc/nginx/sites-available/default
```

Add:
```nginx
server {
    listen 80 default_server;
    server_name _;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

```bash
# Restart nginx
sudo systemctl restart nginx
```

#### Step 8: Set Up SSL (HTTPS)
```bash
# Install certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com
```

**Cost:** $50-200/month
**Setup time:** 1 hour
**Best for:** Enterprise, high traffic

---

## Option 5: Docker Deployment

### Prerequisites
- Docker installed
- Docker Hub account (optional)

### Steps

#### Step 1: Create Dockerfile
```dockerfile
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Step 2: Create .dockerignore
```
.git
.gitignore
__pycache__
*.pyc
.env
.streamlit
.pytest_cache
venv
.vscode
```

#### Step 3: Build Docker Image
```bash
docker build -t afrifin-ai-cfo:latest .
```

#### Step 4: Run Container Locally
```bash
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=sk-your-api-key \
  afrifin-ai-cfo:latest
```

#### Step 5: Push to Docker Hub
```bash
# Tag image
docker tag afrifin-ai-cfo:latest your-username/afrifin-ai-cfo:latest

# Push to Docker Hub
docker login
docker push your-username/afrifin-ai-cfo:latest
```

#### Step 6: Deploy with Docker Compose
```yaml
version: '3.8'

services:
  afrifin:
    image: your-username/afrifin-ai-cfo:latest
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=sk-your-api-key
      - DATABASE_PATH=./data/afrifin.db
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

```bash
docker-compose up -d
```

**Cost:** Varies by platform
**Setup time:** 30 minutes
**Best for:** Containerized deployments, microservices

---

## 🏆 Recommended Deployment Strategy

### For Small Teams (Best Value)
```
1. Start with Streamlit Cloud (FREE)
2. Move to Railway when scaling ($5/month)
3. Eventually migrate to AWS if needed
```

### Quick Deployment Checklist

- [ ] Ensure `.env` file is created with `OPENAI_API_KEY`
- [ ] Test app locally: `streamlit run app.py`
- [ ] Push code to GitHub
- [ ] Choose deployment platform
- [ ] Configure environment variables
- [ ] Deploy and test
- [ ] Share URL with team
- [ ] Set up monitoring/logging

---

## 🔒 Security Checklist

- ✅ Never commit `.env` file
- ✅ Use environment variables for secrets
- ✅ Enable HTTPS/SSL
- ✅ Set up authentication if needed
- ✅ Monitor API usage and costs
- ✅ Back up database regularly
- ✅ Use strong API keys
- ✅ Limit access to logs

---

## 📊 Monitoring & Maintenance

### Monitor Application
```bash
# For Streamlit Cloud
# Dashboard shows metrics and logs

# For Heroku
heroku logs --tail

# For AWS EC2
journalctl -u afrifin -f

# For Docker
docker logs -f container-name
```

### Update Application
```bash
# Make changes locally
git add .
git commit -m "Update features"
git push origin main

# Changes auto-deploy (Streamlit Cloud, Railway)
# Or manually redeploy (Heroku, AWS)
```

### Database Backup
```bash
# Download database
wget https://your-deployed-app/data/afrifin.db

# Or via SSH for AWS
scp -i key.pem ubuntu@ip:/home/ubuntu/afrifin-ai-cfo/data/afrifin.db ./
```

---

## 📞 Troubleshooting Deployments

### Issue: "ModuleNotFoundError"
**Solution:** Ensure all requirements in `requirements.txt`
```bash
pip freeze > requirements.txt
git push
```

### Issue: "OPENAI_API_KEY not found"
**Solution:** Verify environment variables are set
```bash
# Streamlit Cloud: Settings → Secrets
# Heroku: heroku config
# Railway: Variables section
```

### Issue: "Port already in use"
**Solution:** Use different port or kill process
```bash
streamlit run app.py --server.port 8502
```

### Issue: "Database locked"
**Solution:** Restart application
```bash
# Streamlit Cloud: Reboot via dashboard
# Heroku: heroku restart
# AWS: sudo systemctl restart afrifin
```

---

## 💰 Cost Comparison

| Platform | Cost | Setup Time | Scalability |
|----------|------|-----------|-------------|
| **Streamlit Cloud** | FREE | 10 min | Low |
| **Railway** | $5/month | 15 min | Medium |
| **Heroku** | $7/month | 20 min | Medium |
| **AWS** | $50+/month | 60 min | High |
| **Docker** | Varies | 30 min | Varies |

---

## ✅ Next Steps After Deployment

1. Test all features in production
2. Share URL with stakeholders
3. Gather feedback
4. Monitor performance
5. Plan scaling strategy
6. Set up automated backups
7. Configure logging/alerts

---

**Happy Deploying! 🚀**
