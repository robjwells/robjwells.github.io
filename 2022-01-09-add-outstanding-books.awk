function dirname(path) {
    cmd = "dirname " path
    cmd |& getline result
    close(cmd)
    return result
}

function ensure_dir(path) {
    system("mkdir -p " dirname(path))  
}

function safe_name(string) {
    return remove_non_word_characters( remove_apostrophes( tolower( string ) ) )
}

function remove_apostrophes(string) {
    return gensub(/['’]/, "", "g", string)
}

function remove_non_word_characters(string) {
    return gensub(/\W+/, "-", "g", string)
}

/^(2020-(0[6-9]|1[0-2])|202[12])/ {
    path_template = "content/books/%s/%s.md"
    year = substr($1, 0, 4)
    title_for_path = safe_name($2)
    path = sprintf(path_template, year, title_for_path)

    content_template = ( \
        "---\n" \
        "title: \"%s\"\n" \
        "author: \"%s\"\n" \
        "finish-date: %s\n" \
        "---\n" \
        "\n" \
        "_Short review to come!_")
    content = sprintf(content_template, $2, $3, $1)

    ensure_dir(path)
    print content > path
}
