let cancelButton;
let okButton;
let deleteButton;
let editButton;
let oldFormData;


function handleCancelButtonDuringEdit() {
    setReadOnly(true, "#form-exercise");
    okButton.className += " hide";
    deleteButton.className += " hide";
    cancelButton.className += " hide";
    editButton.className = editButton.className.replace(" hide", "");

    cancelButton.removeEventListener("click", handleCancelButtonDuringEdit);

    let form = document.querySelector("#form-exercise");
    if (oldFormData.has("name")) form.name.value = oldFormData.get("name");
    if (oldFormData.has("description")) form.description.value = oldFormData.get("description");
    if (oldFormData.has("unit")) form.unit.value = oldFormData.get("unit");
    
    oldFormData.delete("name");
    oldFormData.delete("description");
    oldFormData.delete("unit");

}

function handleCancelButtonDuringCreate() {
    window.location.replace("exercises.html");
}

async function createExercise() {
    let form = document.querySelector("#form-exercise");
    let formData = new FormData(form);
    let body = {"name": formData.get("name"), 
                "description": formData.get("description"), 
                "unit": formData.get("unit")};

    let response = await sendRequest("POST", `${HOST}/api/exercises/`, body);

    if (response.ok) {
        window.location.replace("exercises.html");
    } else {
        let data = await response.json();
        let alert = createAlert("Could not create new exercise!", data);
        document.body.prepend(alert);
    }
}

function handleEditExerciseButtonClick() {
    setReadOnly(false, "#form-exercise");

    editButton.className += " hide";
    okButton.className = okButton.className.replace(" hide", "");
    cancelButton.className = cancelButton.className.replace(" hide", "");
    deleteButton.className = deleteButton.className.replace(" hide", "");

    cancelButton.addEventListener("click", handleCancelButtonDuringEdit);

    let form = document.querySelector("#form-exercise");
    oldFormData = new FormData(form);
}

async function deleteExercise(id) {
    let response = await sendRequest("DELETE", `${HOST}/api/exercises/${id}/`);
    if (!response.ok) {
        let data = await response.json();
        let alert = createAlert(`Could not delete exercise ${id}`, data);
        document.body.prepend(alert);
    } else {
        window.location.replace("exercises.html");
    }
}

async function retrieveExercise(id) {
    let response = await sendRequest("GET", `${HOST}/api/exercises/${id}/`);
    console.log(response.ok);
    if (!response.ok) {
        let data = await response.json();
        let alert = createAlert("Could not retrieve exercise data!", data);
        document.body.prepend(alert);
    } else {
        let exerciseData = await response.json();
        let form = document.querySelector("#form-exercise");
        let formData = new FormData(form);

        for (let key of formData.keys()) {
            let selector = `input[name="${key}"], textarea[name="${key}"]`;
            let input = form.querySelector(selector);
            let newVal = exerciseData[key];
            input.value = newVal;
        }
    }
}

async function updateExercise(id) {
    let form = document.querySelector("#form-exercise");
    let formData = new FormData(form);
    let body = {"name": formData.get("name"), 
                "description": formData.get("description"), 
                "unit": formData.get("unit")};
    let response = await sendRequest("PUT", `${HOST}/api/exercises/${id}/`, body);

    if (!response.ok) {
        let data = await response.json();
        let alert = createAlert(`Could not update exercise ${id}`, data);
        document.body.prepend(alert);
    } else {
        // duplicate code from handleCancelButtonDuringEdit
        // you should refactor this
        setReadOnly(true, "#form-exercise");
        okButton.className += " hide";
        deleteButton.className += " hide";
        cancelButton.className += " hide";
        editButton.className = editButton.className.replace(" hide", "");
    
        cancelButton.removeEventListener("click", handleCancelButtonDuringEdit);
        
        oldFormData.delete("name");
        oldFormData.delete("description");
        oldFormData.delete("unit");
    }
}

async function fetchLeaderBoards() {
    //let response = await sendRequest("GET", `${HOST}/api/exercises/${id}/getLeaderBoards`);
    //Placeholder response and status:
    let response = [{"name": "Mark", "value": 301, "rank": 1},
    {"name": "Anton", "value": 245, "rank": 2},
    {"name": "John", "value": 112, "rank": 3},
    {"name": "Joe", "value": 84, "rank": 4},
    {"name": "Larry", "value": 80, "rank": 5},
    {"name": "Glaum", "value": 1, "rank": 85}];
    response.ok = true;

    if (response.ok) {

        let table = document.getElementById("leaderboardstable");
        let row, cell;

        //The users own score will always be placed last in the JSON response
        let userIndex = response.length - 1;

        for (let i = 0; i < response.length-1; i++) {
            row = table.insertRow();
            cell = row.insertCell();
            cell.textContent = response[i].rank;
            cell = row.insertCell();
            cell.textContent = response[i].name;
            cell = row.insertCell();
            cell.textContent = response[i].value;
          }
        //If the user is not in top 5, the users score will also be rendered
        if(response[userIndex].rank > 5){
            row = table.insertRow();
            cell = row.insertCell();
            cell.textContent = response[userIndex].rank;
            cell = row.insertCell();
            cell.textContent = response[userIndex].name;
            cell = row.insertCell();
            cell.textContent = response[userIndex].value;
        }
    }

    return response;
}

window.addEventListener("DOMContentLoaded", async () => {
    cancelButton = document.querySelector("#btn-cancel-exercise");
    okButton = document.querySelector("#btn-ok-exercise");
    deleteButton = document.querySelector("#btn-delete-exercise");
    editButton = document.querySelector("#btn-edit-exercise");
    oldFormData = null;

    const urlParams = new URLSearchParams(window.location.search);

    // view/edit
    if (urlParams.has('id')) {
        const exerciseId = urlParams.get('id');
        await retrieveExercise(exerciseId);

        editButton.addEventListener("click", handleEditExerciseButtonClick);
        deleteButton.addEventListener("click", (async (id) => await deleteExercise(id)).bind(undefined, exerciseId));
        okButton.addEventListener("click", (async (id) => await updateExercise(id)).bind(undefined, exerciseId));
    } 
    //create
    else {
        setReadOnly(false, "#form-exercise");

        editButton.className += " hide";
        okButton.className = okButton.className.replace(" hide", "");
        cancelButton.className = cancelButton.className.replace(" hide", "");

        okButton.addEventListener("click", async () => await createExercise());
        cancelButton.addEventListener("click", handleCancelButtonDuringCreate);
    }

    await fetchLeaderBoards();
});