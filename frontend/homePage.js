
// URL to extract JD skills
const jd_skills = "http://127.0.0.1:5000/resume_jd/v1/jd_skills"
// const jd_skills = "http://ec2-3-144-159-89.us-east-2.compute.amazonaws.com:5000/resume_jd/v1/jd_skills"

// URL to extract resume skills
const resume_skills = "http://127.0.0.1:5000/resume_jd/v1/resume_skills"
// const resume_skills = "http://ec2-3-144-159-89.us-east-2.compute.amazonaws.com:5000/resume_jd/v1/resume_skills"

// URL to fetch Score
const score = "http://127.0.0.1:5000/resume_jd/v1/skills/score"
// const score = "http://ec2-3-144-159-89.us-east-2.compute.amazonaws.com:5000/resume_jd/v1/skills/score"


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
function createList(data,format) {
	console.log("CONSOLE DATA", data.format)
	if (format === 'JD') {
		const dataElement = document.getElementById('data');
		const skills_UL = document.createElement('ol');
		for (let i = 0; i < data.length; i++) {
			const skills_li = document.createElement('li');

			skills_li.innerHTML = data[i];
			skills_UL.appendChild(skills_li);

			dataElement.appendChild(skills_UL);
		}

	} else {
		const dataElement = document.getElementById('data1');
		while (dataElement.firstChild){
			dataElement.removeChild(dataElement.firstChild)
		}
		const skills_UL = document.createElement('ol');
		for (let i = 0; i < data.length; i++) {
			const skills_li = document.createElement('li');

			skills_li.innerHTML = data[i];
			skills_UL.appendChild(skills_li);

			dataElement.appendChild(skills_UL);
		}
	}
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

