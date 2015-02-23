__author__ = 'darka'
from Tagger import tag


def compare(text1, text2):
    text1_tags = tag(text1, 0)
    text2_tags = tag(text2, 0)
    #get the max number of tags
    t_max=min([text1_tags.__len__(), text2_tags.__len__()])
    if t_max != 0:
        text1_tags = text1_tags[:t_max]
        text2_tags = text2_tags[:t_max]
        #get the less long vector
        common_word = [w for w in text1_tags if text2_tags.__contains__(w)]
        return common_word.__len__()/text1_tags.__len__()
    return 0

#TODO: set MIN and MAX
#min text similitude
MIN = 0
#max text similitude
MAX = 1

'''
Given a list of article (context_list)
return if the article is in the context using the
compare. REMEMBER to set MIN, MAX

'''
def is_article_in_context(article, context_list):
    max_sim = 0
    for ar in context_list:
        sim = compare(ar.text, article.text)
        if sim > max_sim:
            max_sim = sim
        if sim >= MAX or sim <= MIN:
            return False
    #print(max_sim)
    return True


def correlated_article(base_article, articles_by_title_list, article_by_tag_list):
    return article_by_tag_list+articles_by_title_list