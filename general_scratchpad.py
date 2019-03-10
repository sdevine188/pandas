import os
import pandas as pd
import numpy as np
import seaborn as sns
#from dplython import (DplyFrame, X, diamonds, select, sift,
#  sample_n, sample_frac, head, arrange, mutate, group_by,
#  summarize, DelayFunction)

# set working directory
os.chdir("C:/Users/Stephen/Desktop/Python/pandas")
os.getcwd()
os.listdir()

x = "test2"
x


##############################


# remove all varaibles currently in environment
#%reset

# remove particular variable
x = "test"
x

x = None
x


#################################################

#https://pandas.pydata.org/pandas-docs/stable/comparison_with_r.html

# read in csv
movies = pd.read_csv("movies.csv")

# read in .txt
text = pd.read_fwf("pride.txt")
text

# write csv
movies.to_csv("movies_test_to_csv.csv", index = False)

# inspect
# note that read_csv converts blanks, NA, or NaN into NaN
movies
movies.shape
movies.head()
movies.tail(2)
movies.describe()
movies.dtypes
movies.columns


################################################


my_list = ["test", "test2", "abc"]
my_list

# create dataframe from scratch - format is like a dictionary
new_df = pd.DataFrame({"var_name" : my_list})
new_df = pd.DataFrame({"var_name" : ["test", "test2", "abc"], "var_name2" : ["test4", "test5", "ab6"]})
new_df
type(new_df)

# create just a series
new_series = pd.Series(my_list)
new_series = pd.Series(["test", "test2", "abc"])
new_series
type(new_series)


#####################################################


# copying dataframe - you need to use .copy() 
# if not, the "copy" is just a relabeld version of the original, and changes to "copy" affect original

# this is what happens without .copy()
movies
movies2 = movies
movies2.loc[movies.Actor == "Harrison Ford", "Actor"] = "Edward Norton"
movies2
movies

# this is desired/correct behavior with .copy()
movies2 = movies.copy()
movies2.loc[movies.Actor == "Edward Norton", "Actor"] = "Christian Bale"
movies2
movies


#################################################


# missing values
# check for missing
movies.apply(lambda x: x.isnull())
movies.apply(lambda x: x.isnull().sum())

# drop na values
movies.Movie.dropna()
movies.dropna()

# fill na values
movies.Sales.fillna("na_fill")
movies.fillna("na_fill")

# create fill_na function that can be used in .apply (since .fillna is just at method)
def fill_na(df_column, replacement = "na_fill"):
        return(df_column.fillna(replacement))
movies.apply(fill_na, replacement = "na_test")

# add na values
movies.loc[4:4, "Actor"]
movies.loc[4:4, "Actor"] = "NaN"  # a sting value of "NaN" doesn't work
movies
movies.apply(lambda x: x.isnull().sum())
movies.loc[4:4, "Actor"] = np.nan
movies
movies.apply(lambda x: x.isnull().sum())


movies.loc[4:4, "Sales"]
movies.loc[4:4, "Sales"] = np.nan
movies

movies2 = movies.replace({"Actor" : {"HAL" : np.nan}}).copy()
movies2
movies2.apply(lambda x: x.isnull().sum())


######################################################


# convert numeric to string
movies.dtypes
movies[["Sales"]] = movies[["Sales"]].astype(str)
movies.dtypes
movies

# convert string to numeric
movies[["Sales"]] = movies[["Sales"]].astype(float)
movies.dtypes
movies


##############################################33


# select data
list(movies)
movies.Actor
movies.Actor[0:3]
movies[0:2]
movies[["Movie", "Actor"]]
movies[["Actor", "Movie"]]
movies.loc[1:2, "Movie"]
movies.loc[0:0, "Movie"]
movies.loc[:, "Movie"]
movies.loc[:, ["Movie", "Rating"]]
movies.loc[:, "Movie":"Rating"]
movies.drop(['Movie', 'Actor'], axis = 1)
movies.columns

# select all variables except some
movies.drop(['Movie', 'Actor'], axis = 1)
#movies.loc[:, ~(movies.columns.isin(["Actor"]))]

# select columns using regex
movies.loc[:, movies.columns.str.contains(pat = "^Act", case = False, regex = True)]


# note single brackets or dot subsetting just provides series without var name
# but double brackets returns dataframe
movies.Actor
movies["Actor"]
movies[["Actor"]]
# can convert a series back to dataframe with .to_frame(name = )
movies.Actor.to_frame(name = "Actor")


##################


# get values
# aka pull() from dplyr

# preferred is using square brackets and quoted var name, as opposed to df.var method

