import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords


def tag(sentence, num):
    #remove symbols
    import string
    for char in string.punctuation:
        sentence = sentence.replace(char, ' ')
    all_words = sentence.lower().split()
    # Create a frequency distribution
    stop_words = set(stopwords.words('english'))
    stemmer = SnowballStemmer("english")
    clean_words = [stemmer.stem(w) for w in all_words if not stemmer.stem(w) in stop_words]
    freq_clean  = nltk.FreqDist(clean_words)
    result=[]
    if freq_clean.__len__() != 0:
        if num != 0:
            mc = freq_clean.most_common(num)
            result = [w[0] for w in mc]
        else:
            result = freq_clean.most_common(freq_clean.__len__())
    return result


def correlated_article(base_article, articles_by_title_list, article_by_tag_list):
    return article_by_tag_list+articles_by_title_list


#########################
#### NOT USED NOW #######
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
