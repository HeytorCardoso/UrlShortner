const submit_button = document.getElementById("btn-submit");

async function submitUrl () {
    const inputUrl = document.getElementById("urlInput");
    longUrl = inputUrl.value;
    
    const response = await fetch("http://127.0.0.1:8000/submit", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({value: longUrl})
    });

    const result = await response.json();
    alert("Resposta:" + result);
};

