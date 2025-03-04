document.querySelector("button").addEventListener("click", function () {
    let query = document.querySelector("input").value;
    if (!query) {
        alert("Please enter a search term!");
        return;
    }

    fetch(`http://127.0.0.1:5000/search?q=${query}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("searchResults").innerText = data.message;
        })
        .catch(error => console.error("Error:", error));
});