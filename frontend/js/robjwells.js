/*jslint browser: true, maxlen: 79 */
/*globals hljs, window */
(function (document, window, hljs) {
    'use strict';

    var add_line_numbers,
        create_code_page,
        open_new_window,
        build_language_map,
        format_blocks,
        highlight_code;


    add_line_numbers = function (lines, starting_number) {
        var current_line_number = starting_number,
            last_line_number = starting_number + (lines.length - 1),
            max_digits = last_line_number.toString().length,

            pad_number = function (str, target_length) {
                while (str.length < target_length) {
                    str = ' ' + str;
                }
                return str;
            };

        var numbered_lines = lines.map(function (line) {
            // Add line number in span to the start of the line of code
            var html = (
                '<span class="line-number">' +
                pad_number(current_line_number.toString(), max_digits) +
                '  </span>' + line
            );
            current_line_number += 1;
            return html;
        });

        return numbered_lines;
    };


    create_code_page = function (code) {
        // This takes advantage of optional tags in HTML5
        return ('<!DOCTYPE html><title>Code</title>' +
                '<pre><code>' + code + '</code></pre>');
    };


    open_new_window = function (content) {
        var new_window = window.open(),
            new_document = new_window.document;

        new_document.open();
        new_document.write(create_code_page(content));
        new_document.close();
    };


    build_language_map = function () {
        // Map aliases to canonical language names
        var language_map = {};
        hljs.listLanguages().forEach(function (language) {
            var aliases = hljs.getLanguage(language).aliases || [];
            aliases.forEach(function (alias) {
                language_map[alias] = language;
            });
            // Add language itself
            language_map[language] = language;
        });
        return language_map;
    };


    format_blocks = function (code_blocks) {
        var language_map = build_language_map();
        var lang_regex = new RegExp(
            '^(' + Object.keys(language_map).join('|') + '):\\n'
        );

        code_blocks.forEach(function (code_block) {
            var plain_text = code_block.textContent,
                language = plain_text.match(lang_regex),
                line_number_regex,
                numbered_line,
                starting_number,
                new_code;

            // Strip language line if found and set class on block
            if (language) {
                language = language_map[language[1]];  // Convert alias
                code_block.setAttribute('class', 'hljs ' + language);
                // Remove language line from plain text code
                plain_text = plain_text.split('\n').slice(1).join('\n');
            }

            // Detect if code has line numbers
            line_number_regex = /^\ *(\d+):\ {2}/;
            numbered_line = plain_text.match(line_number_regex);
            if (numbered_line) {
                starting_number = parseInt(numbered_line[1], 10);
                // Remove line numbers from plain text code
                plain_text = plain_text.replace(
                    new RegExp(line_number_regex.source, 'gm'),
                    ''
                );
            }

            // Strip blank lines from end of code
            plain_text = plain_text.replace(/\n+$/, '');

            try {
                new_code = hljs.highlight(language, plain_text).value;
            } catch (ignore) {
                new_code = plain_text;
            }

            // Add line numbers to code and append link to plain text
            if (starting_number) {
                new_code = add_line_numbers(
                    new_code.split('\n'),
                    starting_number
                );
                new_code.push('\n' +
                        '<a href="#" class="code-link">' +
                        'Show without line numbers</a>');
                new_code = new_code.join('\n');
            }

            // Fill code block with (highlighted? numbered?) new code
            // Placing the HTML here and adding the event listenener
            // below so that the new content is only inserted in one place
            code_block.innerHTML = new_code;

            // Add event listener to DOM element if code was numbered
            if (starting_number) {
                // Open new window when code link is clicked
                code_block.lastChild.addEventListener('click', function (ev) {
                    ev.preventDefault(); // Don't follow link's href
                    open_new_window(plain_text);
                }, false);
            }

        });  // End of code_blocks.forEach
    };  // End of format_blocks


    highlight_code = function () {
        var code_blocks = Array.prototype.slice.call(
            document.querySelectorAll('pre code')
        );

        if (code_blocks.length) {
            format_blocks(code_blocks);
        }
    };


    // Wait for DOMContentLoaded if it hasn't already fired
    if (document.readyState === 'loading') {
        window.addEventListener('DOMContentLoaded', highlight_code, false);
    } else {
        highlight_code();
    }

}(document, window, hljs));
