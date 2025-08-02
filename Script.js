function calculate() {
    let key = document.getElementById("key").value;
    let a = document.getElementById("num1").value;
    let b = document.getElementById("num2").value;

    fetch(`https://api-462i.onrender.com/api/calc?key=${key}&a=${a}&b=${b}`)
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            document.getElementById("result").innerText = "❌ Access Denied";
        } else {
            document.getElementById("result").innerText = "✅ Result: " + data.result;
        }
    })
    .catch(() => {
        document.getElementById("result").innerText = "⚠️ API Connection Failed!";
    });
}
