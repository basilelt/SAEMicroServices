document.querySelector(".dropdown-btn").addEventListener("click", function() {
    var sidebar = document.getElementById("mySidebar");
    sidebar.style.width = "250px";
});

document.querySelector(".closebtn").addEventListener("click", function() {
    var sidebar = document.getElementById("mySidebar");
    sidebar.style.width = "0";
});