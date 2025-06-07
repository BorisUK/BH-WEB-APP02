# app.py
import os
from flask import Flask, render_template_string

app = Flask(__name__)

# HTML template embedded in the Python file for simplicity
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Environment Variable Display</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .env-var {
            background-color: #e8f4fd;
            padding: 15px;
            border-left: 4px solid #0078d4;
            margin: 20px 0;
            border-radius: 5px;
        }
        .value {
            font-weight: bold;
            color: #0078d4;
            font-size: 1.2em;
        }
        .not-set {
            color: #d13438;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Azure Web App Environment Variables</h1>
        <div class="env-var">
            <h3>MAX_ITEMS Environment Variable:</h3>
            <div class="value">{{ max_items_value }}</div>
        </div>
        
        <h3>All Environment Variables:</h3>
        <div style="max-height: 400px; overflow-y: auto; background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
            {% for key, value in env_vars %}
                <div style="margin: 5px 0;">
                    <strong>{{ key }}:</strong> {{ value }}
                </div>
            {% endfor %}
        </div>
        
        <p style="margin-top: 30px; color: #666;">
            <small>App running on Azure Web App with Python {{ python_version }}</small>
        </p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # Get the MAX_ITEMS environment variable
    max_items = os.environ.get('MAX_ITEMS', 'Not set')
    
    # Get Python version
    import sys
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    # Get all environment variables (filtered for security)
    env_vars = []
    sensitive_keys = ['SECRET', 'PASSWORD', 'KEY', 'TOKEN', 'CONNECTION']
    
    for key, value in sorted(os.environ.items()):
        # Hide sensitive environment variables
        if any(sensitive in key.upper() for sensitive in sensitive_keys):
            env_vars.append((key, '[HIDDEN FOR SECURITY]'))
        else:
            env_vars.append((key, value))
    
    return render_template_string(
        HTML_TEMPLATE,
        max_items_value=max_items,
        env_vars=env_vars,
        python_version=python_version
    )

@app.route('/health')
def health():
    return {'status': 'healthy', 'max_items': os.environ.get('MAX_ITEMS', 'Not set')}

if __name__ == '__main__':
    # For local development
    app.run(debug=True, host='0.0.0.0', port=8000)