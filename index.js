const socialRedirects = {
    github: "https://github.com/PaddeCraft/",
    codepen: "https://codepen.io/paddecraft/",
};
const quotes = [
    "Coding is easy, right?",
    "Python is faster then C.",
    "I use arch btw.",
    ":qw",
    "Legit news: TikTok",
    "My code without StackOverflow:",
    "This is a quote",
    "!false: it's funny bcuz it's true.",
    "An exception occured.",
    "What does this function do again?",
];

document.addEventListener("DOMContentLoaded", function () {
    for (const [id, link] of Object.entries(socialRedirects)) {
        document.getElementById(id).addEventListener("click", function () {
            window.location.href = link;
        });
    }
    // https://stackoverflow.com/a/5915122
    document.getElementById("quote").innerText =
        quotes[Math.floor(Math.random() * quotes.length)];
});
