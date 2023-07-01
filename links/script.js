const main = document.querySelector("main");

(async function () {
    var meta = await (await fetch("meta.json")).json();

    meta.forEach((category) => {
        var links = "";

        for (var i = 1; i < category.length; i++) {
            links += `
                <a href="${category[i].href}">
                    <div class="link">
                        <span class="link-title">${category[i].name}</span>
                    </div>
                </a>
            `;
        }

        main.innerHTML += `
            <div class="category">
                <h3 class="h-category">${category[0]}</h3>
                <div class="category-content">
                    ${links}
                </div>
            </div>
        `;
    });
})();
