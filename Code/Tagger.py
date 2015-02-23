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
    # This is a little more interesting
    if freq_clean.__len__() != 0:
        if num != 0:
            mc = freq_clean.most_common(num)
            result = [w[0] for w in mc]
        else:
            result = freq_clean.most_common(freq_clean.__len__())

    return result