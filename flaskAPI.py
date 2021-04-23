from flask import Flask, request
import os
import urllib.request
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from ContractsOCR import ocrDoc

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"


ALLOWED_EXTENSIONS = set(['pdf'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/file-upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if request.form.get("File"):
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files.get('File')
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resp = jsonify(
            {'message': 'File successfully uploaded :{}'.format(filename),'results':'{}'.format(ocrDoc(filename))})
        # j=ocrDoc(filename)
        return resp
    else:
        resp = jsonify({'message': 'Allowed file type is pdf'})
        resp.status_code = 400
        return resp


if __name__ == '__main__':
    app.run(debug=True)
