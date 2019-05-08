# -------------------------------------------------------------------------------
# Name:        Ejercicio 3
# Purpose:
#
# Author:    Othmane Bakhtaoui
#
# -------------------------------------------------------------------------------

from elasticsearch import Elasticsearch

# adding to stopword the ".*presc.*",".*mg.*" ,".*cm.*", ".*[1-1000].*" to avoid size of prescription and drugs
stopwords = [".*presc.*", ".*mg.*", ".*cm.*", ".*[1-1000].*", "i", "me", "my", "myself", "we", "us", "our",
             "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself",
             "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
             "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be",
             "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "will", "would", "shall",
             "should", "can", "could", "may", "might", "must", "ought", "i'm", "you're", "he's", "she's", "it's",
             "we're", "they're", "i've", "you've", "we've", "they've", "i'd", "you'd", "he'd", "she'd", "we'd",
             "they'd", "i'll",
             "you'll", "he'll", "she'll", "we'll", "they'll", "isn't", "aren't", "wasn't", "weren't", "hasn't",
             "haven't", "hadn't", "doesn't", "don't", "didn't", "won't", "wouldn't", "shan't", "shouldn't", "can't",
             "cannot",
             "couldn't", "mustn't", "let's", "that's", "who's", "what's", "here's", "there's", "when's", "where's",
             "why's",
             "how's",
             "daren't", "needn't", "oughtn't", "mightn't", "a", "an", "the", "and", "but", "if", "or", "because", "as",
             "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through",
             "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
             "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all",
             "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own",
             "same", "so", "than", "too", "very", "one", "every", "least", "less", "many", "now", "ever", "never",
             "say", "says", "said", "also", "get", "go", "goes", "just", "made", "make", "put", "see", "seen",
             "whether", "like", "well", "back", "even", "still", "way", "take", "since", "another", "however", "two",
             "three", "four", "five", "first", "second", "new", "old", "high", "long"]

def search_drugs_and_medications():
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
                                "query": "\"was prescribed\"",
                                "operator": "and"
                            }
                        }
                    }
                }
            },
            "aggs": {
                "Searching medications": {
                    "significant_terms": {
                        "size": 1000,
                        "field": "selftext",
                        "exclude": stopwords,
                        "gnd": {}
                    }
                }
            }
        }
    )

    # _______________________________________________________________#
    # _______________________USING wikidata LIST____________________ #
    # _______________________________________________________________#

    medication_text_file = open('medications.txt', 'r')
    medications_list = []
    for medication in medication_text_file:
        medications_list.append(medication.strip().lower())

    f = open("ej3_result.txt", "wb")
    for medication in results["aggregations"]["Searching medications"]["buckets"]:
        if medication["key"].lower() in medications_list:
            f.write(str(medication["key"]).encode("utf8") + "\n")
    f.close()


    # _______________________________________________________________#
    # _______________________USING wikidata API_____________________ #
    # ________________________NOT RECOMMENDED _______________________#
"""
    f_api = open("ej3_result_using_api.txt", "wb")
    for res in results["aggregations"]["Searching medications"]["buckets"]:
        params = {
            'action': 'wbsearchentities',
            'format': 'json',
            'language': 'en',
            'search': str(res["key"])
        }
        r = requests.get(API_ENDPOINT, params=params)
        try:
            s = r.json()['search'][0]['description']
            if s.find("chemical") != - 1 or s.find("pharmaceut") != - 1 or s.find("compound") != - 1:
                f_api.write(str(res["key"].replace(u'\u2019', "'")) + "\n")

        except KeyError:
            print()
        except IndexError:
            print()

    f_api.close()
"""



def main():
    search_drugs_and_medications()


if __name__ == '__main__':
    main()
