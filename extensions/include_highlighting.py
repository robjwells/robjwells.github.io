import re

highlighted_code_regex = re.compile(
    r'class=["\']syntax["\']>',
    flags=re.IGNORECASE|re.VERBOSE
    )


def contains_code(html):
    """Return whether item contains code block with initial language line"""
    match = highlighted_code_regex.search(html)
    return (match is not None)


def process_posts_and_pages(pages, posts, settings):
    for content_list in [posts, pages]:
        for item in content_list:
            item.include_highlighting = contains_code(item.html)
    return dict(posts=posts, pages=pages)
