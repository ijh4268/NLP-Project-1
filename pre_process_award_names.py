import json
import nltk

new_arr = []
with open("gg2013.json", "r") as file:
    s = json.load(file)
    count = 0
    for i in range(len(s)):
        s[i].pop('id')
        s[i].pop('user')
        words = s[i]['text'].lower().split()
        if "best" in words:
            new_arr.append(s[i])

        else:
            for j in range(len(words)-1):
                if "goes" == words[j]:
                    if "to" == words[j+1]:

                        new_arr.append(s[i])
    json_str = json.dumps(new_arr)
    out = open("pre_process_2013.json", "w")
    out.write(json_str)
    out.close()
