
// URL to extract JD skills
const jd_skills = "http://127.0.0.1:5000/resume_jd/v1/jd_skills"
// const jd_skills = "http://ec2-3-144-159-89.us-east-2.compute.amazonaws.com:5000/resume_jd/v1/jd_skills"

// URL to extract resume skills
const resume_skills = "http://127.0.0.1:5000/resume_jd/v1/resume_skills"
// const resume_skills = "http://ec2-3-144-159-89.us-east-2.compute.amazonaws.com:5000/resume_jd/v1/resume_skills"

// URL to fetch Score
const score = "http://127.0.0.1:5000/resume_jd/v1/skills/score"
// const score = "http://ec2-3-144-159-89.us-east-2.compute.amazonaws.com:5000/resume_jd/v1/skills/score"

// URL to fetch SCore New Method
const score_files = 'http://127.0.0.1:5000/resume_jd/v1/skills/score/files'
// const score_files = "http://ec2-3-144-159-89.us-east-2.compute.amazonaws.com:5000/resume_jd/v1/skills/score/files"

const request = new XMLHttpRequest();
const fileInput = document.getElementById('fileInput');
const message = document.getElementById('message')
let response_ = ''

// JD skills - Response
function submitForm(event) {

    const form = document.getElementById('myForm');
    event.preventDefault(); // prevent form submission
    let job_description = document.getElementById("job_description").value; // get input text value
    let company_name = document.getElementById("company_name").value; // get input text value

    fetch(jd_skills , {
        mode: 'cors',
        method: "POST",
        body: JSON.stringify({
            jd: job_description,
            company_name : company_name
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(
            response => {
                console.log("Response 1",response);
                form.reset()
                return response.json();
            },
        )
        .then(response => {
            // Store the response data in a variable
            console.log("Response 2",response);
            console.log("Response 2",response.skills);
            createList(response.skills,"JD")
            // Do something with the response data
        })
        .catch(error => console.error(error));

}

// Resume - Response
async function uploadFile() {
    const input = document.getElementById('fileInputt');
    let file = input.files[0];
    console.log("FILE RESUME:",file)
    let formData = new FormData();
    formData.append("file", input.files[0]);

    await fetch(resume_skills, {
        method: "POST",
        body: formData
    })
        .then(response => {
            if (response.ok) {
                console.log(response)
                // getResponse();
                return response.json();
            } else {
                throw new Error('Error occurred: ' + response.statusText);
            }
        })
        .then(data => {
            // message.innerHTML = data.message;
            createList(data.skills,"RESUME")
            console.log("DATA", data.message);
        })
        .catch(error => {
            if (error.response) {
                console.error('API error:', error.response.data);
            } else if (error.request) {
                console.error('No response received:', error.request);
            } else {
                console.error('Error occurred:', error.message);
            }
        });
}

// To get Score
function showScore() {
    fetch(score)
        .then(response => response.json())
        .then(data => {
            const score = data.score // convert score to percentage
            const scoreDiv = document.getElementById('score');
            scoreDiv.innerText = score.toFixed(2) + "%"; // format percentage with 2 decimal places
        })
        .catch(error => console.error(error));
}

// Dynamically creating Skills tag
// function createList(data,format) {
//     console.log("CONSOLE DATA", data.format)
//     if (format === 'JD') {
//         const dataElement = document.getElementById('data');
//         const skills_UL = document.createElement('ol');
//         for (let i = 0; i < data.length; i++) {
//             const skills_li = document.createElement('li');
//
//             skills_li.innerHTML = data[i];
//             skills_UL.appendChild(skills_li);
//
//             dataElement.appendChild(skills_UL);
//         }
//
//     } else {
//         const dataElement = document.getElementById('data1');
//         while (dataElement.firstChild){
//             dataElement.removeChild(dataElement.firstChild)
//         }
//         const skills_UL = document.createElement('ol');
//         for (let i = 0; i < data.length; i++) {
//             const skills_li = document.createElement('li');
//
//             skills_li.innerHTML = data[i];
//             skills_UL.appendChild(skills_li);
//
//             dataElement.appendChild(skills_UL);
//         }
//     }
// }

function createList(data, format) {
    console.log("CONSOLE DATA", data.format);
    const dataElement = format === "JD" ? document.getElementById("data") : document.getElementById("data1");

    // Remove all child nodes before appending the new list
    while (dataElement.firstChild) {
        dataElement.removeChild(dataElement.firstChild);
    }

    const skills_UL = document.createElement("ol");
    skills_UL.classList.add("ol-style"); // Add the class name "ol-style" to the ordered list element
    for (let i = 0; i < data.length; i++) {
        const skills_li = document.createElement("li");
        skills_li.classList.add("li-style"); // Add the class name "li-style" to each list item element
        skills_li.innerHTML = data[i];
        skills_UL.appendChild(skills_li);
    }

    dataElement.appendChild(skills_UL);
}



// To clear JD and Resume skills
function clearSkills(){
    console.log(response_)
    const skills_data = document.getElementById('data1');
    while (skills_data.firstChild){
        skills_data.removeChild(skills_data.firstChild)
    }
}
function clearSkills2(){
    const skills_data = document.getElementById('data');
    while (skills_data.firstChild){
        skills_data.removeChild(skills_data.firstChild)
    }
}

// API to get the DISPLAY
async function getResponse() {
    await fetch('http://ec2-18-217-91-251.us-east-2.compute.amazonaws.com:5000/resume_jd/v1/skills',
        {method: 'GET'})
        .then(response => response.json())
        .then(data => createList(data))
        .catch(error => console.error(error));
}
// Upload FIle - API


// Method to submit Score form

// async function submitFormScore(event) {
//     // const input = document.getElementById('resumeInput');
//     // let file = input.files[0];
//     // let formData = new FormData();
//     // formData.append("file", input.files[0]);
//     //
//     // const form = document.getElementById('scoringForm');
//     // event.preventDefault(); // prevent form submission
//     // let job_description = document.getElementById("jd").value; // get input text value
//
//
//     const input = document.getElementById('resumeInput');
//     const file = input.files[0];
//     const formData = new FormData();
//     formData.append("resume", file);
//
//     const form = document.getElementById('scoringForm');
//     event.preventDefault(); // prevent form submission
//     const job_description = document.getElementById("jd").value; // get input text value
//     formData.append('jd', JSON.stringify({ 'jd': job_description }));
//     // formData.append('resume', file);
//     console.log("DATA::::",formData)
//     await fetch(score_files, {
//         mode: 'cors',
//         method: "POST",
//         body: formData
//     })
//         .then(response => {
//             if (response.ok) {
//                 console.log(response)
//                 return response.json();
//             } else {
//                 throw new Error('Error occurred: ' + response.statusText);
//             }
//         })
//         .then(data => {
//             console.log("DATA:",data)
//         })
//         .catch(error => {
//             if (error.response) {
//                 console.error('API error:', error.response.data);
//             } else if (error.request) {
//                 console.error('No response received:', error.request);
//             } else {
//                 console.error('Error occurred:', error.message);
//             }
//         });
//
//
// }

async function submitFormScore() {
    event.preventDefault()

    const formData = new FormData();

    const jobDescription = document.getElementById('jd').value;
    console.log("JD",jobDescription)
    if (!jobDescription) {
        console.error('No job description provided');
        return;
    }
    const input = document.getElementById('resumeInput');
    const file = input.files[0];

    if (!file) {
        console.error('No resume file selected');
        return;
    }
    formData.append('jd', jobDescription);
    formData.append('resume', file);


    try {
        const response = await fetch(score_files, {
            method: 'POST',
            mode: 'cors',
            body:  formData,
        });

        if (response.ok) {
            const data = await response.json();
            const container = document.createElement('div');
            container.classList.add('container');

            const card = document.createElement('div');
            card.classList.add('card');

            const cardHeader = document.createElement('div');
            cardHeader.classList.add('card-header');

            const header = document.createElement('h2');
            header.textContent = 'Similarity Score';

            const cardBody = document.createElement('div');
            cardBody.classList.add('card-body');

            const score = document.createElement('h1');
            score.id = 'score';
            score.classList.add('center');
            score.textContent = `${data.skills_score.toFixed(2)}%`;

            cardHeader.appendChild(header);
            cardBody.appendChild(score);
            card.appendChild(cardHeader);
            card.appendChild(cardBody);
            container.appendChild(card);

            const skillSection = document.getElementById('skill_extraction');
            skillSection.appendChild(container);

        } else {
            console.error('Error occurred:', response.statusText);
        }
    } catch (error) {
        console.error('API error:', error.message);
    }
}
