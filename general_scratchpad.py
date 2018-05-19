import os
import pandas as pd
import numpy as np
import seaborn as sns
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


##############################################33


# select data
list(movies)
movies.Actor
movies.Actor[0:3]
movies[0:2]
movies[["Movie", "Actor"]]
movies.loc[:, "Movie":"Rating"]
movies.drop(['Movie', 'Actor'], axis = 1)
movies.columns
# note single brackets or dot subsetting just provides series without var name
# but double brackets returns dataframe
movies.Actor
movies["Actor"]
movies[["Actor"]]
# can convert a series back to dataframe with .to_frame(name = )
movies.Actor.to_frame(name = "Actor")

# get values
movies.Actor.values
movies.Rating.value_counts()


#################################################3


# distinct
movies.Genre.unique()
movies.Genre.value_counts()
movies[["Genre", "Rating"]].drop_duplicates()
# value_counts() and unique() don't work with dataframe, only with series
#movies[["Genre", "Rating"]].value_counts()


#######################################################


# arrange
movies.sort_values("Sales")
movies.sort_values("Sales", ascending = False)
movies.sort_values(["Rating", "Sales"])
movies.sort_values(["Rating", "Sales"], ascending = [False, True])


#############################################################


# rename
movies.rename(columns = {"Movie" : "new_movie_title"})


#############################################


# mutate
movies.assign(new_movie_title = movies.Movie)
movies = movies.assign(new_movie_title = movies.Movie)


# case_when
# mutate using replace
# replace using a dictionary
# regex = False requires the entire pattern to match the entire value
movies.replace({"Actor" : "Tom Hardy", "Movie" : "AI"}, "awesome")
movies.replace({"Actor" : {"Tom Hardy" : "Tom", "Sam Neil" : "Sam"}})
movies.replace({"Actor" : {"Tom H" : "Tom", "Sam Neil" : "Sam"}})
movies.replace({"Actor" : {"Tom H" : "Tom", "Sam Neil" : "Sam"}}, regex = True)
movies.replace({"Actor" : {"Tom Hardy" : "Tom", "Sam Neil" : "Sam"}}).\
               replace({"Movie" : {"Dunkirk" : "great", "AI" : "awesome"}})
# regex = True allow for partial string replacements
movies.replace({"Actor" : "e"}, {"Actor": "z"}, regex = True)
# replace with tidy eval
replacement_variable = "Actor"
replacement_value_start = "Tom Hardy"
replacement_value_end = "Tom"
movies.replace({replacement_variable : {replacement_value_start : replacement_value_end}})

replacement_df = pd.DataFrame({"replacement_variable" : ["Actor", "Movie"], 
                              "replacement_value_start" : ["Tom Hardy", "AI"],
                              "replacement_value_end" : ["Tom", "awesome"]})
replacement_df
movies.replace({replacement_df.replacement_variable[0] : \
                       {replacement_df.replacement_value_start[0] : replacement_df.replacement_value_end[0]}})


# additional options for case_when, but dictionary seems best
#movies.replace({"Actor" : "Tom Hardy"}, {"Actor": "great_actor"})
#movies.replace({"Actor" : "Tom"}, {"Actor": "great_actor"})
# replace specifc value in specific variable
#movies.Genre.replace("Sci-fi", "science_fiction")
## replace a list of values
#movies.Genre.replace(["Sci-fi", "Adventure"], "good_movies")
## replace using two paired lists of values
#movies.Genre.replace(["Sci-fi", "Adventure"], ["science_fiction", "super_fun"])

# conditional mutate
movies["sale_greater_30"] = np.where(movies["Sales"] > 30, "yes", "no")
# note np.where only works with numeric
#movies["adventure_dummy"] = np.where(movies["Genre"] = "Adventure", "yes", "no")


##############################################3


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
movies.Actor.to_frame(name = "Actor").query("Actor == 'Tom Hardy'")


##########################################################


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


######################################################


# tidyr

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


#############################################################


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


##########################################################


# purrr
movies.Sales + 1

def add_string(column):
        return "new_string_" + column

def get_variable_type(variable):
        return(variable.dtype.name)
        
movies.apply(get_variable_type)
movies.dtypes

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


#########################################################


# pipe function 
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


  
#########################################################        
        
        
# janitor tabyl / table
pd.crosstab(movies.Genre, movies.Rating)
type(pd.crosstab(movies.Genre, movies.Rating))
pd.crosstab(movies.Genre, movies.Rating).columns
pd.crosstab(movies.Genre, movies.Rating)["PG-13"]
pd.crosstab(movies.Genre, movies.Rating)["PG-13"].reset_index()
pd.crosstab(movies.Genre, movies.Rating)["PG-13"].reset_index().Genre
pd.crosstab(movies.Genre, movies.Rating, margins = True)

# to get percentages, use normalize
# normalize = "all", "index" (for rows), or "columns"
pd.crosstab(movies.Genre, movies.Rating, margins = True, normalize = "all")
pd.crosstab(movies.Genre, movies.Rating, margins = True, normalize = "index")
pd.crosstab(movies.Genre, movies.Rating, margins = True, normalize = "columns")

# can run crosstab on multiple variables
pd.crosstab([movies.Genre, movies.Movie], movies.Rating, margins = True)


################################################


# if/else statement
value = 2
if value > 5:
        print("greater_than_5")
elif value > 4:
        print("greater_than_4")
else: 
        print("less_than_or_equal_to_4")


#########################################################
        
        
# for loop
for sale_amount in movies["Sales"]:
        print(sale_amount + 1)
        
        
###############################3

        
# count missing variables
def count_missing_values(variable):
        return(variable.isnull().sum())
movies.apply(count_missing_values)  


#########################################################


# stringr

# count # of matches
movies.Actor
movies.Actor.str.count("t")
# ignore_case
movies.Actor.str.lower()
movies.Actor.str.lower().str.count("t")

# find index of match
# notice it return -1 if pattern is not found
movies.Actor.str.lower().str.find("t")
movies.Actor.str.lower().str.find("t", start = 0, end = 1)
movies.Actor.str.lower().str.find("t", start = 0, end = 1).replace()

# slice
movies.Actor.str.slice(start = 0, stop = 3)


#########################################


# plotting with seaborn
arrests = pd.read_csv("us_arrests.csv")
arrests.shape
arrests.head(5)

# histogram
sns.distplot(arrests.Rape)
sns.distplot(arrests.Rape, kde = False, rug = True)

# scatterplot
sns.jointplot(x = arrests.UrbanPop, y = arrests.Assault)

# correlation matrix / corrplot
sns.pairplot(arrests)

# boxplot
arrests.UrbanPop.max()
arrests.UrbanPop.min()
arrests = arrests.assign(high_pop = "no")
arrests.loc[arrests.UrbanPop > 50, "high_pop"] = "yes"

sns.boxplot(x = arrests.high_pop, y = arrests.Murder)

# barplot
sns.barplot(x = "high_pop", y = "Murder", data = arrests)
      
        

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

