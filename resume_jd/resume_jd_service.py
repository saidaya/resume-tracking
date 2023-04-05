import os
import json
from docx import Document
import pdfminer
from pdfminer.high_level import extract_text
# import pdfminer.high_level
import io
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# SKILLNER
import spacy
from spacy.matcher import PhraseMatcher
# load default skills data base
from skillNer.general_params import SKILL_DB
# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor

# init params of skill extractor
nlp = spacy.load("en_core_web_lg")
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
from resume_jd.resume_jd_model import ResponseData
import pandas as pd


# Method to extract skills from JD - old
def extract_skills_jd(job_description,company_name)-> dict:
    annotations = skill_extractor.annotate(job_description)
    #doc_node_values = [item['doc_node_value'] for item in annotations['results']['ngram_scored'] if item['score'] >= 1]
    doc_node_values = [item['doc_node_value'] for key, value in annotations['results'].items() for item in value if
                        item['score'] >= 1]
    count_dict = {}
    for element in doc_node_values:
        if element in count_dict:
            count_dict[element] += 1
        else:
            count_dict[element] = 1
    sorted_skills = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
    key_skills = [x[0] for x in sorted_skills if x[1] > 1]
    skills_filter = [x[0] for x in sorted_skills if x[1] == 1]
    skills_data = pd.read_csv("/Users/saidayashankar/Desktop/resume_jd_parse/resume_jd/skills_filter.csv")
    df = skills_data.replace(r'\n', '', regex=True)
    df = df.apply(lambda x: x.str.lower())
    skill_list = df["Skill"].values.tolist()
    skill_set = set(skill_list)
    filter_set = set(skills_filter)
    b = list(skill_set.intersection(filter_set))
    for i in b:
        key_skills.append(i)
    data = {
                "skills": key_skills ,
                "format":"JD"
            }
    cwd = os.getcwd()
    file_path = os.path.join(cwd, 'jd_data.json')
    if os.path.isfile(file_path):
        with open(file_path, 'w') as f:
            json.dump(data, f)
    else:
        with open(file_path, 'w') as f:
            json.dump(data, f)

    # if os.path.exists(output_file_path):
    #     with open(output_file_path, "r+") as f:
    #                 json_data = json.load(f)
    #                 if json_data:
    #                     f.seek(0)
    #                     f.truncate()
    #                     json.dump(data, f)
    # else:
    #     with open(output_file_path, "w") as f:
    #         json.dump(data, f)

    responseData =  ResponseData(
        'Data received',
        job_description=job_description,
        company_name=company_name
    )
    return responseData