# note you can't easily get values as a list from a dataframe, need to get it from a series
movies[["Actor"]].tolist()
# can get an array, but each value is its own list
movies[["Actor"]].values
movies[["Actor"]].values.tolist()
list(movies[["Actor"]].values.flat)
movies[["Actor", "Sales"]].values
# to convert this array of nested lists, you need to flatten the array, then convert to a list
list(movies[["Actor"]].values.flat)
list(movies[["Actor", "Sales"]].values.flat)


##############


# can get a list from a series with tolist()
movies["Actor"].tolist()
movies.Actor.tolist()

# .values method to get clean array from series
movies["Actor"].values
movies["Actor"].values[0]
movies["Actor"].values[0:5]
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

# add var as series
type(movies.Movie)
type(movies["Movie"])
movies.assign(new_movie_title = movies.Movie)
movies = movies.assign(new_movie_title = movies.Movie)

# add var as list
actor_var_as_list = movies.Actor.tolist()
actor_var_as_list = movies["Actor"].tolist()
type(actor_var_as_list)
movies = movies.assign(new_actor_var2 = actor_var_as_list)
movies

# add var as array
actor_var_as_array = movies["Actor"].values
actor_var_as_array = movies.Actor.values
type(actor_var_as_array)
movies = movies.assign(new_actor_var3 = actor_var_as_array)
movies

# case_when
# best way to conditional mutate is using .loc
movies2 = movies.copy()
movies2
movies2.loc[(movies.Genre == "Documentary") | (movies.Genre == "Adventure"), "Genre"] = "best_genre"
movies2.loc[(movies.Genre.isin(["best_genre", "Sci-fi"])), "Genre"] = "new_best_genre"
movies2

# case_when
# mutate using replace can require less coding than .loc for multiple specific replacements
# replace using arrays
movies.Genre.replace("Sci-fi", "science_fiction")
movies.Genre.replace(["Sci-fi", "Adventure"], "good_movies")
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
#movies["sale_greater_30"] = np.where(movies["Sales"] > 30, "yes", "no")
# note np.where only works with numeric
#movies["adventure_dummy"] = np.where(movies["Genre"] = "Adventure", "yes", "no")


##############################################3


# instead of np.where, create new var, then conditional mutate using .loc
movies = movies.assign(adventure_dummy = "no")
movies.loc[movies.Sales > 30]
movies.loc[movies.Sales > 30, "adventure_dummy"]
movies.loc[movies.Sales > 30, "adventure_dummy"] = ">30"


# filters
# best way to filter is with .loc
movies.loc[(movies.Genre == "Documentary") | (movies.Actor == "Tom Hardy"), :]
movies.loc[(movies.Genre.isin(["Documentary", "Adventure"])) & (movies.Sales > 30), :]
movies.loc[~(movies.Genre.isin(["Documentary", "Adventure"])) & (movies.Sales > 30), :]
movies.loc[movies.Genre != "Documentary", :]


# can also filter with .query()
#movies[(movies.Genre ==. "Adventure") | (movies.Genre == "Documentary")]
#movies.query("Genre == 'Adventure' | Genre == 'Documentary'")
#movies.query("Genre in ['Adventure', 'Documentary']")
#movies.query("Rating == 'R' & Sales > 20")
#movies.query("Actor == 'Tom Hardy'").Actor
#movies.query("Actor == 'Tom Hardy'").Actor.to_frame(name = "Actor")


##########################################################


# print output as table
movies
print(movies[["Actor", "Movie"]].to_string())


########################################################


# summarize
movies.groupby("Genre").agg(["mean", "sum", "count"])
movies[["Sales"]].apply(lambda x: x.mean())

# group summarizing
# agg is the preferred way to summarize
movies.groupby("Genre", as_index = False).agg({"Sales": ["mean", "sum", "count", "size"]})
movies.groupby("Genre", as_index = False).agg({"Movie": "count", "Sales": ["mean", "sum", "count", "size"]})
movies_summary = movies.groupby("Genre", as_index=False).\
        agg({"Movie": "count", "Sales": ["mean", "sum", "count", "size"]})
type(movies_summary)
movies_summary
# agg returns a dataframe, but need to reset column names
# reset_index only resets the row index, to reset columns would require more painful reset_index parameters
# instead, just use map to merge column names from index and re-assign as new column names
# note apply only works on pandas series/df, not on lists, which is what the col names are
movies_summary.columns.values
movies_summary.columns = list(map("_".join, movies_summary.columns.values))
movies_summary


# note to get grouped counts, you need size function, but it returns 
# a pd.series, not pd.dataframe, which has the counts as an index  aka rowname
# so we need to use reset.index to convert index/rowname into a variable
# then also name the new variable
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
movies_spread = movies.groupby(["Genre", "Rating"]).size().reset_index(name = "n").\
        pivot(index = "Genre", columns = "Rating", values = "n").reset_index().\
        rename_axis(None, axis = 1)
