from flask import Flask, render_template_string, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Load the n8n workflow data
with open('Festival template (1).json', 'r', encoding='utf-8') as f:
    workflow_data = json.load(f)

# Extract the HTML template from the workflow
def get_email_template():
    for node in workflow_data.get('nodes', []):
        if node.get('type') == 'n8n-nodes-base.code':
            js_code = node.get('parameters', {}).get('jsCode', '')
            if 'html = `' in js_code:
                # Extract the HTML template from the JavaScript template literal
                start = js_code.find('html = `') + len('html = `')
                end = js_code.rfind('`')
                if start > 0 and end > start:
                    return js_code[start:end].replace('${subject}', '{subject}').replace('${body}', '{body}')
    return None

# Get today's festival data
def get_todays_festival():
    today = datetime.now().strftime('%-d %B %Y')
    # This is a simplified example - you'll need to adapt this based on your actual data structure
    # In a real app, you would query your database or data source
    return {
        'subject': 'Today\'s Festival',
        'body': 'This is a sample festival message. In a real app, this would be dynamically generated.'
    }

@app.route('/')
def index():
    festival = get_todays_festival()
    template = get_email_template()
    
    if template:
        try:
            # Render the template with the festival data
            return render_template_string(template, **festival)
        except Exception as e:
            return f"Error rendering template: {str(e)}"
    else:
        return jsonify({
            'status': 'success',
            'message': 'Festival Email Automation is running!',
            'data': festival
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
