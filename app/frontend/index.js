document.getElementById("confirm").addEventListener("click", readForm);
document.addEventListener("DOMContentLoaded", setCurrentTime);

function setCurrentTime() {
    const timeInput = document.getElementById("departure");

    const now = new Date();
    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");

    timeInput.value = `${hours}:${minutes}`;
}

function readForm() {
    document.getElementById('warning-text').innerText = "";

    const from = document.getElementById("from").value;
    const to = document.getElementById("to").value;
    const type = document.getElementById("type").value;
    const persons = document.getElementById("person-count").value;
    const departure = document.getElementById("departure").value;

    if (!from || !to || !type || !persons) {
        document.getElementById('warning-text').innerText = "Uzupełnij wszystkie wymagane pola!";
        return;
    }

    body = {
        from: from,
        to: to,
        type: type,
        persons: persons,
        departure: departure,
        trip_distance: 5 // TO TRZEBA JAKOŚ OBLICZAĆ...
    };

    console.log(body);
}

function getPlaces() {
    
}

function fillSelect(id, options) {
    const select = document.getElementById(id);
    select.innerHTML = `<option value="">-- wybierz --</option>`;
    
    options.forEach(option => {
        const opt = document.createElement("option");
        opt.value = option;
        opt.textContent = option;
        select.appendChild(opt);
    });
}