from flask import Flask

app = Flask(__name__)
import main
app.run(host='0.0.0.0', port=1000, debug=True)