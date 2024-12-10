"use-strict"
//@ts-check

window.onload = () => {
    document.getElementById("suljeIkkuna").addEventListener("click", (e) => {
        e.preventDefault();
        window.close();
    });
};