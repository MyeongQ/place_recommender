import numpy as np
import pandas as pd

file_name = 'place_infos.txt'

with open(file_name, 'r', encoding='utf-8') as f:
    lines = f.readlines()

locals = []
place_profiles=[]
count = 0
for line in lines:
    if line[0] == '[':
        local = line.strip('[]\n')
        locals.append(local)

    elif line != '\n':
        count += 1
        if count==1:
            name = line.strip()
        else:
            line = line.strip()
            if line.isdigit() or (len(line)==3 and line[1]=='.'):
                rank_avg = float(line)
            elif line[0]=='(':
                line = line.strip('()')
                num_reviews = 0
                if ',' in line:
                    num_reviews += int(line.split(',')[0])*1000
                    num_reviews += int(line.split(',')[1])
                else:
                    num_reviews = int(line)

            else:
                describe = line
    # '/n'
    else:
        if count>0:
            place_profiles.append({"local":local, "name":name, "rank_avg":rank_avg, "num_reviews":num_reviews, "describe":describe})

        count = 0
        rank_avg = 0
        num_reviews = 0
        describe = ''


print(locals)
place_profs = []
for item in place_profiles:
    if item["rank_avg"]==0 or item["num_reviews"] < 50: continue
    place_profs.append([item["local"], item["name"], item["rank_avg"], item["num_reviews"], item["describe"]])

place_profs = np.array(place_profs)

for line in place_profs:
    print(line)
df = pd.DataFrame(place_profs)
df.to_csv('place_profile.csv')