movies_spread

movies_spread.melt(id_vars = ["Genre"], value_vars = ["PG-13", "R"], 
                   var_name = "Rating", value_name = "movie_count")

# melt also works when there is no id_vars is specified
movies_spread.melt(value_vars = ["PG-13", "R"], 
                   var_name = "Rating", value_name = "movie_count")

# also works when you don't reference all columns by name
movies_spread.melt(value_vars = movies_spread.columns, 
                   var_name = "Rating", value_name = "movie_count")

columns_to_melt = ["PG-13", "R"]
movies_spread.melt(value_vars = columns_to_melt, 
                   var_name = "Rating", value_name = "movie_count")

movies_spread.melt(id_vars = ["Genre"], value_vars = columns_to_melt, 
                   var_name = "Rating", value_name = "movie_count")

#############################################################


# bind_rows
movies.iloc[0:5, :]
movies.iloc[:, 2]
# note that the second number after ":" is excluded, 
#so to get a single row as a dataframe, must be like .iloc[5:6, ]
movies.iloc[5:6, :]
type(movies.iloc[5:6, :])
# if you just index with one number, it returns the row as a series, which is weird
movies.iloc[5, :]
type(movies.iloc[5, :])

movies1 = movies.iloc[0:5, :]
movies1
movies2 = movies.iloc[5:, :]
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
# apply is the best to use when you want the output returned by the function; 
# works on dataframe (df[["<var>"]]) or series (df.var or df["<var>"]) 
#http://jonathansoma.com/lede/foundations/classes/pandas%20columns%20and%20functions/apply-a-function-to-every-row-in-a-pandas-dataframe/

# if you only want the side effect of the function (not what is returned) use a for loop
# because apparently for some crazy reason, apply is called twice on the first row???
# https://stackoverflow.com/questions/50477664/count-iterations-of-pandas-dataframe-apply-function
movies.Sales + 1

# create function relying on the actual values as input (so .apply is passed a series not a dataframe)
def classify_sales(sale_amount):
        if(sale_amount > 20):
                return("high_sales")
        else:
                return("low_sales")

# note that .apply can receive a dataframe or a series
# when inputting a series, .apply iterates through the actual values
# but when inputting a df, .apply iterates through the columns
# so to iterate through actual values of each column in a dataframe, you need to 
# use a pass .apply a lambda function that converts each column into a series, 
# on which you then .apply your function of interest (see below)
# the transform is: .apply(lambda x: pd.Series(list(x.values.flat))
# purrr map functions behave like they always receive a series, iterating through values 

# when .apply is passed the dataframe, it can do operations to entire column vectors
movies[["Sales"]].apply(lambda x: x + 1)
# but can't process each individual value of a vector the way you can when .apply gets a series
movies[["Sales"]].apply(lambda x: x[0])
movies.Sales.apply(lambda x: x[0])

# dataframe
movies = movies.assign(Sales_2 = movies.Sales + 10)
type(movies[["Sales"]])
movies[["Sales"]].apply(classify_sales)
movies[["Sales"]].apply(lambda x: type(x))
movies[["Sales"]].apply(lambda x: type(x.values))
pd.Series(list(movies[["Sales"]].values.flat)).apply(classify_sales)
movies[["Sales"]].apply(lambda x: pd.Series(list(x.values.flat)).apply(classify_sales))
movies[["Sales", "Sales_2"]].apply(lambda x: pd.Series(list(x.values.flat)).apply(classify_sales))

# series
type(movies["Sales"])
movies["Sales"].apply(classify_sales)
type(movies.Sales)
movies.Sales.apply(classify_sales)


###############


def add_string(column):
        return "new_string_" + column

def get_variable_type(variable):
        return(variable.dtype.name)
        
# note .apply does not work on lists
# need to use lambda function or list comprehension
list_of_strings = ["lincoln", "obama", "fdr"]
list_of_strings.apply(add_string)
[("new_string_" + string) for string in list_of_strings]

# using .apply on dataframes        
movies.apply(get_variable_type)
movies.dtypes

add_string(movies.Actor)  
movies.Actor.apply(add_string)
movies["Actor"].apply(add_string)
movies[["Actor", "Movie"]].apply(add_string)
# apply axis = 0 (default) iterates over rows, axis = 1 iterates over columns, but same effect here
movies[["Actor", "Movie"]].apply(add_string, axis = 0)
movies[["Actor", "Movie"]].apply(add_string, axis = 1)


############


