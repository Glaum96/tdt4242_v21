async function fetchWorkouts(ordering) {
    let response = await sendRequest("GET", `${HOST}/api/workouts/?ordering=${ordering}`);

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    } else {
        let data = await response.json();

        let workouts = data.results;
        let container = document.getElementById('div-content');

        for(const workout of workouts){

            let workoutLikes = await sendRequest("GET", `${HOST}/api/workoutLiking/${workout.id}`);

            let workoutLikesData = [true, 1]

            if(workoutLikes.ok){
                workoutLikesData = await workoutLikes.json()
            }

            let templateWorkout = document.querySelector("#template-workout");
            let cloneWorkout = templateWorkout.content.cloneNode(true);

            let aWorkout = cloneWorkout.querySelector("a");
            aWorkout.href = `workout.html?id=${workout.id}`;

            let h5 = aWorkout.querySelector("h5");
            h5.textContent = workout.name;

            let localDate = new Date(workout.date);

            let table = aWorkout.querySelector("table");
            let rows = table.querySelectorAll("tr");
            rows[0].querySelectorAll("td")[1].textContent = localDate.toLocaleDateString(); // Date
            rows[1].querySelectorAll("td")[1].textContent = localDate.toLocaleTimeString(); // Time
            rows[2].querySelectorAll("td")[1].textContent = workout.owner_username; //Owner
            rows[3].querySelectorAll("td")[1].textContent = workout.exercise_instances.length; // Exercises

            rows[4].querySelectorAll("td")[1].textContent = workoutLikesData[1]

            let likeButton = rows[4].querySelectorAll("td")[2].querySelector(".like-button")

            if(!workoutLikesData[0]){
                likeButton.classList.add("active")
            }

            likeButton.addEventListener("click", async function(e) {
                e.preventDefault();

                if(!this.classList.contains("active")){
                    this.classList.add("active");
                    this.classList.add("animated");
                    generateClones(this);

                    let likeWorkoutResponse = await sendRequest("POST", `${HOST}/api/workoutLiking/${workout.id}/`, {});

                    if(likeWorkoutResponse.ok){
                        let likeWorkoutData = await likeWorkoutResponse.json()
                        rows[4].querySelectorAll("td")[1].textContent = likeWorkoutData[1]
                        likeButton.classList.add("active")
                    }
                }
            })


            container.appendChild(aWorkout);
        }
        return workouts;
    }
}

function createWorkout() {
    window.location.replace("workout.html");
}

window.addEventListener("DOMContentLoaded", async () => {
    let createButton = document.querySelector("#btn-create-workout");
    createButton.addEventListener("click", createWorkout);
    let ordering = "-date";

    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('ordering')) {
        let aSort = null;
        ordering = urlParams.get('ordering');
        if (ordering == "name" || ordering == "owner" || ordering == "date") {
                let aSort = document.querySelector(`a[href="?ordering=${ordering}"`);
                aSort.href = `?ordering=-${ordering}`;
        } 
    } 

    let currentSort = document.querySelector("#current-sort");
    currentSort.innerHTML = (ordering.startsWith("-") ? "Descending" : "Ascending") + " " + ordering.replace("-", "");

    let currentUser = await getCurrentUser();
    // grab username
    if (ordering.includes("owner")) {
        ordering += "__username";
    }
    let workouts = await fetchWorkouts(ordering);
    
    let tabEls = document.querySelectorAll('a[data-bs-toggle="list"]');
    for (let i = 0; i < tabEls.length; i++) {
        let tabEl = tabEls[i];
        tabEl.addEventListener('show.bs.tab', function (event) {
            let workoutAnchors = document.querySelectorAll('.workout');
            for (let j = 0; j < workouts.length; j++) {
                // I'm assuming that the order of workout objects matches
                // the other of the workout anchor elements. They should, given
                // that I just created them.
                let workout = workouts[j];
                let workoutAnchor = workoutAnchors[j];

                switch (event.currentTarget.id) {
                    case "list-my-workouts-list":
                        if (workout.owner == currentUser.url) {
                            workoutAnchor.classList.remove('hide');
                        } else {
                            workoutAnchor.classList.add('hide');
                        }
                        break;
                    case "list-athlete-workouts-list":
                        if (currentUser.athletes && currentUser.athletes.includes(workout.owner)) {
                            workoutAnchor.classList.remove('hide');
                        } else {
                            workoutAnchor.classList.add('hide');
                        }
                        break;
                    case "list-public-workouts-list":
                        if (workout.visibility == "PU") {
                            workoutAnchor.classList.remove('hide');
                        } else {
                            workoutAnchor.classList.add('hide');
                        }
                        break;
                    default :
                        workoutAnchor.classList.remove('hide');
                        break;
                }
            }
        });
    }
});





function generateClones(button) {
  let clones = randomInt(4, 7);
  for (let it = 1; it <= clones; it++) {
    let clone = button.querySelector("svg").cloneNode(true),
      size = randomInt(5, 16);
    button.appendChild(clone);
    clone.setAttribute("width", size);
    clone.setAttribute("height", size);
    clone.style.position = "absolute";
    clone.style.transition =
      "transform 0.5s cubic-bezier(0.12, 0.74, 0.58, 0.99) 0.3s, opacity 1s ease-out .5s";
    let animTimeout = setTimeout(function() {
      clearTimeout(animTimeout);
      clone.style.transform =
        "translate3d(" +
        (plusOrMinus() * randomInt(10, 25)) +
        "px," +
        (plusOrMinus() * randomInt(10, 25)) +
        "px,0)";
      clone.style.opacity = 0;
    }, 1);
    let removeNodeTimeout = setTimeout(function() {
      clone.parentNode.removeChild(clone);
      clearTimeout(removeNodeTimeout);
    }, 900);
  }
}


function plusOrMinus() {
  return Math.random() < 0.5 ? -1 : 1;
}

function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}
