// ======================================================
// SalesPro Technologies
// AI Sales Intelligence System
// script.js
// ======================================================

// Welcome Message
window.onload = function () {

    console.log("SalesPro Technologies Loaded Successfully!");

};


// ==============================
// Smooth Fade Animation
// ==============================

const cards = document.querySelectorAll(".card, .info-box, .company-card");

cards.forEach((card, index) => {

    card.style.opacity = "0";
    card.style.transform = "translateY(30px)";

    setTimeout(() => {

        card.style.transition = "0.6s";

        card.style.opacity = "1";

        card.style.transform = "translateY(0)";

    }, index * 150);

});


// ==============================
// Sidebar Highlight
// ==============================

const links = document.querySelectorAll(".sidebar a");

links.forEach(link => {

    if (window.location.href.includes(link.getAttribute("href"))) {

        link.style.background = "#2563eb";

        link.style.color = "white";

    }

});


// ==============================
// Card Hover Effect
// ==============================

const infoCards = document.querySelectorAll(".info-box");

infoCards.forEach(card => {

    card.addEventListener("mouseenter", function () {

        card.style.transform = "scale(1.02)";

        card.style.transition = ".3s";

    });

    card.addEventListener("mouseleave", function () {

        card.style.transform = "scale(1)";

    });

});


// ==============================
// Search Box Effect
// ==============================

const search = document.querySelector("input[name='q']");

if (search) {

    search.addEventListener("focus", function () {

        search.style.boxShadow = "0 0 12px #2563eb";

    });

    search.addEventListener("blur", function () {

        search.style.boxShadow = "none";

    });

}


// ==============================
// Progress Bar Animation
// ==============================

const bars = document.querySelectorAll(".progress-bar");

bars.forEach(bar => {

    let width = bar.style.width;

    bar.style.width = "0";

    setTimeout(() => {

        bar.style.transition = "2s";

        bar.style.width = width;

    }, 500);

});


// ==============================
// Notification Popup
// ==============================

function showNotification(message) {

    const notification = document.createElement("div");

    notification.innerHTML = message;

    notification.style.position = "fixed";

    notification.style.top = "20px";

    notification.style.right = "20px";

    notification.style.background = "#2563eb";

    notification.style.color = "white";

    notification.style.padding = "15px";

    notification.style.borderRadius = "10px";

    notification.style.boxShadow = "0 10px 20px rgba(0,0,0,.3)";

    notification.style.zIndex = "999";

    document.body.appendChild(notification);

    setTimeout(() => {

        notification.remove();

    }, 3000);

}


// Show Welcome Notification

setTimeout(() => {

    showNotification("Welcome to SalesPro Technologies 🚀");

}, 800);


// ==============================
// Current Date
// ==============================

const footer = document.querySelector("footer");

if (footer) {

    const date = new Date();

    const p = document.createElement("p");

    p.innerHTML =

        "Today's Date : " +

        date.toLocaleDateString();

    footer.appendChild(p);

}


// ==============================
// Scroll to Top Button
// ==============================

const topBtn = document.createElement("button");

topBtn.innerHTML = "⬆";

topBtn.style.position = "fixed";

topBtn.style.bottom = "20px";

topBtn.style.right = "20px";

topBtn.style.padding = "12px 15px";

topBtn.style.border = "none";

topBtn.style.borderRadius = "50%";

topBtn.style.background = "#2563eb";

topBtn.style.color = "white";

topBtn.style.cursor = "pointer";

topBtn.style.display = "none";

document.body.appendChild(topBtn);

window.addEventListener("scroll", function () {

    if (window.scrollY > 200)

        topBtn.style.display = "block";

    else

        topBtn.style.display = "none";

});

topBtn.onclick = function () {

    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

};


// ======================================================
// End of Script
// ======================================================