from bs4 import BeautifulSoup

def process_posts_and_pages(pages, posts, settings):
    for content_list in [posts, pages]:
        for item in content_list:
            if '<pre><code>' in item.html:
                item.include_highlighting = True
            else:
                item.include_highlighting = False
    return dict(posts=posts, pages=pages)

