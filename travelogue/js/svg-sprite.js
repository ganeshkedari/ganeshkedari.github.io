/**
 * Injects SVG sprite into the DOM for icon usage.
 * Uses DOMParser instead of innerHTML to avoid XSS risks (CodeQL: js/xss-through-dom).
 *
 * @param {string} path - URL to the SVG sprite file
 * @see https://css-tricks.com/ajaxing-svg-sprite/
 */
function injectSvgSprite(path) {
    var ajax = new XMLHttpRequest();
    ajax.open("GET", path, true);
    ajax.send();
    ajax.onload = function (e) {
        var div = document.createElement("div");
        div.className = 'd-none';
        // Use DOMParser to safely parse SVG content instead of innerHTML
        var parser = new DOMParser();
        var doc = parser.parseFromString(ajax.responseText, "image/svg+xml");
        var svg = doc.documentElement;
        if (svg && svg.nodeName === "svg") {
            div.appendChild(svg);
        }
        document.body.insertBefore(div, document.body.childNodes[0]);
    }
}
