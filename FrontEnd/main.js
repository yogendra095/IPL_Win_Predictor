
const url = "http://127.0.0.1:8000/predict";

// Form elements
const battingTeam = document.querySelector("#batting_team");
const bowlingTeam = document.querySelector("#bowling_team");
const city = document.querySelector("#city");
const overInput = document.querySelector("#over");
const targetInput = document.querySelector("#target");
const scoreInput = document.querySelector("#score");
const wicketInput = document.querySelector("#wicket");
const btn = document.querySelector("#predict-btn");
const output = document.querySelector("#json-output");
output.classList.add("output")


btn.addEventListener("click", async (event) => {
    event.preventDefault(); // Prevent form submission

    const data = {
        batting_team: battingTeam.value,
        bowling_team: bowlingTeam.value,
        city: city.value,
        over: parseFloat(overInput.value),     
        target: parseInt(targetInput.value),     
        score: parseInt(scoreInput.value),
        wicket: parseInt(wicketInput.value)
    };

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });


        const result = await response.json();

        if (result.error) {
            output.innerText = `Error: ${result.error}`;
        } else {
            output.classList.remove("output")
            output.innerText = `Win Probability of ${bowlingTeam.value}: ${result.Bowling_win*100}%\nWin Probability of ${battingTeam.value}: ${result.Batting_win*100}%`;
        }
    } catch (err) {
        console.error(err);
        output.innerText = `Fetch Error: ${err.message}`;
    }
});