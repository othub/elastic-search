# -------------------------------------------------------------------------------
# Name:        Ejercicio 4 - HurtSelf
# Purpose:
#
# Author:    Othmane Bakhtaoui
#
# -------------------------------------------------------------------------------

from elasticsearch import Elasticsearch

"""
scholarly is a module that allows you to retrieve author
and publication information from Google Scholar in a friendly, Pythonic way.
import scholarly
"""

stopwords = ["i'm", "work", "getting","lot","tell", "head","because","cause","consequence",
             "please", "hurt", "myself", "person", "try", "want", "best", "quit", "a", "about", "relapse",
             "above", "after", "apace", "again", "against", "all", "also", "am", "an", "got",
             "and", "another", "any", "are", "aren't", "as", "at", "back", "be", "because",
             "been", "before", "being", "brain", "last", "below", "between", "both", "but","sure",
             "by", "can", "really", "need", "recent","based","follow","die","sent", "explain",
             "different", "hard", "time", "times", "got", "free",
             "watch","ago","done","1","2","3","4","5","6","7","8","9","0","lot", "tell","making", "accept","end","find",
             "watching", "habit", "ufo", "thing", "better", "anything", "everything", "going",
             "cannot", "could", "couldn't", "day", "days", "did", "didn't", "do", "does",
             "don't", "down", "during", "each", "even", "ever", "every", "few", "first",
             "for", "four", "from", "further", "mind", "get", "self", "feel", "feeling", "encyclopedia",
             "go", "goes", "had", "hadn't", "has", "burned.after", "burned", "decide", "decided",
             "hasn't", "have", "peace", "haven't", "having", "helpable", "come", "he", "he'd",
             "he'll", "he's", "her", "came", "start", "stop", "thing", "things", "something",
             "here's", "hers", "herself", "high", "him", "himself", "his", "how", "how's",
             "however", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't",
             "it", "it's", "its", "itself", "relapsed", "just", "least", "less", "life", "let's",
             "made", "make", "many", "me", "more", "most", "mustn't", "my", "myself", "never",
             "new", "no", "nor", "not", "now", "of", "want", "week", "quitting", "feel", "off",
             "journey", "old", "on", "good", "started", "recovery", "much", "rebooted", "streak",
             "once", "one", "only", "or", "other", "day", "month", "year", "ought", "our",
             "over", "own", "put", "said", "same", "say", "says", "second", "see", "seen",
             "shan't", "she", "felt", "problem", "bad", "months", "days", "without", "real",
             "help", "real", "finally", "far", "ours", "ourselves", "out", "stop", "think",
             "she'd", "long", "here", "pacts", "ufo's", "know", "doesn't", "doing", "five",
             "she'll", "she's", "should", "shouldn't", "since", "so", "some", "still", "such",
             "take", "than", "that", "become", "that's", "the", "their", "theirs",
             "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
             "they've", "this", "those", "time", "three", "through", "to", "too", "two",
             "until", "up", "very", "was", "able", "actually", "wasn't", "read", "clean",
             "wanted", "way", "became", "away", "we", "will", "we'd", "we'll", "keep", "found",
             "we're", "use", "reading", "rid", "hope", "past", "strong", "them", "themselves", "can't", "like",
             "we've", "well", "using", "always", "never", "today", "give", "were", "weren't",
             "what", "what's", "when", "when's", "where", "under","consider","lack","ending","sent", "random"
             "where's", "whether", "which", "while", "who", "who's", "whom", "why", "why's",
             "with", "won't", "would", "part", "wouldn't", "you", "you'd", "you'll", "you're",
             "your", "yours", "yourself", "yourselves", "years", "you've"]
possible_terms = set()


def search_self_harm_reasons():
    es = Elasticsearch()
    results = es.search(
        index="reddit-mentalhealth",
        body={
            "size": 0,
            "query": {
                "bool": {
                    "should": {
                        "match": {
                            "selftext": {
                                "query": "\"diagnosed with\""
                                , "operator": "and"
                            }
                        }
                    },
                    "must": [
                        {
                            "match": {
                                "selftext": {
                                    "query": "hurt myself",
                                    "operator": "and"
                                }
                            }
                        },
                    ]
                }
            },
            "aggs": {
                "titles": {
                    "significant_terms": {
                        "field": "title",
                        "size": 1200,
                        "exclude": stopwords,
                    }
                },
                "selftexts": {
                    "terms": {
                        "field": "selftext",
                        "size": 1200,
                        "exclude": stopwords,
                    }
                },
                "subreddits": {
                    "significant_terms": {
                        "field": "subreddit",
                        "size": 1200,
                        "exclude": stopwords,
                    }
                }
            }
        }
    )
    # Llaves de nombres del foro
    for key in results['aggregations']['subreddits']['buckets']:
        possible_terms.add(key['key'] + "\n")

    for key in results['aggregations']['selftexts']['buckets']:
        possible_terms.add(key['key'])

    for key in results['aggregations']['titles']['buckets']:
        possible_terms.add(key['key'])


"""

term: the term found in the query used
search_method: can be either title or abstract(which is a summary of the article)
:return: the list found
def look_up_scholar_articles(term, search_method):    
    try:
        search_query = scholarly.search_pubs_query(term + ' comorbid')
        return search_query.bib[search_method]
    except Exception as e:
        print()
"""


def main():
    search_self_harm_reasons()
    # leo los articulos obtenidos desde PoP
    article_titles = open('articles_title.txt', 'r')
    articles = []
    for article in article_titles:
        articles.append(article.decode('utf-8').strip().lower())

    #quitar duplicados de la lista
    terms = list(set(possible_terms))
    aux = set()
    for term in terms:
        for article in articles:
            if term.lower() in article:
                aux.add(term)

    # escribir dichos ficheros en el archivo
    f = open("ej4_result_self_harm.txt", 'wb')
    for term in list(set(aux)):
        f.write(term + "\n")
    f.close()


if __name__ == '__main__':
    main()
