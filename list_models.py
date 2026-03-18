import json
import os
import sys

# Ensure we are in the right place
sys.path.append('/opt/CTFd')

from CTFd import create_app
import CTFd.models

def list_models():
    app = create_app()
    with app.app_context():
        return dir(CTFd.models)

if __name__ == "__main__":
    try:
        models = list_models()
        print(json.dumps(models, indent=4))
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
