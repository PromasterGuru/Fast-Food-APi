#run.def

'''
Debug the app.
'''

import os
from app import create_app

app_config_name = os.getenv('FLASK_ENV')
app = create_app(app_config_name)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
