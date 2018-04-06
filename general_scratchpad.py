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
# .value_counts doesn't work with multiple variables apparently
#movies[["Genre", "Rating"]].value_counts()


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
        pivot(index = "Genre", columns = "Rating", values = "n").reset_index().\
        rename_axis(None, axis = 1)

movies.groupby(["Movie", "Genre", "Rating"]).size().reset_index(name = "n").\
        assign(genre_rating = movies.Genre.str.cat(movies.Rating, sep = "_")).\
        pivot(index = "Movie", columns = "genre_rating", values = "n").reset_index().\
        rename_axis(None, axis = 1)
        
# gather
movies_gather = movies.groupby(["Genre", "Rating"]).size().reset_index(name = "n").\
        pivot(index = "Genre", columns = "Rating", values = "n").reset_index().\
        rename_axis(None, axis = 1)
movies_gather
movies_gather.melt(id_vars = ["Genre"], value_vars = ["PG-13", "R"], 
                   var_name = "Rating", value_name = "movie_count")

# bind_rows
movies1 = movies.iloc[0:5, ]
movies1
movies2 = movies.iloc[5:, ]
movies2
movies_original = movies1.append(movies2)
movies_original

movies3 = movies.iloc[0:5, 0:1]
movies3
movies_new = movies3.append(movies2)
movies_new

# bind_cols
movies1 = movies.iloc[:, 0:2]
movies1
movies2 = movies.iloc[:, 2:]
movies2
movies_concat = pd.concat([movies1, movies2], axis = 1)
movies_concat

# left_join
movies1 = movies.iloc[:, 0:2]
movies1
movies2 = movies.iloc[:, 1:]
movies2
movies_new = pd.merge(left = movies1, right = movies2, how = "left", 
                      left_on = ["Actor"], right_on = ["Actor"])
movies_new

# purrr
movies.Sales + 1

def add_string(column):
        return "new_string_" + column

add_string(movies.Actor)  
movies.Actor.apply(add_string)
movies[["Actor", "Movie"]].apply(add_string)

# tidy eval
var_name = "Actor"
movies[var_name]      

var_name2 = "Movie"
movies[[var_name, var_name2]]
