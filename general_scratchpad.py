import os
import pandas as pd
import numpy as np

# set working directory
os.chdir("C:/Users/Stephen/Desktop/Python/pandas")
os.getcwd()
os.listdir(".")

x = "test2"
x


##############################

#https://pandas.pydata.org/pandas-docs/stable/comparison_with_r.html

# read in data
movies = pd.read_csv("movies.csv")

# inspect
movies.shape
movies.head()
movies.tail(2)
movies.describe()

# select data
list(movies)
movies.Actor
movies.Actor[0:3]
movies[0:2]
movies[["Movie", "Actor"]]
movies.loc[:, "Movie":"Rating"]
movies.drop(['Movie', 'Actor'], axis = 1)

# get values
movies.Actor.values
movies.Rating.value_counts()

# distinct
movies[["Genre", "Rating"]].drop_duplicates()
movies[["Genre", "Rating"]].value_counts()


# arrange
movies.sort_values("Sales")
movies.sort_values("Sales", ascending = False)
movies.sort_values(["Rating", "Sales"])
movies.sort_values(["Rating", "Sales"], ascending = [False, True])

# rename
movies.rename(columns = {"Movie" : "new_movie_title"})

# mutate
movies.assign(new_movie_title = movies.Movie)

# filters
movies[(movies.Genre == "Adventure") | (movies.Genre == "Documentary")]
movies.query("Genre == 'Adventure' | Genre == 'Documentary'")
movies.query("Genre in ['Adventure', 'Documentary']")

# summarize
movies.groupby("Genre").agg(["mean", "sum", "count"])

# group summarizing
# note to get grouped counts, you need size function, but it returns 
# a pd.series, not pd.dataframe, which has the counts as an index  aka rowname
# so we need to use reset.index to convert index/rowname into a variable
# then also name the new variable
movies.groupby("Genre").agg(["mean", "sum", "count", "size"])
movies.groupby("Genre").agg({"Movie": "count", "Sales": ["mean", "sum", "count"]})

movies.groupby(["Genre", "Rating"]).agg(["count"])
movies.groupby(["Genre", "Rating"]).count()
movies.groupby(["Genre", "Rating"]).count().reset_index()
movies.groupby(["Genre", "Rating"]).size()
movies.groupby(["Genre", "Rating"]).size().reset_index()
movies.groupby(["Genre", "Rating"]).size().reset_index(name = "n")
#pd.DataFrame({"count" : movies.groupby(["Genre", "Rating"]).size()})
#pd.DataFrame({'count' : movies.groupby(["Genre", "Rating"]).size()}).reset_index()


#x = movies.groupby(["Genre", "Rating"]).size()
#x
#x.head(2)
#x[0:2]
#list(x)
#type(x)
#x.index

# spread
movies.groupby(["Genre", "Rating"]).size().reset_index(name = "n").\
        pivot_table(values = "n", index = "Genre", columns = "Rating", aggfunc = "sum")

movies.groupby(["Movie", "Genre", "Rating"]).size().reset_index(name = "n").\
        





















