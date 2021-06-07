import json 
import hashlib
from datetime import datetime 

class CacheSRL:

    def __init__(self):
        self.map = None


    def load(self):
  
        try:
            with open('cache_SRL/cache_SRL.json') as file_obj:
                cache = json.load(file_obj)
            print("Successfully load cache from cache_SRL.json.")
        except:
            cache = {}
            for lang in ['eng']: #self.map[name].keys():
                cache[lang] = {}
            print("Cannot find cache_SRL.json and an empty new nested dictionary for cache is created.")
        
        return cache


    def read(self, cache_dic, hash_value, lang='eng'):

        tokens = cache_dic[lang][hash_value]['tokens']
        end_pos = cache_dic[lang][hash_value]['end_pos']
        srl = cache_dic[lang][hash_value]['srl']
        
        if 'count' not in cache_dic[lang][hash_value].keys():
            cache_dic[lang][hash_value]['count'] = 1
        else:
            cache_dic[lang][hash_value]['count'] += 1

        print("--------------The annotations is loaded from cache_srl --------------")


        return tokens, end_pos, srl, cache_dic


    def add(self, text, hash_value, tokens, end_pos, annjsonSRL, cache_dic, lang='eng'):

        cache_dic[lang][hash_value] = {}
        cache_dic[lang][hash_value]['text'] = text
        cache_dic[lang][hash_value]['tokens'] = tokens
        cache_dic[lang][hash_value]['end_pos'] = end_pos
        cache_dic[lang][hash_value]['srl'] = annjsonSRL
        cache_dic[lang][hash_value]['count'] = 1

        print("--------------The annotations is not included in cache_srl--------------")

        return cache_dic

    
    def count(self, cache_dic):
        '''
        This function is used to count the number of sentence in a cache
        '''  
        num = sum([len(cache_dic[key]) for key in cache_dic.keys()])

        return num


    def write(self, cache_dic):

        json_dic = json.dumps(cache_dic, indent=4)
        with open('cache_SRL/cache_srl_'+ datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.json', 'w') as json_file:
            json_file.write(json_dic) 



