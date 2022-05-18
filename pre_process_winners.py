import json
import nltk

name_matching = {}
name_matching['cecil b. demille award'] = ['demille award']
name_matching['best motion picture - drama'] = ['best picture', 'best drama']
name_matching['best performance by an actress in a motion picture - drama'] = ['best actress drama']
name_matching['best performance by an actor in a motion picture - drama'] = ['best actor drama']
name_matching['best motion picture - comedy or musical'] = ['best picture', 'best comedy', 'best musical']
name_matching['best performance by an actress in a motion picture - comedy or musical'] = ['best actress comedy', 'best actress musical', 'best comedy actress', 'best musical actress']
name_matching['best performance by an actor in a motion picture - comedy or musical'] = ['best actor comedy', 'best actor musical', 'best comedy actor', 'best musical actor']
name_matching['best animated feature film'] = ['best animated']
name_matching['best foreign language film'] = ['best foreign']
name_matching['best performance by an actress in a supporting role in a motion picture'] = ['best supporting actress']
name_matching['best performance by an actor in a supporting role in a motion picture'] = ['best supporting actor']
name_matching['best director - motion picture'] = ['best director']
name_matching['best screenplay - motion picture'] = ['best screenplay']
name_matching['best original score - motion picture'] = ['best score', 'best original score']
name_matching['best original song - motion picture'] = ['best song', 'best original song']
name_matching['best television series - drama'] = ['best television series', 'best TV drama']
name_matching['best performance by an actress in a television series - drama'] = ['best actress TV drama']
name_matching['best performance by an actor in a television series - drama'] = ['best actor TV drama']
name_matching['best television series - comedy or musical'] = ['best television series', 'best TV comedy', 'best TV musical']
name_matching['best director - motion picture'] = ['best director']
name_matching['best television series - comedy or musical'] = ['best tv comedy', 'best tv musical', 'best tv comedy or musical']
name_matching['best performance by an actress in a television series - comedy or musical'] = ['best actress TV', 'best actress television']
name_matching['best performance by an actor in a television series - comedy or musical'] = ['best actor TV', 'best actor television']
name_matching['best mini-series or motion picture made for television'] = ['best TV show', 'best television show', 'best show']
name_matching['best performance by an actress in a mini-series or motion picture made for television'] = ['best actress TV', 'best actress television']
name_matching['best performance by an actor in a mini-series or motion picture made for television'] = ['best actor TV', 'best actor television']
name_matching['best performance by an actress in a supporting role in a series, mini-series or motion picture made for television'] = ['best supporting actress']
name_matching['best performance by an actor in a supporting role in a series, mini-series or motion picture made for television'] = ['best supporting actor']

new_arr = []
with open("gg2015.json", "r") as file:
    s = json.load(file)
    for i in range(len(s)):
        s[i].pop('id')
        s[i].pop('user')
        words = s[i]['text'].lower()
        
        for award in name_matching.keys():
            if award in words:
                new_arr.append((s[i], award))
            else:
                for colloquial in name_matching[award]:
                    if colloquial in words:
                        new_arr.append((s[i], award))
    json_str = json.dumps(new_arr)
    out = open("pre_process_winners_2015.json", "w")
    out.write(json_str)
    out.close()