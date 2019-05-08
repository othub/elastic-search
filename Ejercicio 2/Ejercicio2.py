# -------------------------------------------------------------------------------
# Name:        Ejercicio 2 - more like this
# Purpose:
#
# Author:    Othmane Bakhtaoui
#
# -------------------------------------------------------------------------------

from elasticsearch import Elasticsearch

stopwords = [".*addict.*", "addicts", "addictive", "cravings", "addictions", "obsession",
             "addict", "addiction", "addicted", "craving", "quit", "a", "about", "relapse",
             "above", "after", "apace", "again", "against", "all", "also", "am", "an", "got",
             "and", "another", "any", "are", "aren't", "as", "at", "back", "be", "because",
             "been", "before", "being", "brain", "last", "below", "between", "both", "but",
             "by", "can", "really", "need", "hard", "time", "times", "got", "free", "watch",
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
             "take", "than", "that", "people", "become", "that's", "the", "their", "theirs",
             "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
             "they've", "this", "those", "time", "three", "through", "to", "too", "two",
             "until", "up", "very", "was", "able", "actually", "wasn't", "read", "clean",
             "wanted", "way", "became", "away", "we", "will", "we'd", "we'll", "keep", "found",
             "we're", "use", "reading", "rid", "hope", "past", "strong", "them", "themselves", "can't", "like",
             "we've", "well", "using", "always", "never", "today", "give", "were", "weren't",
             "what", "what's", "when", "when's", "where", "under",
             "where's", "whether", "which", "while", "who", "who's", "whom", "why", "why's",
             "with", "won't", "would", "part", "wouldn't", "you", "you'd", "you'll", "you're",
             "your", "yours", "yourself", "yourselves", "years", "you've"]

def main():
    es = Elasticsearch()
    results = es.search(
        index="reddit-mentalhealth",
        body=
        {
            "size": 0,
            "query": {
                "bool": {
                    "should": [
                        {
                            "more_like_this": {
                                "fields": [
                                    "title",
                                    "selftext",
                                    "subreddit"
                                ],
                                "like": "addiction",
                                "min_term_freq": 1,
                                "max_query_terms": 12
                            }
                        }
                    ]
                }
            },
            "aggregations": {
                "significant_addiction_terms": {
                    "significant_terms": {
                        "field": "selftext",
                        "size": 20,
                        "exclude": stopwords
                    }
                }
            }
        }
    )

    f = open("ej2_result.tsv", "wb")

    term_length = len(results['aggregations']['significant_addiction_terms']['buckets'])
    print("\n______________Significant Terms_______________\n")
    for i in range(0, term_length):
        term = results['aggregations']['significant_addiction_terms']['buckets'][i]['key']
        print(term + "\n")
        f.write(
            term.encode("utf8") + "\n"
        )
    f.close()


# Running the app
if __name__ == '__main__':
    main()
