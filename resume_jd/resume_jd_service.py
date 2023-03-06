import os
import json
from docx import Document
import pdfminer
from pdfminer.high_level import extract_text
# import pdfminer.high_level
import io


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


def extract_text(file_path: str) -> str:
    print("FILE FILE : ",file_path)

    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            # Create a StringIO object to store the extracted text
            output_string = io.StringIO()

            # Extract the text using pdfminer
            pdfminer.high_level.extract_text_to_fp(file, output_string)
            # Get the text from the StringIO object
            text = output_string.getvalue()
            return text
    elif file_path.endswith('.docx'):
        text = ''
        document = Document(file_path)
        for paragraph in document.paragraphs:
            text += paragraph.text
        return text
    else:
        print('Unsupported file format')
        return 'unsupported file'

def extract_skills_from_resume(filepath,output_file_path):
    # text = extract_text(filepath)
    # print(text)
    annotations = skill_extractor.annotate(filepath)
    doc_node_values = [item['doc_node_value'] for item in annotations['results']['ngram_scored'] if item['score'] >= 1]
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
    if os.path.exists(output_file_path):
        with open(output_file_path, "r+") as f:
            json_data = json.load(f)
            if json_data:
                f.seek(0)
                f.truncate()
                json.dump(data, f)
    else:
        with open(output_file_path, "w") as f:
            json.dump(data, f)

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

def extract_skills_jd(job_description,company_name,output_file_path)-> dict:
    annotations = skill_extractor.annotate(job_description)
    doc_node_values = [item['doc_node_value'] for item in annotations['results']['ngram_scored'] if item['score'] >= 1]
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
    if os.path.exists(output_file_path):
        with open(output_file_path, "r+") as f:
                    json_data = json.load(f)
                    if json_data:
                        f.seek(0)
                        f.truncate()
                        json.dump(data, f)
    else:
        with open(output_file_path, "w") as f:
            json.dump(data, f)

    responseData =  ResponseData(
        'Data received',
        job_description=job_description,
        company_name=company_name
    )
    return responseData



 # Should be deleted later
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