import json
import hashlib
import requests


BASE_SRL_HTTP = "http://dickens.seas.upenn.edu:4039/annotate"

#--------------------- Sample Sentences ---------------------
sample_dic ={
            "eng": [
                "In the January attack, two Palestinian suicide bombers blew themselves up in central Tel Aviv. The bombing destroyed the whole building, killing 23 other people.",
                "And on Tuesday, Israeli troops shot dead an elderly Palestinian shepherd outside a Jewish settlement on the edge of Gaza City.",
                "Despite operating under bankruptcy laws, united posted the best on time performance.",
                "Police in Pennsylvania a student fatally shot a principal before killing himself this morning.",
                "Last Friday, I was teaching the kids. However, we now need to vaccinate to get rid of the COVID.",
                "Sigmund Freud was an Austrian neurologist and the founder of psychoanalysis, a clinical method for treating psychopathology through dialogue between a patient and a psychoanalyst. Freud was born to Galician Jewish parents in the Moravian town of Freiberg, in the Austrian Empire. He qualified as a doctor of medicine in 1881 at the University of Vienna. Freud lived and worked in Vienna, having set up his clinical practice there in 1886. In 1938, Freud left Austria to escape Nazi persecution. He died in exile in the United Kingdom in 1939.",
                "Barack Hussein Obama II is an American politician and attorney who served as the 44th president of the United States from 2009 to 2017. A member of the Democratic Party, Obama was the first African-American president of the United States. He previously served as a U.S. senator from Illinois from 2005 to 2008 and an Illinois state senator from 1997 to 2004.",
                "Mohandas Karamchand Gandhi was an Indian lawyer, anti-colonial nationalist, and political ethicist. He employed nonviolent resistance to lead the successful campaign for India's independence from British rule, and in turn inspired movements for civil rights and freedom across the world. The honorific Mahātmā, first applied to him in 1914 in South Africa, is now used throughout the world."
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


