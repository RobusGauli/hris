from hris import create_app
from flask_cors import CORS, cross_origin

app = create_app()
CORS(app)
app.run(host='0.0.0.0', port=9000, debug=True)