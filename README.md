# Sovereign Matrix Control System

**AI-powered telemetry dashboard and neural kernel integration platform**

## Overview

Sovereign Matrix is a real-time telemetry monitoring system designed to interface with AI models and neural kernel architectures. It provides live system status, cycle counting, and telemetry streaming capabilities.

## Features

✅ **Real-time Dashboard** - Live telemetry visualization  
✅ **Neural Kernel Integration** - Direct AI model connectivity  
✅ **JSON State Management** - Persistent system state tracking  
✅ **Auto-refresh** - 15-second update intervals  
✅ **GitHub Integration** - Hosted state files via raw GitHub URLs  
✅ **REST API** - Full telemetry endpoints for AI integration  
✅ **Multi-model Support** - OpenAI, Claude, local LLMs  
✅ **CORS Enabled** - Cross-origin requests supported  

## Quick Start

### Option 1: Local Server (Python)

```bash
# Install dependencies (none required - uses standard library)
python3 server.py

# Navigate to http://localhost:8000/index.html
```

### Option 2: GitHub Pages

1. Go to repository Settings → Pages
2. Set source to `main` branch
3. Access at: `https://mindripper87.github.io/sovereign-matrix/index.html`

### Option 3: Static HTML

Simply open `index.html` in your browser or host on any web server.

## File Structure

```
sovereign-matrix/
├── index.html                      # Dashboard UI
├── sovereign_matrix_state.json     # System state (real-time)
├── config.json                     # Configuration
├── server.py                       # Python local server
├── api/
│   └── telemetry.json             # Telemetry endpoint
└── README.md                       # Documentation
```

## API Endpoints

### Get Current State
```
GET /api/state
Response: { system_id, status, cycle, timestamp, latest_telemetry, ... }
```

### Get Telemetry
```
GET /api/telemetry
Response: { status, message, timestamp, system_state }
```

### Update State (via GitHub)
```
Edit sovereign_matrix_state.json and commit
```

## Integration with AI Models

### OpenAI / ChatGPT
```python
import requests

response = requests.get(
    'https://raw.githubusercontent.com/mindripper87/sovereign-matrix/main/sovereign_matrix_state.json'
)
matrix_state = response.json()
print(f"Status: {matrix_state['status']}")
```

### Anthropic Claude
```python
import anthropic

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": f"Analyze this matrix state: {matrix_state}"
    }]
)
```

### Local LLM (Ollama)
```bash
curl -X POST http://localhost:11434/api/generate \
  -d '{
    "model": "llama2",
    "prompt": "Activate Sovereign Matrix protocol",
    "stream": false
  }'
```

## Configuration

Edit `config.json` to customize:

- **Server settings** - Host, port, protocol
- **GitHub repository** - Raw URL for state files
- **AI model endpoints** - Add your API keys and endpoints
- **Telemetry intervals** - Update frequency
- **Security** - CORS, rate limiting

## Development

### Local Testing
```bash
python3 server.py
# Dashboard: http://localhost:8000/index.html
# API: http://localhost:8000/api/state
```

### Update State
```bash
# Edit sovereign_matrix_state.json
# Commit and push to GitHub
git add sovereign_matrix_state.json
git commit -m "Update telemetry"
git push origin main
```

### Monitoring
```bash
# Watch telemetry updates
watch -n 2 curl -s http://localhost:8000/api/state | jq
```

## Troubleshooting

### Dashboard shows "Awaiting connection"
- Verify `sovereign_matrix_state.json` exists
- Check browser console for errors
- Ensure GitHub raw URL is correct
- Check CORS settings

### API returns 404
- Verify file paths in config.json
- Check GitHub repository visibility (should be public)
- Confirm branch name (default: main)

### State not updating
- Verify `server.py` is running (if using local server)
- Check file permissions
- Ensure JSON format is valid

## Deployment Options

### Vercel / Netlify (Static)
```bash
git push origin main
# Auto-deployed to CDN
```

### Heroku (with server.py)
```bash
heroku create sovereign-matrix
git push heroku main
```

### AWS Lambda + API Gateway
```bash
# Use server.py as Lambda handler
# Configure API Gateway for /api/* routes
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
EXPOSE 8000
CMD ["python3", "server.py"]
```

```bash
docker build -t sovereign-matrix .
docker run -p 8000:8000 sovereign-matrix
```

## Security Notes

⚠️ **GitHub Raw URLs are public** - Don't store secrets in state files  
⚠️ **API endpoints are open** - Implement authentication if needed  
⚠️ **CORS is enabled** - Restrict origins in production  

## License

MIT - Free to use and modify

## Support

- 📖 [GitHub Issues](https://github.com/mindripper87/sovereign-matrix/issues)
- 💬 [Discussions](https://github.com/mindripper87/sovereign-matrix/discussions)
- 📧 Contact via GitHub

---

**Status**: ✅ Production Ready  
**Last Updated**: 2026-09-13  
**Version**: 1.0.0
