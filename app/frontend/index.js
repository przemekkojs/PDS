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
    const tip = document.getElementById("tip").value;

    if (!from || !to || !type) {
        document.getElementById('warning-text').innerText = "Uzupełnij wszystkie wymagane pola!";
        return {
            good:false,
            body: {}
        };
    }

    return {
        good: true,
        body: {
            start: from,
            end: to,
            type: type,
            persons: persons || 1,
            departure: departure,
            tip: tip || 0
        }
    };
}

async function getPlaces() {
    const fromSelect = document.getElementById("from");
    const toSelect = document.getElementById("to");

    try {
        const response = await fetch("http://localhost:8000/zones");

        if (!response.ok) {
            throw new Error("Nie udało się pobrać stref");
        }

        const zones = await response.json();

        fromSelect.innerHTML = "";
        toSelect.innerHTML = "";

        fromSelect.appendChild(new Option("Wybierz miejsce", ""));
        toSelect.appendChild(new Option("Wybierz miejsce", ""));

        for (const [id, name] of Object.entries(zones)) {
            fromSelect.appendChild(new Option(name, id));
            toSelect.appendChild(new Option(name, id));
        }

    } catch (error) {
        console.error(error);
    }
}

async function predict() {
    document.getElementById('confirm').disabled = true;

    const formResult = readForm();
    const body = formResult.body;

    if (!formResult.good) {
        document.getElementById('confirm').disabled = false;
        return;
    }        

    try {
        const response = await fetch("http://localhost:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Prediction failed");
        }

        const data = await response.json();

        document.getElementById("price-est").innerText = `$${data.fee.toFixed(2)}`;
        document.getElementById("time-est").innerText = `${Math.round((data.time / 60))} min`;
        document.getElementById("dist-est").innerText = `${data.dist.toFixed(2)} mi`;

        document.getElementById('confirm').disabled = false;
    } catch (error) {
        document.getElementById('confirm').disabled = false;
        console.error(error);
    }
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

document.addEventListener("DOMContentLoaded", () => {
    getPlaces();
});