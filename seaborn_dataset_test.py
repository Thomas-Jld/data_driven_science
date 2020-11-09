import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df = sns.load_dataset("iris")

print(min(df["sepal_width"]))
print(max(df["sepal_width"]))


fig, ax = plt.subplots()


x = df["petal_length"]
y = df["petal_width"]

labels = ["setosa", "versicolor", "virginica"]
cols = ['#ce125680', '#23844380', '#fc4e2a80']

color = {"setosa": cols[0], "versicolor": cols[1], "virginica": cols[2]}

colors = [color[species] for species in df["species"]]
sizes = [[10+2**(3*(length - min(df["sepal_length"]))) for length in df["sepal_length"]],
        [10+2**(3*(length - min(df["sepal_width"]))) for length in df["sepal_width"]]]

ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=col) for col in cols], labels=labels)

ax.set_xlabel("petal_length")
ax.set_ylabel("petal_width")
ax.set_title("Differenciation of species based on petal dimensions")

plt.scatter(x, y, s = sizes[0], c=colors)
plt.scatter(x, y, s = sizes[1], c=colors)
plt.show()