document.addEventListener("DOMContentLoaded", function () {

    const button = document.getElementById("themeToggle");

    if (!button) return;

    function updateButton() {

        if (document.body.classList.contains("dark-mode")) {
            button.innerHTML = "☀️ Light";
        } else {
            button.innerHTML = "🌙 Dark";
        }

    }

    updateButton();

    button.addEventListener("click", function () {

        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
        } else {
            localStorage.setItem("theme", "light");
        }

        updateButton();

    });

});