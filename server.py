#!/usr/bin/env python3
"""
Sovereign Matrix Control System - Local Server
Serves telemetry dashboard and updates state JSON
"""

import json
import os
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time


class MatrixStateManager:
    """Manages the sovereign matrix state"""
    
    def __init__(self, state_file='sovereign_matrix_state.json'):
        self.state_file = state_file
        self.load_state()
    
    def load_state(self):
        """Load state from JSON file"""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = self._default_state()
            self.save_state()
    
    def _default_state(self):
        """Return default state"""
        return {
            "system_id": "SM-NEURAL-KERNEL-001",
            "status": "nominal",
            "cycle": 0,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "latest_telemetry": "[INIT] Sovereign Matrix initialized. Awaiting neural kernel activation.",
            "version": "1.0.0",
            "uptime_seconds": 0,
            "ai_model": "sovereign-v1"
        }
    
    def save_state(self):
        """Save state to JSON file"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def update_cycle(self):
        """Increment cycle and update timestamp"""
        self.state['cycle'] += 1
        self.state['timestamp'] = datetime.utcnow().isoformat() + "Z"
        self.state['uptime_seconds'] += 15
        self.save_state()
    
    def update_telemetry(self, message):
        """Update latest telemetry message"""
        self.state['latest_telemetry'] = message
        self.save_state()
    
    def set_status(self, status):
        """Set system status"""
        if status in ['nominal', 'recovering', 'error', 'standby']:
            self.state['status'] = status
            self.save_state()


class MatrixRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        # Serve state JSON
        if parsed_path.path == '/api/state':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(state_manager.state).encode())
        
        # Serve telemetry endpoint
        elif parsed_path.path == '/api/telemetry':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            telemetry_data = {
                "status": "success",
                "message": "Sovereign Matrix telemetry API online.",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "system_state": state_manager.state
            }
            self.wfile.write(json.dumps(telemetry_data).encode())
        
        # Serve HTML files
        else:
            super().do_GET()
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")


def update_state_loop():
    """Background thread to update state periodically"""
    messages = [
        "[TICK] Kernel synchronization in progress...",
        "[SYNC] Neural pathways optimized. Latency: 45ms",
        "[MONITOR] All systems nominal. Performance: 99.98%",
        "[HEARTBEAT] Life support systems active. Cycle count: ",
        "[ALERT] Minor memory optimization in progress."
    ]
    msg_idx = 0
    
    while True:
        time.sleep(15)
        state_manager.update_cycle()
        message = messages[msg_idx % len(messages)]
        if "Cycle count" in message:
            message += str(state_manager.state['cycle'])
        state_manager.update_telemetry(message)
        msg_idx += 1
        print(f"[UPDATE] Cycle {state_manager.state['cycle']} - {message}")


if __name__ == '__main__':
    state_manager = MatrixStateManager()
    
    # Start background update thread
    update_thread = threading.Thread(target=update_state_loop, daemon=True)
    update_thread.start()
    
    # Start HTTP server
    PORT = 8000
    handler = MatrixRequestHandler
    httpd = HTTPServer(('0.0.0.0', PORT), handler)
    
    print(f"")
    print(f"╔══════════════════════════════════════════════════════════════╗")
    print(f"║          SOVEREIGN MATRIX CONTROL SYSTEM v1.0.0             ║")
    print(f"║                                                              ║")
    print(f"║  Server running on: http://localhost:{PORT}                 ║")
    print(f"║  Dashboard: http://localhost:{PORT}/index.html              ║")
    print(f"║  API State: http://localhost:{PORT}/api/state               ║")
    print(f"║  Telemetry: http://localhost:{PORT}/api/telemetry           ║")
    print(f"║                                                              ║")
    print(f"║  Press Ctrl+C to terminate neural kernel...                 ║")
    print(f"╚═══════��══════════════════════════════════════════════════════╝")
    print(f"")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Sovereign Matrix shutting down gracefully...")
        httpd.shutdown()
