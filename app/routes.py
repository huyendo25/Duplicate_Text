from functions import *
from flask_cors import CORS
import shutil
#from app import functions
from pickle import NONE
from flask import Flask, request, redirect, url_for , jsonify , send_file ,send_from_directory
from werkzeug.utils import secure_filename
import json

class DataModel:
    def __init__(self, result, message, item):
        self.result = result
        self.message = message
        self.item = item

class ErrorModel:
    def __init__(self, result, message,item):
        self.result = result
        self.message = message
        self.item = item

class ResponseModel:
    def __init__(self, data, error):
        self.data = data
        self.error = error

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'docx','doc','pdf','txt'}

app = Flask(__name__, static_url_path='/static')
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['upload_folder'] = UPLOAD_FOLDER 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    error = None
    data = None
    try:
        if request.method == 'POST':
            file = request.files['file']
            filename = secure_filename(file.filename)
            input_file = os.path.join(app.config['upload_folder'], filename)
            file.save(input_file)
            item = predict_data (input_file)
            data = DataModel(True, " Xử lí file thành công ", item)
        if error is not None:
            error = vars(error)
        if data is not None:
            data = vars(data)
        response = ResponseModel(data, error)
    except:
        if response.status_code in [500]:
            data = DataModel(False, " Chưa tải tệp tin! ", item)
            if error is not None:
                error = vars(error)
            if data is not None:
                data = vars(data)
            response = ResponseModel(data, error)
        if error is not None:
            error = vars(error)
        if data is not None:
            data = vars(data)
        response = ResponseModel(data, error)
    return json.dumps(vars(response))

@app.route('/view', methods=['GET', 'POST'])
def view():
    error = None
    data = None
    filename = request.args.get('filename')
    try:
        if request.method == 'POST':
            path = fr'E:\DATN\dataframe\train_file\{filename}'
            path1 = os.path.join(app.config['upload_folder'], filename)
            item = {"input_path": path, "output_path": path1}
            shutil.copyfile(path, path1)
            #file.save(input_file)
            #item = predict_data (input_file)
            data = DataModel(True, " Xử lí file thành công ", item)
        if error is not None:
            error = vars(error)
        if data is not None:
            data = vars(data)
        response = ResponseModel(data, error)
    except:
        item = {"input_path": [], "output_path": []}
        data = DataModel(False, " Không tìm thấy tập tin! ", item)
        if error is not None:
            error = vars(error)
        if data is not None:
            data = vars(data)
        response = ResponseModel(data, error)
    return json.dumps(vars(response))

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
    app.run (host='0.0.0.0', port=4000)
