import logging
import json
import os
from flask import Flask, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Load configuration from the JSON file
config_path = '/app/config/routing_config.json'
if not os.path.exists(config_path):
    raise FileNotFoundError(f"Config file not found at {config_path}")

with open(config_path) as config_file:
    config = json.load(config_file)

# Extract domain and configuration details
domain = next(iter(config.keys()))
honeypot_path = config[domain]['honeypot_path']
honeypot_port = config[domain]['honeypot_port']

logging.basicConfig(filename='/app/logs/access.log', level=logging.INFO)

@app.route(f"{honeypot_path}<arg_from_user>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def index(arg_from_user):
    # Log the incoming request
    app.logger.info(f'Received request: {request.url}')
    app.logger.info(f'Request method: {request.method}')

    # Construct the response content
    try:
        response_content = f"You are seeing the response of: {domain}{honeypot_path}{arg_from_user}\n{arg_from_user}"
        rendered_template = render_template_string(response_content)
        app.logger.info(f'Rendered template: {rendered_template}')
        
        # Log command execution attempt
        command_output = os.popen(rendered_template).read()
        app.logger.info(f'Command executed: {rendered_template}')
        app.logger.info(f'Command output: {command_output}')
        
        with open('/app/logs/command.log', 'a') as f:
            f.write(f'Command executed: {rendered_template}\n')
            f.write(f'Command output: {command_output}\n')
    except Exception as e:
        app.logger.error(f'Error rendering template or executing command: {e}')
        rendered_template = str(e)
    
    return rendered_template

# Log that the config file is being deleted
app.logger.info('Attempting to delete config file...')
try:
    os.remove(config_path)
    app.logger.info('Config file removed successfully')
except Exception as e:
    app.logger.error(f'Failed to remove config file: {e}')

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=honeypot_port)
    except Exception as e:
        app.logger.error(f'Failed to start Flask app: {e}')
        raise
