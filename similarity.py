import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns
import pyspark
from pyspark.sql import SQLContext
sc = pyspark.SparkContext()

PATH = "utility_matrix.csv"

ratings = pd.read_csv("utility_matrix.csv", header='infer')
ratings.drop('userName', axis=1, inplace=True)
ratings = np.array(ratings)

users = {}
places = []
theta = 4

for line in ratings:
    user_name = line[2]
    if user_name not in users:
        users[user_name] = 1
    else:
        users[user_name] += 1

#print(users)
users_2 = []
users_3 = []
users_4 = []
users_5 = []
users_6 = []
users_theta = []

for key in users:
    if users[key] >= 2:
        users_2.append(key)
    if users[key] >= 3:
        users_3.append(key)
    if users[key] >= 4:
        users_4.append(key)
    if users[key] >= 5:
        users_5.append(key)
    if users[key] >= 10:
        users_6.append(key)
    if users[key] >= theta:
        users_theta.append(key)

#print(users_theta)

"""
print(len(users_2)) # 5051
print(len(users_3)) # 2096
print(len(users_4)) # 1021
print(len(users_5)) # 557
print(len(users_9)) # 89
print(len(users_10)) # 62
"""
print(len(users_theta))

places = []
for line in ratings:
    name = line[2]
    place = int(line[0])
    if name in users_theta:
        if place not in places:
            places.append(place)

places.sort()
print(len(places))  # 45

df = np.zeros((len(places), len(users_theta)))
df2 = np.zeros((len(places), len(users_theta)))

for line in ratings:
    name = line[2]
    place = int(line[0])
    rating = int(line[1])
    if name in users_theta:
        u_idx = users_theta.index(name)
        p_idx = places.index(place)
        df[p_idx, u_idx] = rating
        df2[p_idx, u_idx] = rating

# zero-based
for row, p_rating in enumerate(df):
    rated = [x for x in p_rating if x != 0]
    row_avg = sum(rated) / len(rated)
    for col, rating in enumerate(p_rating):
        if rating != 0:
            df[row, col] -= row_avg
# print(df)

similarity = cosine_similarity(df)

print(similarity)
sns.heatmap(similarity, xticklabels=places, yticklabels=places, cmap='viridis')
plt.show()
