var settingsMenu = document.querySelector('.settings-menu');
var darkBtn = document.getElementById("dark-btn");

function settingsMenuToogle() {
    settingsMenu.classList.toggle('settings-menu-height');
}

darkBtn.onclick = function () {
    darkBtn.classList.toggle("dark-btn-on");
    document.body.classList.toggle("dark-theme");

    if (localStorage.getItem("theme") == "light") {
        localStorage.setItem("theme", "dark");
    }
    else {
        localStorage.setItem("theme", "light");
    }
}

if (localStorage.getItem("theme") == "light") {
    darkBtn.classList.remove("dark-btn-on");
    document.body.classList.remove("dark-theme");
}
else if (localStorage.getItem("theme") == "dark") {
    darkBtn.classList.add("dark-btn-on");
    document.body.classList.add("dark-theme");
}
else {
    localStorage.setItem("theme", "light");
}



function toggleDropdown(menuClass) {
    const dropdown = document.querySelector(`.${menuClass}-dropdown`);
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
}


window.onclick = function(event) {
    if (!event.target.closest('.menu-container')) {
        const dropdowns = document.querySelectorAll('.dropdown-menu');
        dropdowns.forEach(dropdown => {
            if (dropdown.style.display === "block") {
                dropdown.style.display = "none";
            }
        });
    }
}
