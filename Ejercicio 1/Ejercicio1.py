# -------------------------------------------------------------------------------
# Name:        Ejercicio 1
# Purpose:
#
# Author:    Othmane Bakhtaoui
#
# -------------------------------------------------------------------------------
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import json


def expand_query(terms_size, metric):
    query_with_terms = load_significant_terms(terms_size, metric)
    results = Elasticsearch().search(index="reddit-mentalhealth", body=query_with_terms)

    # getting terms
    terms = []
    terms_length = len(results['aggregations']['terminos mas significativos']['buckets'])
    for i in range(0, terms_length):
        terms.append(results['aggregations']['terminos mas significativos']['buckets'][i]['key'])

    # initial query
    initial_query = """ {
                "query": {
                    "query_string": {
                        "default_field": "selftext",
                        "query": "addiction OR craving OR obsession"""
    for i in range(0, len(terms)):
        initial_query += " OR " + terms[i]

    expanded_query = initial_query + '"' + """} }  }"""
    return json.loads(expanded_query)

def load_significant_terms(terms_size, metric):
    size = str(terms_size)
    query_with_aggs = """ {
                "size": 0,
                "query": {
                    "query_string": {
                        "default_field": "selftext",
                        "query": "addiction OR craving OR obsession"
                    }
                },
                "aggs": {
                    "terminos mas significativos": {
                        "significant_terms": {
                            "field": "selftext",
                            "size":""" + size + """,
                            "exclude": [ ".*addict.*","addicts", "addictive", "cravings", "addictions", "obsession"
                                        ,"addict", "addiction","addicted", "craving","quit", "a", "about","relapse",
                                        "above", "after", "apace", "again", "against", "all", "also", "am", "an","got",
                                        "and", "another", "any", "are", "aren't", "as", "at", "back", "be", "because",
                                        "been", "before", "being","brain", "last", "below", "between", "both", "but", 
                                        "by", "can", "really", "need", "hard", "time", "times","got", "free", "watch",
                                        "watching","habit", "ufo","thing", "better", "anything", "everything","going",
                                        "cannot", "could", "couldn't","day","days", "did", "didn't", "do", "does", 
                                        "don't", "down", "during", "each", "even", "ever", "every", "few", "first", 
                                        "for", "four", "from", "further", "mind", "get","self","feel", "feeling","encyclopedia",
                                         "go", "goes", "had", "hadn't", "has", "burned.after", "burned","decide","decided",
                                        "hasn't", "have", "peace", "haven't", "having","helpable","come", "he","he'd",
                                         "he'll","he's","her", "came","start", "stop", "thing", "things", "something",
                                        "here's", "hers", "herself", "high", "him", "himself", "his", "how", "how's",
                                        "however", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't",
                                        "it", "it's", "its", "itself", "relapsed", "just", "least", "less","life", "let's", 
                                        "made", "make", "many", "me", "more", "most", "mustn't", "my", "myself", "never",
                                        "new", "no", "nor", "not", "now", "of","want","week", "quitting","feel", "off",
                                        "journey", "old", "on","good", "started", "recovery","much", "rebooted", "streak",
                                        "once", "one", "only","or", "other","day", "month", "year", "ought", "our", 
                                        "over", "own", "put","said", "same", "say", "says", "second", "see", "seen",
                                        "shan't", "she", "felt", "problem", "bad", "months", "days","without","real", 
                                        "help","real","finally", "far","ours", "ourselves", "out","stop", "think",
                                        "she'd","long","here","pacts", "ufo's", "know", "doesn't", "doing", "five",
                                        "she'll", "she's", "should", "shouldn't", "since", "so", "some", "still", "such",
                                        "take", "than", "that","people", "become", "that's", "the", "their", "theirs", 
                                        "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
                                        "they've", "this", "those","time", "three", "through", "to", "too", "two", 
                                        "until", "up", "very", "was","able", "actually", "wasn't","read", "clean", 
                                        "wanted", "way", "became", "away", "we","will", "we'd", "we'll","keep", "found",
                                         "we're","use","reading","rid", "hope", "past", "strong","them", "themselves","can't", "like", 
                                        "we've", "well","using", "always", "never", "today", "give", "were", "weren't", 
                                        "what", "what's", "when", "when's", "where", "under",
                                        "where's", "whether", "which", "while", "who", "who's", "whom", "why", "why's",
                                        "with", "won't", "would","part", "wouldn't", "you", "you'd", "you'll", "you're",
                                        "your", "yours", "yourself", "yourselves", "years",  "you've"],
                            """

    query_with_aggs += metric + """ }    }   }   }"""
    return json.loads(query_with_aggs)


