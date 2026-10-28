"""Flask integration for the published Tableau dashboard and story."""
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent / '.packages'))
import os
from urllib.parse import urlparse
from flask import Flask, render_template, jsonify
import json

ROOT = Path(__file__).resolve().parent
app = Flask(__name__)

def tableau_url(variable):
    value = os.environ.get(variable, '').strip()
    if not value:
        return None
    parsed = urlparse(value)
    if parsed.scheme != 'https' or parsed.netloc != 'public.tableau.com' or not parsed.path.startswith('/views/'):
        raise ValueError(f'{variable} must be an https://public.tableau.com/views/... view URL')
    return value

@app.route('/')
def dashboard():
    return render_template('index.html', dashboard_url=tableau_url('TABLEAU_DASHBOARD_URL'), story_url=tableau_url('TABLEAU_STORY_URL'))

@app.route('/health')
def health():
    return jsonify(status='ok', tableau_configured=bool(tableau_url('TABLEAU_DASHBOARD_URL')))

@app.route('/api/audit')
def audit():
    return jsonify(json.loads((ROOT/'data'/'audit.json').read_text(encoding='utf-8')))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=False)