#Method to extract skills from resume - old
def extract_skills_from_resume(filepath):
    # text = extract_text(filepath)
    # print(text)
    annotations = skill_extractor.annotate(filepath)
    doc_node_values = [item['doc_node_value'] for item in annotations['results']['ngram_scored'] if item['score'] >= 1]
    # doc_node_values = [item['doc_node_value'] for key, value in annotations['results'].items() for item in value if
    #                    item['score'] >= 1]
    count_dict = {}
    for element in doc_node_values:
        if element in count_dict:
            count_dict[element] += 1
        else:
            count_dict[element] = 1
    sorted_skills = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
    key_skills = [x[0] for x in sorted_skills if x[1] > 1]
    skills_filter = [x[0] for x in sorted_skills if x[1] == 1]
    skills_data = pd.read_csv("/Users/saidayashankar/Desktop/resume_jd_parse/resume_jd/skills_filter.csv")
    df = skills_data.replace(r'\n', '', regex=True)
    df = df.apply(lambda x: x.str.lower())
    skill_list = df["Skill"].values.tolist()
    skill_set = set(skill_list)
    filter_set = set(skills_filter)
    b = list(skill_set.intersection(filter_set))
    for i in b:
        key_skills.append(i)
    data = {
        "skills": key_skills,
        "format": "RESUME"
    }

    cwd = os.getcwd()
    file_path = os.path.join(cwd, 'resume_data.json')
    if os.path.isfile(file_path):
        with open(file_path, 'w') as f:
            json.dump(data, f)
    else:
        with open(file_path, 'w') as f:
            json.dump(data, f)

    # if os.path.exists(output_file_path):
    #     with open(output_file_path, "r+") as f:
    #         json_data = json.load(f)
    #         if json_data:
    #             f.seek(0)
    #             f.truncate()
    #             json.dump(data, f)
    # else:
    #     with open(output_file_path, "w") as f:
    #         json.dump(data, f)

    # print("Annotations",annotations)
    # keywords = []
    # for key, value in annotations['results'].items():
    #     for item in value:
    #         if (int(item['score']) >= 0):
    #             keywords.append(item['doc_node_value'])
    #
    # # Format annotations as a dictionary
    # print("Keywords",type(keywords))
    # if isinstance(keywords, list):
    #     data = {
    #         "skills": keywords ,
    #         "format":"JD"
    #     }
    #     print(data)
    #     if os.path.exists(output_file_path):
    #         with open(output_file_path, "r+") as f:
    #             json_data = json.load(f)
    #             if json_data:
    #                 f.seek(0)
    #                 f.truncate()
    #                 json.dump(data, f)
    #     else:
    #         with open(output_file_path, "w") as f:
    #             json.dump(data, f)
    # else:
    #     print("ERROR ")

    # Dump dictionary to JSON file

    #
    # responseData = ResponseData('Data received', job_description=job_description, company_name=company_name)
    # return responseData
    responseData = {
        'message' : 'Skills has been successfully Extracted',
        'skills': data,
        'format':'resume'
    }
    return responseData


# Method to extract skills from JD - New
def extract_skills_jd_1(job_description, company_name):
    if not job_description:
        return {
            "status": 501,
            "message": "No job description provided. No skills to extract."
        }

    try:
        # Load skills data
        skills_data = pd.read_csv("/Users/saidayashankar/Desktop/resume_jd_parse/resume_jd/skills_filter.csv")
        skills_data["Skill"] = skills_data["Skill"].str.lower()
        skill_set = set(skills_data["Skill"].tolist())

        # Extract skills from job description
        annotations = skill_extractor.annotate(job_description)
        doc_node_values = [item["doc_node_value"] for key, value in annotations["results"].items() for item in value if
                           item["score"] >= 1]
        count_dict = {}
        for element in doc_node_values:
            count_dict[element] = count_dict.get(element, 0) + 1
        sorted_skills = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
        key_skills = [x[0] for x in sorted_skills if x[1] > 1]
        skills_filter = [x[0] for x in sorted_skills if x[1] == 1]
        filter_set = set(map(str.lower, skills_filter))

        # Find matching skills
        matching_skills = list(skill_set.intersection(filter_set))
        key_skills.extend(matching_skills)

        # Save skills data as JSON
        data = {
            "skills": key_skills,
            "format": "JD"
        }
        cwd = os.getcwd()
        file_path = os.path.join(cwd, "jd_data.json")
        with open(file_path, "w") as f:
            json.dump(data, f)

        # Create response data object
        response_data = {
            "message": "Data received",
            "job_description": job_description,
            "company_name": company_name,
            "skills": key_skills
        }

        return response_data

    except FileNotFoundError:
        # Handle file not found error
        error_message = "Skills CSV file not found."
        error_data = {
            "message": error_message,
            "job_description": job_description,
            "company_name": company_name
        }
        return error_data

    except Exception as e:
        # Handle any other exceptions
        error_message = "An error occurred while extracting skills: " + str(e)
        error_data = {
            "message": error_message,
            "job_description": job_description,
            "company_name": company_name
        }
        return error_data
