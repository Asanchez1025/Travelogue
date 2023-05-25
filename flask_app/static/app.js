const form = document.querySelector("#form-upload")
const progress = document.querySelector(".progress")
const progressBar = document.querySelector(".progress-bar")
const errorMessageDiv = document.querySelector("#error-div")
const successMessageDiv = document.querySelector("#success-div")

function showProgressBar() {
    progress.style.display = 'flex'
}
function setProgressBarPercentage(percentage) {
    progressBar.style.width = `${percentage}%`
}

function showErrorMessage(message){
    errorMessageDiv.innerHTML = message;
    errorMessageDiv.style.display = 'block';
}

function showSuccessMessage(message){
    successMessageDiv.innerHTML = message;
    successMessageDiv.style.display = 'block';
}

form.addEventListener("submit", handleFormSubmission)
function handleFormSubmission(event) {
    event.preventDefault()
    const file = form.querySelector("input[type='file']")



    showProgressBar()
    const  xhr = new XMLHttpRequest()
    xhr.upload.progress.addEventListener("progress", function(event) {
        if (event.lengthComputable) {
            const percentage = Math.floor((event.loaded / event.total) * 100)
            setProgressBarPercentage(percentage)
        }
    })
    

    const formData = new FormData()
    formData.append("my-file", file.files[0])

    xhr.open("POST", "/upload", true)
    xhr.send(formData)
    return false
}

function handleFormSubmission(event) {
    event.preventDefault();
    const input = document.querySelector('input[type="file"]');
    const file = input.files[0];
    console.log(file)

    const formData = new FormData()
    formData.append("my_file", file)


    const xhr = new XMLHttpRequest()
    xhr.onload = function() {
        response = JSON.parse(xhr.response)
        if("error" in response){
            showErrorMessage(response.error)
        }
        else if("success" in response) {
            showSuccessMessage(response.success)
        } else{
            showErrorMessage("Unknown server response")
        }
    };
    xhr.open("POST", "/upload")
    xhr.send(formData)
}