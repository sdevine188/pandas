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
movies = movies.assign(new_movie_title = movies.Movie)
movies["sale_greater_30"] = np.where(movies["Sales"] > 30, "yes", "no")
# note np.where only works with numeric
#movies["adventure_dummy"] = np.where(movies["Genre"] = "Adventure", "yes", "no")

# instead of np.where, create new var, then conditional mutate using .loc
movies = movies.assign(adventure_dummy = "no")
movies.loc[movies["Sales"] > 30]
movies.loc[movies["Sales"] > 30, "adventure_dummy"]
movies.loc[movies["Sales"] > 30, "adventure_dummy"] = ">30"


# filters
movies[(movies.Genre == "Adventure") | (movies.Genre == "Documentary")]
movies.query("Genre == 'Adventure' | Genre == 'Documentary'")
movies.query("Genre in ['Adventure', 'Documentary']")
movies.query("Rating == 'R' & Sales > 20")

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

# tidy eval select
var_name = "Actor"
movies[var_name]      

var_name2 = "Movie"
movies[[var_name, var_name2]]

# tidy eval query
# tidy eval with local variables uses the @ symbol instead of !! to unquote
value1 = "Dunkirk"
movies.query("Movie == @value1")

var1 = "Movie"
query_string = var1 + " == '" + value1 + "'"
query_string
movies.query(query_string)

movies.query("{} == 'Dunkirk'".format(var1))
movies.query("{} == @value1".format(var1))
movies.query("{} == '{}'".format(var1, value1))

# tidy eval rename
var1 = "Movie"
new_var = "new_movie_title"
movies.rename(columns = {"Movie" : "new_movie_title"})
movies.rename(columns = {var1 : new_var})


# tidy eval: the eval function can be used for numeric calculations
movies.eval('new_sales = Sales + 1')
movies.eval('new_sales = Sales + 1', inplace = True)