# Method to extract skills from Resume - New
def extract_skills_from_resume_1(resume_text):
    if not resume_text:
        # Return error response if resume_text is empty
        error_data = {
            "status": 501,
            "message": "No resume provided. No skills to extract.",
        }
        return error_data

    try:
        # Load skills data
        skills_data = pd.read_csv("/Users/saidayashankar/Desktop/resume_jd_parse/resume_jd/skills_filter.csv")
        skills_data["Skill"] = skills_data["Skill"].str.lower()
        skill_set = set(skills_data["Skill"].tolist())

        # Extract skills from resume
        annotations = skill_extractor.annotate(resume_text)
        doc_node_values = [item["doc_node_value"] for key, value in annotations["results"].items() for item in value
                           if item["score"] >= 1]
        count_dict = {}
        for element in doc_node_values:
            count_dict[element] = count_dict.get(element, 0) + 1
        sorted_skills = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
        key_skills = [x[0] for x in sorted_skills if x[1] > 1]
        skills_filter = [x[0] for x in sorted_skills if x[1] == 1]
        filter_set = set(map(str.lower, skills_filter))

        # Find matching skills
        matching_skills = list(skill_set.intersection(filter_set))
        key_skills.extend(matching_skills)

        # Save skills data as JSON
        data = {
            "skills": key_skills,
            "format": "Resume"
        }
        cwd = os.getcwd()
        file_path = os.path.join(cwd, "resume_data.json")
        with open(file_path, "w") as f:
            json.dump(data, f)

        # Create response data object
        response_data = {
            "status": 200,
            "message": "Data received",
            "resume_text": resume_text,
            "skills": key_skills
        }

        return response_data

    except FileNotFoundError:
        # Handle file not found error
        error_data = {
            "status": 500,
            "message": "Skills CSV file not found.",
            "resume_text": resume_text,
        }
        return error_data

    except Exception as e:
        # Handle any other exceptions
        error_message = "An error occurred while extracting skills: " + str(e)
        error_data = {
            "status": 500,
            "message": error_message,
            "resume_text": resume_text,
        }
        return error_data

#Method to find the score (JD,RESUME) - old
def scorer():
    # pip install -U scikit-learn scipy matplotlib
    with open('jd_data.json') as f1:
        data1 = json.load(f1)
        skills1 = data1['skills']

    with open('resume_data.json') as f2:
        data2 = json.load(f2)
        skills2 = data2['skills']

    # create a list of all skills
    all_skills = list(set(skills1 + skills2))

    # create vectors for each file
    vector1 = np.array([1 if skill in skills1 else 0 for skill in all_skills])
    vector2 = np.array([1 if skill in skills2 else 0 for skill in all_skills])

    # calculate the cosine similarity
    cosine_sim = cosine_similarity(vector1.reshape(1, -1), vector2.reshape(1, -1))[0][0]
    cosine = cosine_sim*100
    print(f"The cosine similarity between the two skill sets is {cosine}")
    return cosine





#Method to find the score (JD,RESUME) - new
def scorer_new():
    try:
        # check if the necessary files are present in the directory
        if not os.path.isfile('jd_data.json'):
            raise FileNotFoundError("File 'jd_data.json' not found in directory.")
        if not os.path.isfile('resume_data.json'):
            raise FileNotFoundError("File 'resume_data.json' not found in directory.")

        # load the data from the JSON files
        with open('jd_data.json') as f1:
            jd_data = json.load(f1)
            jd_skills = jd_data['skills']

        with open('resume_data.json') as f2:
            resume_data = json.load(f2)
            resume_skills = resume_data['skills']

        # combine all skills into a single list and remove duplicates
        all_skills = list(set(jd_skills + resume_skills))

        # create a binary vector for each file, indicating which skills are present
        jd_vector = np.array([1 if skill in jd_skills else 0 for skill in all_skills])
        resume_vector = np.array([1 if skill in resume_skills else 0 for skill in all_skills])

        # calculate the cosine similarity between the two vectors
        cosine_sim = cosine_similarity(jd_vector.reshape(1, -1), resume_vector.reshape(1, -1))[0][0]

        # convert cosine similarity to a percentage and return the result as JSON
        cosine_similarity_percentage = round(cosine_sim * 100, 2)
        response = {'cosine_similarity': cosine_similarity_percentage}

    except FileNotFoundError as e:
        response = {'error': str(e)}

    return response