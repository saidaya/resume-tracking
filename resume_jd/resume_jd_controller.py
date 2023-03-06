# Importing Flask Lib
from flask import Blueprint, jsonify, request
from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin

# Import service and model
from resume_jd.resume_jd_service import extract_skills_from_resume
from resume_jd.resume_jd_service  import extract_skills_jd
from resume_jd.resume_jd_model import ResponseData

#Importing Lib for JSON,DOCX,PDF
import json
import PyPDF2
from io import BytesIO
import docx


# PATH for API route and skills JSON
resume_jd_route_path = 'resume_jd/v1'
resume_jd_route = Blueprint(resume_jd_route_path, __name__)
output_path = '/Users/saidayashankar/Desktop/DAEN690/code/resume-tracking/resume_jd/skills.json'

# API TO GET JOB DESCRIPTION - POST
@resume_jd_route.route("/jd", methods=['POST'])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def extract_jd():
    data = request.get_json()
    job_description = data.get('jd')
    company_name = data.get('company_name')
    extract_skills_jd(job_description,company_name,output_path)
    response_data = ResponseData('Data received', job_description=job_description, company_name=company_name)
    return jsonify(response_data.to_dict())

# API TO EXTRACT SKILLS  - GET
@resume_jd_route.route('/skills', methods=['GET'])
def get_skills():
    try:
        with open(output_path, 'r') as f:
            skills = json.load(f)
            if skills:
                return jsonify(skills)
            else:
                return jsonify({'message': 'No skills found'})
    except FileNotFoundError:
        return jsonify({'error': 'Skills file not found'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API TO GET RESUME - POST
@resume_jd_route.route("/resume", methods=['POST'])
def extract_resume():
    file = request.files['file']
    fileName = file.filename
    print(fileName)
    if fileName.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))
        print("PDF REader",pdf_reader)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        extract_skills_from_resume(text,output_path)
        response_data = {
            'message': 'PDF is uploaded successfully',
            'text': text
        }
        return jsonify(response_data), 200
    elif fileName.endswith('.docx'):
        doc = docx.Document(BytesIO(file.read()))
        text = ''
        for paragraph in doc.paragraphs:
            text += paragraph.text
        print("TEXT : ",text)
        extract_skills_from_resume(text, output_path)
        response_data = {
            'message': 'DOCX is uploaded successfully',
            'text': text
        }
        return jsonify(response_data), 200
    elif fileName.endswith('.txt'):
        text = file.read().decode('utf-8')
        extract_skills_from_resume(text, output_path)
        response_data = {
            'message': 'Text is uploaded successfully',
            'text': text
        }
        return jsonify(response_data), 200
    else:
        response_data = {
            'message': 'Invalid file format'
        }
        return jsonify(response_data), 400


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf','docx'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Should delete later
# file = request.files['file']
    # print("FILE>",file)
    # file_contents = file.read()
    # # file_type = request.file.get('file_type')
    # # file_content = request.files.get('file')
    # # if file_type == 'pdf':
    # pdf_file = file_contents
    # print("pdf_file:",pdf_file)
    # # Create a SimplePDFViewer object and bind it to the PDF file
    # viewer = SimplePDFViewer(pdf_file)
    # # Process each page in the PDF file and extract its text
    # text = ''
    # while True:
    #     try:
    #         viewer.render()
    #     except StopIteration:
    #         break
    #     else:
    #         text += viewer.canvas.text_content
    #
    # print(text)
    # # extract_skills_from_resume(file_content,output_path)
    # response_data = {
    #     'message':'Sucess'
    # }
    # return  response_data, 200

    # try:
    #     response = request.headers
    #     file = request.files['file']
    #     file_contents = file.read()
    #     content_type = response.get('content-type')
    #     print("CONTENT:",content_type)
    #     # If the content type is docx
    #     if 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in content_type:
    #
    #         # Get the text content from the docx file
    #         text = docx2txt.process(response.content)
    #         print("TEXTTTTT:",text)
    #     # If the content type is pdf
    #     elif 'application/pdf' in content_type:
    #
    #         # Read the PDF file
    #         pdf_file = PyPDF2.PdfFileReader(response.content)
    #
    #         # Get the text content from each page of the PDF file
    #         text = ''
    #         for i in range(pdf_file.getNumPages()):
    #             page = pdf_file.getPage(i)
    #             text += page.extractText()
    #
    #     # If the content type is not supported
    #     else:
    #         print('Unsupported content type:', content_type)
    #         text = None
    #
    #     # Print the text content in human-readable format
    #     if text is not None:
    #         print(text)
    #     file = request.files['file']
    #     file_contents = file.read()
    #
    #     # print(file_contents)
    #     # response = extract_skills_from_resume(file_contents,output_path)
    # except KeyError:
    #     return jsonify({'error': 'No file was provided'}), 400
    #
    # if file.filename == '':
    #     return jsonify({'error': 'No file was selected'}), 400
    #
    # if not allowed_file(file.filename):
    #     return jsonify({'error': 'Unsupported file format'}), 400
    #
    # try:
    #     file_contents = file.read()
    #     response_data = {
    #         'message': 'File has been successfully Uploaded'
    #     }
    #     print(response_data)
    # except Exception:
    #     return jsonify({'error': 'Error reading file'}), 500
    #
    # return response_data, 200

