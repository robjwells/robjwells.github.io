(function (document, window) {
    "use strict";

    // Tag-replacing function taken from this StackOverflow question:
    // http://stackoverflow.com/questions/5499078/
    function santise_tags(str) {
        return (
            str.replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
        );
    }

    function clean_code(node) {
        // Remove 'Show without line numbers' link
        node.lastChild.remove();

        // Remove line numbers
        Array.prototype.slice.call(
            node.querySelectorAll(".lineno")
        ).forEach(function (line_num) {
            line_num.remove();
        });

        return node.textContent;
    }

    function create_code_page(code) {
        // This takes advantage of optional tags in HTML5
        // Code is sanitised to prevent oddities with HTML snippets
        return (
            "<!DOCTYPE html><title>Code</title>" +
            "<pre><code>" + santise_tags(code) + "</code></pre>"
        );
    }

    function open_new_window(content) {
        var new_window = window.open();
        var new_document = new_window.document;

        new_document.open();
        new_document.write(create_code_page(content));
        new_document.close();
    }

    function code_link_listener(ev) {
        ev.preventDefault();
        open_new_window(
            clean_code(
                // Clone the node as it needs manipulating and we don't
                // want to affect the highlighted code on the page
                ev.target.parentElement.cloneNode(true)
            )
        );
    }

    function add_plain_code_link(el) {
        // Add newline to space out link
        el.appendChild(document.createTextNode("\n"));

        // Build a link with the listening function attached
        var link = document.createElement("a");
        var link_text = document.createTextNode("Show without line numbers");
        link.appendChild(link_text);
        link.setAttribute("href", "#");
        link.addEventListener("click", code_link_listener, false);

        el.appendChild(link);
    }

    function add_links_to_code_blocks() {
        var pre_blocks = Array.prototype.slice.call(
            document.querySelectorAll(".syntax pre")
        );
        pre_blocks.forEach(function (el) {
            if (el.querySelector(".lineno")) {
                add_plain_code_link(el);
            }
        });
    }

    // Wait for DOMContentLoaded if it hasn't already fired
    if (document.readyState === "loading") {
        window.addEventListener(
            "DOMContentLoaded",
            add_links_to_code_blocks,
            false
        );
    } else {
        add_links_to_code_blocks();
    }

}(document, window));