def print_posts_with_terms(terms_size, metric):
    # posts
    body = expand_query(terms_size, metric)
    results = Elasticsearch().search(index="reddit-mentalhealth", body=body, size=20)
    length = len(results['hits']['hits'])
    print("\n______________Reddit Posts_______________\n")
    for i in range(0, length):
        author = results['hits']['hits'][i]['_source']['author'].replace("\n", " ").replace("\t", " ")
        subreddit = results['hits']['hits'][i]['_source']['subreddit'].replace("\n", " ").replace("\t", " ")
        self_text = results['hits']['hits'][i]['_source']['selftext'].replace("\n", " ").replace("\t", " ")
        print(author + "<-->" + subreddit + "<-->" + self_text + "\n")

    # terms
    query_with_terms = load_significant_terms(terms_size, metric)
    term_results = Elasticsearch().search(index="reddit-mentalhealth", body=query_with_terms)
    term_length = len(term_results['aggregations']['terminos mas significativos']['buckets'])
    print("\n______________Significant Terms_______________\n")
    for i in range(0, term_length):
        print(term_results['aggregations']['terminos mas significativos']['buckets'][i]['key'] + "\n")


def write_result_in_file(terms_size, metric):
    query = expand_query(terms_size, metric)

    results = helpers.scan(
        Elasticsearch(),
        index="reddit-mentalhealth",
        query=query,
        preserve_order=True
    )

    reddit_posts = []
    for res in results:
        # information
        autor = res['_source']['author']
        subreddit = res['_source']['subreddit']
        date = datetime.utcfromtimestamp(res['_source']['created_utc']).strftime('%Y-%m-%d %H:%M:%S')
        post = res['_source']['selftext']
        # full post
        full_post = autor + "\t" + subreddit + "\t" + date + "\t" + post
        # appending
        reddit_posts.append(full_post)

    # printing
    f = open("ej1_result.tsv", "wt")
    for i in range(0, len(reddit_posts)):
        f.write(reddit_posts[i].encode(encoding='UTF-8') + "\n")
    f.close()


def main():
    # _______________________________________________________________#
    # FIRST ROUND BETWEEN gnd and chi_square and jlh and mutual_info #
    # _______________________________________________________________#

    # 6 terms with gnd
    print("\n\n___________6 results using gnd__________\n")
    print_posts_with_terms(6, '"gnd":{}')

    # 6 terms with chi_square
    print("\n\n___________6 results using chi_square__________\n")
    print_posts_with_terms(6, '"chi_square": {}')

    # 6 terms with jlh
    print("\n\n___________6 results using jlh__________\n")
    print_posts_with_terms(6, '"jlh": {}')

    # 6 terms with mutual_information
    print("\n\n______6 results using mutual_information________\n")
    print_posts_with_terms(6, '"mutual_information": {}')

    # _______________________________________________________________#
    #        SECOND ROUND BETWEEN gnd and chi_square and jlh        #
    # _______________________________________________________________#

    # 12 terms with gnd
    print("\n\n___________12 results using gnd__________\n")
    print_posts_with_terms(12, '"gnd":{}')

    # 12 terms with chi_square
    print("\n\n___________12 results using chi_square__________\n")
    print_posts_with_terms(12, '"chi_square": {}')

    # 12 terms with jlh
    print("\n\n___________12 results using jlh__________\n")
    print_posts_with_terms(12, '"jlh": {}')

    # _______________________________________________________________#
    #            FINAL ROUND BETWEEN gnd and chi_square             #
    # _______________________________________________________________#

    # 25 terms with gnd
    print("\n\n___________25 results using gnd__________\n")
    print_posts_with_terms(25, '"gnd":{}')

    # 25 terms with chi_square
    print("\n\n___________25 results using chi_square__________\n")
    print_posts_with_terms(25, '"chi_square": {}')

    # _______________________________________________________________#
    #                     FINAL ROUND WITH gnd                      #
    # _______________________________________________________________#
    write_result_in_file(14, '"gnd": {}')
    print_posts_with_terms(14, '"gnd": {}')


# Running the app
if __name__ == '__main__':
    main()
