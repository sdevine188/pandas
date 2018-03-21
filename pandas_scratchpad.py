import numpy as np
import pandas as pd
import pylab as pl
import os


# set working directory
os.chdir("C:/Users/Stephen/Desktop/Python/pandas")
os.getcwd()

# create fake df
df = pd.DataFrame(np.random.randn(8, 3),
                      columns=['A', 'B', 'C'])

# read in data
arrests = pd.read_csv("us_arrests.csv")
arrests

# inspect first few rows
arrests[:5]
arrests.head()
arrests.tail()

# select column
arrests["state"]
arrests["state"][:5]
x = arrests[["state", "Murder"]]
x[:5]

# value_counts()
iris = pd.read_csv("iris.csv")
iris[:5]
iris[1:5]
iris["Species"].values
species_counts = iris["Species"].value_counts()
species_counts
species_counts.plot(kind = "bar")

# various functions
setosa = iris[iris["Species"] == "setosa"]
setosa.describe()
setosa.columns[1]
setosa.mean()
setosa.count()
setosa.min()[:1]
setosa.min()[:1]
len(setosa["Species"])
setosa["Species"].describe()
setosa.describe(include = ["object"])
setosa.describe(include = ["number"])
iris.icol(4)
iris.irow(0)
iris.columns
iris["Species"].unique()
z = "hellosarah"
x = ", ".join(z)
" ".join("hello", "sarah")

petal_length_bins = pd.cut(iris["Petal.Width"], 4)
petal_length_qbins = pd.qcut(iris["Petal.Width"], 4)

# use lambda to create functions on the fly
x = lambda x : x + 1
x(5)

# combine lambda with map to get equivalent to sapply
# map returns an iterator, so you need to list it, and then put in a df
iris.columns
y = iris["Petal.Length"]
z = lambda x : x + 100
x = map(lambda x : x + 100, y)
y.head()
x1 = list(x)
x1 = pd.DataFrame(x1)
x1.head()
x1.shape
type(x)
type(x1)

# define same function traditionally, not using lambda
def plus_100(x):
    return x + 100
plus_100(2)
def plus_200(x):
    z = x + 100    
    return z + 100
plus_200(1)
iris.apply(plus_100)

# create new column
# note the SettingWithCopy warning is just saying the dataframe 
# is already a copy of an existing df
# it is only to job your memory you have another copy of df floating around
setosa["new_col"] = pd.Series(new_col)
new_col = list(map(lambda x : x + 100, setosa["Petal.Length"]))
new_col = pd.DataFrame(new_col)
setosa.columns
setosa.head()
new_col.shape
setosa.shape
setosa["new_col"] = setosa["Petal.Length"]
new_col.head()
setosa["Petal.Length"].head()
setosa.head()
setosa["new_col"] = new_col
setosa.loc[:, "new_col2"] = pd.Series[new_col, index = setosa.index]
setosa["new_col2"] = list(new_col)
setosa.head()
setosa.loc[ :, "new_col"] = new_col

# this works
df = pd.DataFrame(np.random.randn(5,2),columns=list('AB'))
df["new_col"] = df.loc[:, "A"]
df.head()

# pulling specific rows, columns, or arrays
# use .loc if you want to include column names
# use .iloc if you want to use just row/column numbers
setosa.loc[:, "Species"]
iris.loc[ 1:3 , "Species"]
iris.iloc[3:5, :]
iris.iloc[: , 1:3]
iris.iloc[2, 2]
x = ["setosa"]
type(x)
iris[iris["Species"].isin(["virginica", "setosa"])]
iris[iris["Species"].isin(x)]

# groupby and aggregate (split, apply, combine)
x = iris.groupby("Species").aggregate(sum)

# strings
x = iris["Species"].str.contains("s")
x = iris[x]
x.shape

# group-by
iris.groupby("Species").mean()
iris.groupby("Species").mean()

# append new row
new_rows = iris.loc[1:5, :]
iris.shape
iris2 = iris.append(new_rows)
iris2.shape

# stacking and unstacking
iris3 = iris.stack()
iris3.shape
type(iris3)
iris3[0:2]
iris3.unstack().iloc[1:10, :]
iris3.unstack(1).iloc[1:10, :]
iris3.unstack(1).head()
iris3.head()
iris3.unstack(0).head()

# pivot tables
iris2 = 










