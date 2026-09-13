# Sovereign Matrix - Deployment Guide

## Quick Deploy URLs

### GitHub Pages (Recommended for Dashboard)
1. Go to: https://github.com/mindripper87/sovereign-matrix/settings/pages
2. Select source: `main` branch
3. Access at: `https://mindripper87.github.io/sovereign-matrix/`

### Live Dashboard
🔗 **https://mindripper87.github.io/sovereign-matrix/index.html**

### API Endpoints (GitHub Raw)
- State: `https://raw.githubusercontent.com/mindripper87/sovereign-matrix/main/sovereign_matrix_state.json`
- Telemetry: `https://raw.githubusercontent.com/mindripper87/sovereign-matrix/main/api/telemetry.json`
- Config: `https://raw.githubusercontent.com/mindripper87/sovereign-matrix/main/config.json`

## Local Development

```bash
# Clone repository
git clone https://github.com/mindripper87/sovereign-matrix.git
cd sovereign-matrix

# Start local server
python3 server.py

# Open browser to http://localhost:8000/index.html
```

## Production Deployment

### Option 1: Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Option 2: Netlify
```bash
npm install -g netlify-cli
netlify deploy
```

### Option 3: Heroku
```bash
heroku create sovereign-matrix-prod
git push heroku main
heroku logs --tail
```

### Option 4: Docker + Any Cloud
```bash
# Build
docker build -t sovereign-matrix:1.0.0 .

# Push to registry
docker tag sovereign-matrix:1.0.0 myregistry/sovereign-matrix:latest
docker push myregistry/sovereign-matrix:latest

# Deploy to cloud (AWS ECS, Google Cloud Run, Azure Container Instances, etc.)
```

## AI Model Integration

### 1. OpenAI API
```bash
# Set environment variable
export OPENAI_API_KEY="your-key-here"

# Test connection
python3 -c "
import requests
import os
response = requests.get(
    'https://raw.githubusercontent.com/mindripper87/sovereign-matrix/main/sovereign_matrix_state.json'
)
print(response.json())
"
```

### 2. Anthropic Claude
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### 3. Local LLM (Ollama)
```bash
# Install Ollama from https://ollama.ai
# Start Ollama service
ollama serve

# Test endpoint
curl http://localhost:11434/api/generate -d '{"model":"llama2","prompt":"test"}'
```

## GitHub Actions Automation

Create `.github/workflows/update-telemetry.yml`:

```yaml
name: Update Telemetry

on:
  schedule:
    - cron: '*/15 * * * *'  # Every 15 minutes
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Update State
        run: |
          python3 -c "
          import json
          from datetime import datetime
          
          state = {
              'system_id': 'SM-NEURAL-KERNEL-001',
              'status': 'nominal',
              'cycle': 0,
              'timestamp': datetime.utcnow().isoformat() + 'Z',
              'latest_telemetry': '[AUTO] Sovereign Matrix telemetry updated via GitHub Actions',
              'version': '1.0.0'
          }
          
          with open('sovereign_matrix_state.json', 'w') as f:
              json.dump(state, f, indent=2)
          "
      - uses: stefanzweifel/git-auto-commit-action@v4
        with:
          commit_message: 'Auto-update telemetry'
```

## Monitoring & Alerts

### Uptime Monitoring
```bash
# Using curl
watch -n 60 'curl -s https://mindripper87.github.io/sovereign-matrix/index.html | grep -o "System ID"'
```

### Log Aggregation
```bash
# Stream logs
tail -f sovereign_matrix_state.json
```

## Troubleshooting Deployment

### CORS Issues
- GitHub Pages automatically sets proper CORS headers
- For custom servers, ensure `config.json` has correct CORS settings

### Stale Content
- GitHub Pages caches for ~5 minutes
- Add `?t=` parameter to bypass cache (already in index.html)

### Rate Limiting
- GitHub raw URLs: 60 requests/hour/IP
- Implement caching for production

## Performance Optimization

### Enable Compression
Add to server headers:
```
Content-Encoding: gzip
```

### Cache Control
```
Cache-Control: public, max-age=60, must-revalidate
```

### CDN Integration
Use Cloudflare or similar to cache JSON responses globally.

## Rollback Procedure

```bash
# Revert to previous commit
git revert HEAD
git push origin main

# Or reset to specific commit
git reset --hard abc123
git push -f origin main
```

## Support & Debugging

Check browser console (F12) for errors and API responses.

---

**Status**: Ready for Production  
**Last Updated**: 2026-09-13  
**Maintainer**: mindripper87
