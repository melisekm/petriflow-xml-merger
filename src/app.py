import json

from flask import Flask, Response, request, render_template
from flask import jsonify

from merge_combinations import merge_from_file

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['xml']


@app.route('/process_form', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        positions = request.form.get('positions')
        if positions is None:
            return jsonify(error=0, error_msg='No positions selected')
        positions = json.loads(positions)
        uploaded_files = request.files.getlist("file[]")
        if len(uploaded_files) < 2:  # file.filename == '':
            return jsonify(error=0, error_msg='Please select at least two files.'), 422
        not_allowed_file_check = (not allowed_file(file.filename) for file in uploaded_files)
        contains_not_allowed_file = any(not_allowed_file_check)
        if contains_not_allowed_file:
            return jsonify(error=0, error_msg='Please select only XML files.'), 422
        xml_read_files = [file.read() for file in uploaded_files]
        try:
            file = merge_from_file(xml_files=xml_read_files, pos_list=positions)
        except Exception as e:
            print(e)
            return jsonify(error=0, error_msg=str(e)), 422
        headers = {
            'Content-Type': 'application/octet-stream',
            'Content-Disposition': 'attachment; filename=merged.xml'
        }
        return Response(file, headers=headers)
    return Response('Something went wrong', 422)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.secret_key = 'the random string'
    app.run(debug=True)