# can use .apply(axis = 1) to apply function to each row, like with pmap
movies = movies.assign(Sales_2 = movies.Sales + 10)
movies.loc[1:5, "Sales"] = [55, np.nan, 65, 85, 95]

# create get_higher_sales
def get_higher_sales(row_df):
        if(row_df.Sales >= row_df.Sales_2):
                return(row_df.Sales)
        else:
                return(row_df.Sales_2)
movies.assign(higher_sales = movies.apply(get_higher_sales, axis = 1))


###########


# to update a variable from inside a function as a side effect,
# you need to first define that variable inside the function as a global variable
# this is like using the <<- "one level up" assignment operator in r
# and is similar to walk/pwalk where you call a function for its side effect, not any output

# note that *args allows for any number of unnamed arguments to be passed to function, like ... in r
# this isn't necessary if it's called on its own where i can deliberatly not pass anything
# like increment_counter_side_effect()
# but if i call the function on a pandas series with .apply, then it has to be able to handle the
# value .apply is passing it
# if needed, you can also use *kwargs for any number of named arguments
# https://stackoverflow.com/questions/919680/can-a-variable-number-of-arguments-be-passed-to-a-function

# create increment_counter_side_effect function
def increment_counter_side_effect(*args):
        global counter
        print("counter is at number " + str(counter))
        counter = counter + 1

# set counter
counter = 0

# call increment_counter_side_effect() by itself for side effect on counter variable
increment_counter_side_effect()
increment_counter_side_effect()
increment_counter_side_effect()
counter

# can also call function for side effect on variables using .apply w/ pandas
pd.DataFrame({"row_number" : list(range(1, 6))})  .row_number.apply(increment_counter_side_effect)
counter


###########

# lambda function on the fly
movies.Actor.apply(lambda row: "new_string_" + row)
movies[["Actor", "Movie"]].apply(lambda row: "new_string_" + row)
movies.groupby("Sales").apply(lambda x: x.mean())
movies.groupby("Genre").apply(lambda x: x.Sales.mean())
movies.groupby("Genre").apply(lambda x: x.Sales.mean()).reset_index(name = "mean")

########


# map function
# note that map only works on series using df.var and df["var"] format, df[["<var>"]] dataframes don't work
# applymap only works on dataframes
movies.Actor.map(add_string)
movies["Actor"].map(add_string)
movies[["Actor"]].map(add_string)

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

# overwrite existing df
movies2 = movies.rename(columns = {"Movie" : "new_movie_title"})
movies2

# tidy eval: the eval function can be used for numeric calculations
eval_string = 'new_sales = Sales + 1'
eval_string
movies.eval('new_sales = Sales + 1')
movies.eval('new_sales = Sales + 1', inplace = True)


##########################################################3


# list comprehension
[name for name in movies.Actor]
[(name + "_test") for name in movies.Actor]
movies["Actor_test"] = [(name + "_test") for name in movies.Actor]
movies

  
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
     

###########################################################
        
        
# try / catch style error/exception/warning handling
#https://jakevdp.github.io/WhirlwindTourOfPython/09-errors-and-exceptions.html
#https://code.tutsplus.com/tutorials/professional-error-handling-with-python--cms-25950
#https://stackoverflow.com/questions/3891804/raise-warning-in-python-without-interrupting-program
        
import warnings
def e():
        warnings.warn("this is just a warning", Warning)
e()

def f():
    return 4 / 0
 
def g():
    raise Exception("Don't call us. We'll call you")
 
def h():
    try:
        f()
 
    # note that by default, e has a class defined by the type of error
    # so if you want to manipulate the error name as a string, must first convert as str(e)
    except Exception as e:
        print(type(e))   
        print("error message is " + str(e) + "\n\nThis error has stopped the function.")
 
    try:
        g()
 
    except Exception as e:
        print(e)
        
h()
        
        
###############################################################

        
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

# str.contains
# regular expressions: https://www.w3schools.com/python/python_regex.asp
movies.columns.str.contains(pat = "^Act", case = False, regex = True)

# concatenate strings
"test1 " + "test2 " + "test3 "
list = ["test1", "test2", "test3"]
list

# add to 
list.append("test4")
list

# collapse strings
" ".join(list)


##############################################################


# get dummy variables
movies.dtypes
movies_categorical_vars = movies.select_dtypes(include = ["object"])
movies_categorical_vars.columns

# get dummies
movies_dummies = pd.get_dummies(data = movies_categorical_vars)
movies_dummies

# get numeric variables
movies_numeric_vars = movies.select_dtypes(include = ["number"])
movies_numeric_vars.columns

# bind dummies and numeric
movies2 = pd.concat([movies_numeric_vars, movies_dummies], axis = 1)
movies2.columns
movies2.head()


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


