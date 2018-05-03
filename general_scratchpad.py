import os
import pandas as pd
import numpy as np
from dplython import (DplyFrame, X, diamonds, select, sift,
  sample_n, sample_frac, head, arrange, mutate, group_by,
  summarize, DelayFunction)

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
movies.columns

# get values
movies.Actor.values
movies.Rating.value_counts()

# distinct
movies.Genre.unique()
movies.Genre.value_counts()
movies[["Genre", "Rating"]].drop_duplicates()
# value_counts() and unique() don't work with dataframe, only with series
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

# mutate using replace
movies.Genre.replace("Sci-fi", "science_fiction")

# conditional mutate
movies["sale_greater_30"] = np.where(movies["Sales"] > 30, "yes", "no")
# note np.where only works with numeric
#movies["adventure_dummy"] = np.where(movies["Genre"] = "Adventure", "yes", "no")

# instead of np.where, create new var, then conditional mutate using .loc
movies = movies.assign(adventure_dummy = "no")
movies.loc[movies.Sales > 30]
movies.loc[movies.Sales > 30, "adventure_dummy"]
movies.loc[movies.Sales > 30, "adventure_dummy"] = ">30"


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
# apply axis = 0 (default) iterates over rows, axis = 1 iterates over columns, but same effect here
movies[["Actor", "Movie"]].apply(add_string, axis = 0)
movies[["Actor", "Movie"]].apply(add_string, axis = 1)

# lambda function on the fly
movies.Actor.apply(lambda row: "new_string_" + row)
movies[["Actor", "Movie"]].apply(lambda row: "new_string_" + row)
movies.groupby("Sales").apply(lambda x: x.mean())
movies.groupby("Genre").apply(lambda x: x.Sales.mean())
movies.groupby("Genre").apply(lambda x: x.Sales.mean()).reset_index(name = "mean")


# map function
# note that map only works on series, applymap only works on dataframes
movies.Actor.map(add_string)
movies.Actor.applymap(add_string)
movies[["Actor", "Movie"]].map(add_string)
movies[["Actor", "Movie"]].applymap(add_string)

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
eval_string = 'new_sales = Sales + 1'
eval_string
movies.eval('new_sales = Sales + 1')
movies.eval('new_sales = Sales + 1', inplace = True)


# pipe function - note you need to wrap code including pipe in parenthesis for some kind of delayed eval
# pipe: return only series
def plus1_series(dataframe, variable):
        return dataframe[variable] + 1
plus1_series(dataframe = movies, variable = ["Sales"])
movies.pipe(plus1_series, variable = ["Sales"])

# pipe: return entire df
def plus1_df(dataframe, variable):
        return dataframe.assign(new_var = dataframe[variable] + 1)
plus1_df(dataframe = movies, variable = ["Sales"])
movies.pipe(plus1_df, variable = ["Sales"])
# pipe with tidy eval
new_var = "Sales"
movies.pipe(plus1_df, variable = [new_var])

# multiple pipes into each other
def copy_var(dataframe, variable):
        return dataframe.\
        assign(new_var2 = dataframe[variable])
copy_var(dataframe = movies, variable = ["Genre"])
movies.pipe(plus1_df, variable = ["Sales"]).pipe(copy_var, variable = ["Sales"])

# multiple arguments to a pipe function
def join_string(dataframe, variable, string):
        return dataframe.assign(new_var3 = dataframe[variable] + string)
join_string(dataframe = movies, variable = ["Genre"], string = "test")
movies.pipe(plus1_df, variable = ["Sales"])\
        .pipe(copy_var, variable = ["Sales"])\
        .pipe(join_string, variable = ["Genre"], string = "test")


########################################################
#######################################################
#######################################################


# dplython select
# https://pythonhosted.org/dplython/
movies_dpf = DplyFrame(movies)
movies_dpf
movies_dpf >> select(X.Actor) >> head(5)

# dplython 
movies.count()
movies_dpf.count()
movies_dpf >> group_by(X.Genre) >> \
        summarize(avg_sales = X.Sales.mean(), genre_count = X.Actor.size())

