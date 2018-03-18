from flask import Flask, jsonify, request, render_template
from werkzeug import secure_filename
import os

from utils import allowed_file, convert_html_to_pdf, convert_doc_to_pdf

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """ Renders Index.html """
    try:
        return render_template('index.html')
    except Exception as e:
        print("Exception Occurred", e)
        return jsonify({"status": "failed", "message": "Something Went Wrong !!"})


@app.route('/upload', methods=['POST'])
def file_converter():
    """
    Function Processing Steps:
    Step-1 : Check uploaded file extension ,if accepted format process further
    Step-2 : Save the files into uploads folder
    Step-3 : Convert the html,doc and docx files into pdf file and stores into converted_files folder

    Note :  If file is already in pdf format than file will directly save in converted_files
            folder without other action.
    """
    if request.method == "POST":
        try:
            files = request.files.getlist('file')
            print("files", files)
            if len(files) > 0:
                for data in files:
                    if allowed_file(data.filename):
                        filename = secure_filename(data.filename)
                        extension = filename.split('.')
                        file_path = os.path.join('static/uploads', filename)

                        if extension[-1] == 'pdf':
                            pdf_file_path = os.path.join('static/converted_files', filename)
                            data.save(pdf_file_path)
                        else:
                            data.save(file_path)

                        if extension[-1] == 'html':
                            if convert_html_to_pdf(file_path, extension[0]):
                                print("File Converted to PDF Successfully !!")
                            else:
                                raise Exception('Something Went Wrong !')

                        elif extension[-1] == "docx" or extension[-1] == "doc":
                            if convert_doc_to_pdf(file_path):
                                print("File Converted to PDF Successfully !!")
                            else:
                                raise Exception('Something Went Wrong !')
                        return jsonify({"status": "success", "message": "File Uploaded Successfully !!"})

                    else:
                        return jsonify({"status": "failed", "message": "Format Not Allowed !!"})
            else:
                return jsonify({"status": "failed"})
        except Exception as e:
            print("Exception Occurred", e)
            return jsonify({"status": "exception", "message": "Something Went Wrong !!"})
    else:
        return jsonify({"status": "failed", "message": "Method Not Allowed !"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
