import json
import nltk

def pre_process(year):
    new_arr = []
    with open("gg" + str(year) + ".json", "r") as file:
        s = json.load(file)
        for i in range(len(s)):
            s[i].pop('id')
            s[i].pop('user')
            words = s[i]['text'].lower().split()
            if "best" in words:
                new_arr.append(s[i])
        json_str = json.dumps(new_arr)
        out = open("pre_process_" + str(year) + ".json", "w")
        out.write(json_str)
        out.close()
