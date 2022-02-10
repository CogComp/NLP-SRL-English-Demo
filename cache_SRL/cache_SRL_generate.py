import json
import hashlib
import requests


BASE_SRL_HTTP = "http://dickens.seas.upenn.edu:4039/annotate"

#--------------------- Sample Sentences ---------------------
sample_dic = {
    "eng": [
        "To achieve her mission, she opened schools to teach young women her philosophy of dance.",
        "Duncan disliked the commercial aspects of public performance, such as touring and contracts, because she felt they distracted her from her real mission, namely the creation of beauty and the education of the young.",
        "A meteor procession was visible across much of eastern North and South America, leading astronomers to conclude that its source was a small, short-lived natural satellite of the Earth.",
        "Semantic parsing of sentences is believed to be an important task on the road to natural language understanding, and has immediate applications in tasks such as information extraction and question answering.",
        "His duties will be assumed by John Smith who has been elected deputy chairman.",
        "The eruption of an underwater volcano near Tonga on Saturday was likely the biggest recorded anywhere on the planet in more than 30 years, according to experts. Dramatic images from space captured the eruption in real time, as a huge plume of ash, gas and steam was spewed up to 20 kilometers into the atmosphere and tsunami waves were sent crashing across the Pacific.",
        "Crews fighting a massive fire along the central coast of California near the iconic Highway 1 made progress Sunday in containing the blaze, but dozens of homes remained under evacuation orders. The Colorado fire ignited Friday evening in Palo Colorado Canyon in the Big Sur region of Monterey County and swelled to 1050 acres Saturday, up from 100 acres a day prior.", 
        "Pfizer and BioNTech have begun a clinical trial for their Omicron-specific Covid-19 vaccine candidate, they announced in a news release on Tuesday. The study will evaluate the vaccine for safety, tolerability and the level of immune response, as both a primary series and a booster dose, in up to 1420 healthy adults ages 18 to 55."
]
}


#-------------------- Annontation Function --------------------
def getBasicAnnotations(text):

    # SRL
    input = {"sentence":text}
    res_out_SRL = requests.post(BASE_SRL_HTTP, json = input)
    res_json_SRL = res_out_SRL.json()
    tokens = []
    endPositions = []
    if "tokens" in res_json_SRL:
        tokens = res_json_SRL["tokens"]
    # print(tokens)
    if "sentences" in res_json_SRL:
        sentences = res_json_SRL["sentences"]
        if "sentenceEndPositions" in sentences:
            endPositions = sentences["sentenceEndPositions"]
    return tokens, endPositions, res_json_SRL



if __name__ == "__main__":
    cache = {}
    for lang in sample_dic.keys():
        cache[lang] = {}

        for text in sample_dic[lang]:
            hash_value = hashlib.sha1(text.encode()).hexdigest()
            if hash_value in cache[lang].keys():
                raise ValueError('COLLISION ERROR: Different text has same hash value!')
            else:
                cache[lang][hash_value] = {}
                cache[lang][hash_value]['text'] = text
                cache[lang][hash_value]['tokens'], cache[lang][hash_value]['end_pos'], cache[lang][hash_value]['srl'] = getBasicAnnotations(text)


cache_json = json.dumps(cache, indent=4)
with open('cache_SRL/cache_SRL.json', 'w') as json_file:
    json_file.write(cache_json)


