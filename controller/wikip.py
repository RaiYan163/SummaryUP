import wikipedia


def get_article_name_from_link(link):

    parts = link.split('/')    
    article_name = parts[-1]
    article_name = article_name.replace('_', ' ')
    return article_name

def wiki_sum(url):
    name = get_article_name_from_link(url)
    return wikipedia.summary(name)
def wiki_trans(url):
    name = get_article_name_from_link(url)
    return wikipedia.page(name).content