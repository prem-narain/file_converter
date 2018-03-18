from weasyprint import HTML,CSS
from uuid import uuid4
import os
import subprocess

ALLOWED_EXTENSIONS = set(['doc', 'docx', 'pdf', 'html'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def convert_html_to_pdf(file_path, file_name):
    try:
        random_string = str(uuid4())[:10]
        HTML(file_path).write_pdf(os.path.join('static/converted_files',
                                               file_name+'_'+random_string+'.pdf'),
                                  stylesheets=[CSS(string='body { font-family: serif !important;margin-left:-80px; }')])
    except Exception as e:
        print("Exception Occurred", e)
        return False
    return True


def convert_doc_to_pdf(file_path):
    try:
        subprocess.call(['soffice', '--headless', '--convert-to', 'pdf',
                         "--outdir", 'static/converted_files', file_path])
    except Exception as e:
        print("Exception Occurred", e)
        return False
    return True
