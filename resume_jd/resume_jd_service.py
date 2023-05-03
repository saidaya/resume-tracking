import os
import json
from docx import Document
import pdfminer
from pdfminer.high_level import extract_text
# import pdfminer.high_level
import io
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from resume_jd.resume_jd_model import ResponseData
import pandas as pd
import sys
import spacy
from spacy.matcher import PhraseMatcher
# import skill extractor code
from src.skill_extractor_class import SkillExtractor
# load default skills data base
from src.general_params import SKILL_DB
# init params of skill extractor
nlp = spacy.load("en_core_web_lg")
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)


current_dir = os.getcwd()
skills_filter_file = os.path.join(current_dir,'resume_jd', 'skills_filter.csv')

# Methods to extract SKILLS from JD and RESUME - new
# Method to extract skills from JD - New
def extract_skills_jd(job_description, company_name):
    if not job_description:
        return {
            "status": 501,
            "message": "No job description provided. No skills to extract."
        }

    try:
        skill_data = pd.read_csv(skills_filter_file)
        skill_data["Skill"] = skill_data["Skill"].str.lower()
        skill_set = set(skill_data["Skill"].tolist())

        # # Extract skills from resume
        # annotations = skill_extractor.annotate(job_description)
        # doc_node_values = [item['doc_node_value'] for item in annotations['results']['ngram_scored'] if
        #                    item['score'] >= 1]
        # full_match = [item['doc_node_value'] for item in annotations['results']['full_matches']]
        #
        # # Add full matches to the key skills list
        # # key_skills = list(set(doc_node_values + full_match))
        # for i in full_match:
        #     doc_node_values.append(i)
        # count_dict = {}
        # for element in doc_node_values:
        #     if element in count_dict:
        #         count_dict[element] += 1
        #     else:
        #         count_dict[element] = 1
        # sorted_skills = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
        # print("Sorted Skills:", sorted_skills)
        # key_skills = [x[0] for x in sorted_skills if x[1] > 1]
        # for i in full_match:
        #     key_skills.append(i)
        # print("Key skills:", key_skills)
        # skills_filter = [x[0] for x in sorted_skills if x[1] == 1]
        # filter_set = set(map(str.lower, skills_filter))
        #
        # # Find matching skills
        # matching_skills = list(skill_set.intersection(filter_set))
        # print("Matching SKills:", matching_skills)
        # key_skills.extend(matching_skills)
        # print("Key SKills Final :", key_skills)
        #
        # Save skills data as JSON

        #### Testing ....


        # Extract skills from resume
        annotations = skill_extractor.annotate(job_description)
        matched_phrases = [item['doc_node_value'] for item in annotations['results']['ngram_scored'] if
                           item['score'] >= 1]
        full_matches = [item['doc_node_value'] for item in annotations['results']['full_matches']]
        matched_phrases += full_matches

        # Count the occurrences of each matched phrase
        phrase_counts = {}
        for phrase in matched_phrases:
            # Use default dict to simplify the counting process
            phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1

        # Sort the phrases by frequency and extract the most frequent ones as key phrases
        sorted_phrases = sorted(phrase_counts.items(), key=lambda x: x[1], reverse=True)
        key_phrases = [x[0] for x in sorted_phrases if x[1] > 1]
        key_phrases += full_matches
        key_phrases = list(set(key_phrases))

        # Find all unmatched phrases and filter them against a list of known skills
        unmatched_phrases = [x[0] for x in sorted_phrases if x[1] == 1]
        # Convert all skills to lowercase for case-insensitive matching
        skill_data = skill_data.apply(lambda x: x.str.lower())
        skill_set = set(skill_data["Skill"].tolist())
        unmatched_set = set(unmatched_phrases)
        # Find the intersection of the unmatched phrases and known skills to identify key skills
        key_phrases += list(skill_set.intersection(unmatched_set))
        key_phrases = list(set(key_phrases))

        data = {
            "skills": key_phrases,
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
            "skills": key_phrases
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
def extract_skills_from_resume(resume_text):
    if not resume_text:
        # Return error response if resume_text is empty
        error_data = {
            "status": 501,
            "message": "No resume provided. No skills to extract.",
        }
        return error_data

    try:
        # # Load skills data
        # skills_data = pd.read_csv(skills_filter_file)
        # skills_data["Skill"] = skills_data["Skill"].str.lower()
        # skill_set = set(skills_data["Skill"].tolist())
        #
        # # Extract skills from resume
        # annotations = skill_extractor.annotate(resume_text)
        # doc_node_values = [item['doc_node_value'] for item in annotations['results']['ngram_scored'] if
        #                           item['score'] >= 1]
        # full_match = [item['doc_node_value'] for item in annotations['results']['full_matches']]
        #
        # # Add full matches to the key skills list
        # # key_skills = list(set(doc_node_values + full_match))
        # for i in full_match:
        #     doc_node_values.append(i)
        # count_dict = {}
        # for element in doc_node_values:
        #     if element in count_dict:
        #         count_dict[element] += 1
        #     else:
        #         count_dict[element] = 1
        # sorted_skills = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
        # print("Sorted Skills:",sorted_skills)
        # key_skills = [x[0] for x in sorted_skills if x[1] > 1]
        # for i in full_match:
        #     key_skills.append(i)
        # print("Key skills:",key_skills)
        # skills_filter = [x[0] for x in sorted_skills if x[1] == 1]
        # filter_set = set(map(str.lower, skills_filter))
        #
        # # Find matching skills
        # matching_skills = list(skill_set.intersection(filter_set))
        # print("Matching SKills:",matching_skills)
        # key_skills.extend(matching_skills)
        # print("Key SKills Final :",key_skills)

        # Testing ......
        # Load skills data
        skill_data = pd.read_csv(skills_filter_file)
        skill_data["Skill"] = skill_data["Skill"].str.lower()
        skill_set = set(skill_data["Skill"].tolist())

        # Extract skills from resume
        annotations = skill_extractor.annotate(resume_text)
        print("Annotations",annotations)
        matched_phrases = [item['doc_node_value'] for item in annotations['results']['ngram_scored'] if
                           item['score'] >= 1]
        print("matched_phrases:", matched_phrases)
        full_matches = [item['doc_node_value'] for item in annotations['results']['full_matches']]
        print("full_matches:", full_matches)
        matched_phrases += full_matches
        print("matched_phrases:", matched_phrases)

        # Count the occurrences of each matched phrase
        phrase_counts = {}
        for phrase in matched_phrases:
            # Use defaultdict to simplify the counting process
            phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1

        # Sort the phrases by frequency and extract the most frequent ones as key phrases
        sorted_phrases = sorted(phrase_counts.items(), key=lambda x: x[1], reverse=True)
        print("sorted_phrases:", sorted_phrases)
        key_phrases = [x[0] for x in sorted_phrases if x[1] > 1]
        key_phrases += full_matches
        key_phrases = list(set(key_phrases))
        print("key_phrases:", key_phrases)

        # Find all unmatched phrases and filter them against a list of known skills
        unmatched_phrases = [x[0] for x in sorted_phrases if x[1] == 1]
        # Convert all skills to lowercase for case-insensitive matching
        skill_data = skill_data.apply(lambda x: x.str.lower())
        skill_set = set(skill_data["Skill"].tolist())
        unmatched_set = set(unmatched_phrases)
        # Find the intersection of the unmatched phrases and known skills to identify key skills
        key_phrases += list(skill_set.intersection(unmatched_set))
        key_phrases = list(set(key_phrases))
        # Save skills data as JSON
        data = {
            "skills": key_phrases,
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
            "skills": key_phrases
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

#Method to find the score (JD,RESUME) - new
def scorer():
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



#Method to extract skills

def skillExtraction(text):
    try:
        skill_data = pd.read_csv(skills_filter_file)
        skill_data["Skill"] = skill_data["Skill"].str.lower()
        skill_set = set(skill_data["Skill"].tolist())

        # Extract skills from resume
        annotations = skill_extractor.annotate(text)
        print("Annotations", annotations)
        matched_phrases = [item['doc_node_value'] for item in annotations['results']['ngram_scored'] if
                           item['score'] >= 1]
        print("matched_phrases:", matched_phrases)
        full_matches = [item['doc_node_value'] for item in annotations['results']['full_matches']]
        print("full_matches:", full_matches)
        matched_phrases += full_matches
        print("matched_phrases:", matched_phrases)

        # Count the occurrences of each matched phrase
        phrase_counts = {}
        for phrase in matched_phrases:
            # Use defaultdict to simplify the counting process
            phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1

        # Sort the phrases by frequency and extract the most frequent ones as key phrases
        sorted_phrases = sorted(phrase_counts.items(), key=lambda x: x[1], reverse=True)
        print("sorted_phrases:", sorted_phrases)
        key_phrases = [x[0] for x in sorted_phrases if x[1] > 1]
        key_phrases += full_matches
        key_phrases = list(set(key_phrases))
        print("key_phrases:", key_phrases)

        # Find all unmatched phrases and filter them against a list of known skills
        unmatched_phrases = [x[0] for x in sorted_phrases if x[1] == 1]
        # Convert all skills to lowercase for case-insensitive matching
        skill_data = skill_data.apply(lambda x: x.str.lower())
        skill_set = set(skill_data["Skill"].tolist())
        unmatched_set = set(unmatched_phrases)
        # Find the intersection of the unmatched phrases and known skills to identify key skills
        key_phrases += list(skill_set.intersection(unmatched_set))
        key_phrases = list(set(key_phrases))
        # Save skills data as JSON
        data = {
            "skills": key_phrases,
        }
        return data

    except FileNotFoundError:
        # Handle file not found error
        error_data = {
            "status": 500,
            "message": "Skills CSV file not found.",
        }
        return error_data
    except Exception as e:
        # Handle any other exceptions
        error_message = "An error occurred while extracting skills: " + str(e)
        error_data = {
            "status": 500,
            "message": error_message,
        }
        return error_data


#Method to get score from JD and REsume : NEW FILES

def matchingScore(job_text,resume_text):
    if not resume_text:
        # Return error response if resume_text is empty
        error_data = {
            "status": 501,
            "message": "No resume provided. No skills to extract.",
        }
        return error_data
    if not job_text:
        return {
            "status": 501,
            "message": "No job description provided. No skills to extract."
        }

    try:

        jd_skills_extracted = skillExtraction(job_text)
        resume_skills_extracted = skillExtraction(resume_text)

        jd_skills = jd_skills_extracted['skills']
        resume_skills = resume_skills_extracted['skills']

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




