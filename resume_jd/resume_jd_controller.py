# Importing Flask Lib
from flask import Blueprint, jsonify, request
from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin

# Import service and model
from resume_jd.resume_jd_service import extract_skills_from_resume_old
from resume_jd.resume_jd_service import extract_skills_from_resume
from resume_jd.resume_jd_service  import extract_skills_jd
from resume_jd.resume_jd_service  import extract_skills_jd_old
from resume_jd.resume_jd_service import scorer
from resume_jd.resume_jd_service import scorer_old
from resume_jd.resume_jd_model import ResponseData

#Importing Lib for JSON,DOCX,PDF
import json
import PyPDF2
from io import BytesIO
import docx
import os


# PATH for API route and skills JSON
resume_jd_route_path = 'resume_jd/v1'
resume_jd_route = Blueprint(resume_jd_route_path, __name__)



#API to get the skills from JD - new
@resume_jd_route.route("/jd_skills", methods=['POST'])
def skills_jd():
    data = request.get_json()
    job_description = data.get('jd')
    company_name = data.get('company_name')
    skills = extract_skills_jd(job_description, company_name)
    if "status" in skills:
        # If extract_skills_jd_1 function returns an error
        response_data = {
            'company_name': company_name,
            'job_description': job_description,
            'message': skills["message"]
        }
        return jsonify(response_data), 500  # Internal Server Error status code

    # If extract_skills_jd_1 function returns skills data
    response_data = {
        'company_name': company_name,
        'job_description': job_description,
        'skills': skills['skills']
    }
    print(response_data)
    return jsonify(response_data)

#API to get the skills from Resume -new
@resume_jd_route.route('/resume_skills', methods=['POST'])
def skills_resume():
    # Check if the file was uploaded
    if 'file' not in request.files:
        response_data = {
            'message': 'No file part in the request'
        }
        return jsonify(response_data), 400

    uploaded_file = request.files['file']
    file_name = uploaded_file.filename

    # Check if the filename is valid
    if not file_name or '.' not in file_name or file_name.rsplit('.', 1)[1].lower() not in ['pdf', 'docx', 'txt']:
        response_data = {
            'message': 'Invalid file format'
        }
        return jsonify(response_data), 400

    # Read the uploaded file based on its type
    if file_name.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
        resume_text = ''
        for page in pdf_reader.pages:
            resume_text += page.extract_text()
    elif file_name.endswith('.docx'):
        doc = docx.Document(BytesIO(uploaded_file.read()))
        resume_text = ''
        for paragraph in doc.paragraphs:
            resume_text += paragraph.text
    elif file_name.endswith('.txt'):
        resume_text = uploaded_file.read().decode('utf-8')
    else:
        response_data = {
            'message': 'Invalid file format'
        }
        return jsonify(response_data), 400

    # Extract skills from the resume text
    skills_response = extract_skills_from_resume(resume_text)

    # Check if there was an error extracting skills
    if "status" in skills_response and skills_response["status"] != 200:
        return jsonify(skills_response), skills_response["status"]

    # Prepare the response
    response_data = {
        'message': f'{file_name} is uploaded successfully',
        'resume_text': resume_text,
        'skills': skills_response["skills"]
    }
    return jsonify(response_data), 200

#API to get cosine Simmilarity: - new
@resume_jd_route.route('/skills/score', methods=['GET'])
def get_score_new():
    try:
        cosine_score = scorer()['cosine_similarity']
        return jsonify({
            'message': 'Success',
            'score': cosine_score,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#API to get JD- -old
@resume_jd_route.route("/jd", methods=['POST'])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def extract_jd():
    data = request.get_json()
    job_description = data.get('jd')
    company_name = data.get('company_name')
    extract_skills_jd_old(job_description,company_name)
    response_data = ResponseData('Data received', job_description=job_description, company_name=company_name)
    return jsonify(response_data.to_dict())

#API to get resume - -old
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
        extract_skills_from_resume_old(text)
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
        extract_skills_from_resume_old(text)
        response_data = {
            'message': 'DOCX is uploaded successfully',
            'text': text
        }
        return jsonify(response_data), 200
    elif fileName.endswith('.txt'):
        text = file.read().decode('utf-8')
        extract_skills_from_resume_old(text)
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

#API to show the extracted skills JD -old
@resume_jd_route.route('/skills/jd', methods=['GET'])
def get_skills_jd():
    jd_filename = os.path.join(os.getcwd(), 'jd_data.json')

    # check if files exist
    if not os.path.exists(jd_filename):
        return jsonify({'error': 'Skills file not found'})


    # check filename and load JSON data from file
    if 'jd_data' in jd_filename:
        message = 'JD SKills'
        with open(jd_filename, 'r') as f:
            data = json.load(f)
    else:
        return jsonify({'error': 'SKills not available'})
    # return JSON data and message
    return jsonify({'message': message, 'data': data})

    #     with open(output_path, 'r') as f:
    #         skills = json.load(f)
    #         if skills:
    #             return jsonify(skills)
    #         else:
    #             return jsonify({'message': 'No skills found'})
    # except FileNotFoundError:
    #     return jsonify({'error': 'Skills file not found'})
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

#API to show the extracted skills resume -old
@resume_jd_route.route('/skills/resume', methods=['GET'])
def get_skills_resume():
    resume_filename = os.path.join(os.getcwd(), 'resume_data.json')
    # check if files exist
    if not os.path.exists(resume_filename):
        return jsonify({'error': 'Resume Skills not found'})
    # check filename and load JSON data from file

    if 'resume_data' in resume_filename:
        message = 'Resume data loaded'
        with open(resume_filename, 'r') as f:
            data = json.load(f)
    else:
        return jsonify({'error': 'No Skills to be displayed'})
    # return JSON data and message
    return jsonify({'message': message, 'data': data})

    #     with open(output_path, 'r') as f:
    #         skills = json.load(f)
    #         if skills:
    #             return jsonify(skills)
    #         else:
    #             return jsonify({'message': 'No skills found'})
    # except FileNotFoundError:
    #     return jsonify({'error': 'Skills file not found'})
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

#API to get cosine Simmilarity: - old
@resume_jd_route.route('/skills/score_old', methods=['GET'])
def get_score_old():
    try:
        cosine_score = scorer_old()
        return jsonify({
            'message':'Success',
            'score':cosine_score,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


