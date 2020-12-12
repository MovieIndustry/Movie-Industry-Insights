import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import matplotlib.pyplot as plt
import seaborn as sns

##### Metadata (dfm) #####
dfm = pd.read_csv('movies_metadata.csv')

## Use dfm if you need to choose specific columns for questions
dfm= dfm[["adult", "id","overview","imdb_id","budget", "popularity", "release_date", "revenue", "runtime", "original_language", "title", "vote_average", "vote_count"]]
dfm.sort_values("title", inplace = True)
dfm.drop_duplicates(subset =["title","imdb_id"], keep = "last", inplace = True)
#print(dfm)
## Filters out all NAs for dfm
dfm_perf = dfm.dropna() # drop null values

##### IMDb (imdb) #####
imdb_movie = pd.read_csv('IMDb movies.csv')

## Use imdb_movie if you need to choose specific columns for questions
imdb_movie = imdb_movie[["title", "year", "genre", "duration", "country", "language", "director", "production_company", "actors", "budget", "reviews_from_users", "reviews_from_critics","imdb_title_id"]] 
imdb_movie = imdb_movie.rename(columns={'imdb_title_id': 'imdb_id'})
imdb_movie["year"].replace({"TV Movie 2019":"2019"}, inplace=True)
imdb_movie["year"]=imdb_movie["year"].astype(int)
imdb_movie = imdb_movie[imdb_movie.year >= 2000]
## Filters out all NAs for imdb_movie
imdb_movie_perf = imdb_movie.dropna()


## Merged imdb_movie and dfm
all_df = pd.merge(imdb_movie, dfm, on='imdb_id')
all_df=all_df.set_index("imdb_id")
all_df = all_df[all_df.year >= 2000]

# Create movie_revenue is merge IMBD with Meta data csv to find revenue among match
print("\nStep 1: Top 10 movies based on revenue:")
g = dfm.groupby("title", as_index = False).sum()
g = g.sort_values(by=['revenue'], ascending=False)
g = g.head(10)
g = g[["title", "revenue"]]
g["revenue"] = g["revenue"].div(1000000).round(2)
g = g.rename(columns={'revenue': 'revenue(millions)'})
print(g.to_string(index=False))


print("\nStep 2: Top 10 movies based on user rating:")
movieRating = dfm.groupby("title").sum()
movieRating = movieRating.sort_values(by=['vote_average'], ascending=False)
movieRating = movieRating.head(10)
movieRating = movieRating["vote_average"]
print(movieRating)


print("\nStep 3: # of movies by year...")
movieYear=imdb_movie.groupby('year')['title'].count()
movieYear=movieYear.tail(21)
movieYear.plot.bar()
plt.title("Number of movies by year")
plt.ylabel("# of movies")

print("\nStep 4:")
print("Histogram")  
all_df.hist(figsize=(10,10))


print("\nStep 5: Genre")
all_df['genre'].str.contains(', ')
all_df['genre'].unique()
all_df_split_genre_kx = all_df.copy()
split_genre_kx = all_df_split_genre_kx['genre'].str.split(', ').apply(pd.Series, 1).stack().reset_index(level=1, drop=True)
split_genre_kx.name = 'genre_split'
all_df_split_genre_kx = all_df_split_genre_kx.drop(['genre'], axis=1).join(split_genre_kx)
all_df_split_genre_kx.sort_values("title_x", inplace = True)
all_df_split_genre_kx.drop_duplicates(subset =["title_x","year"], keep = "first", inplace = True)
all_df_split_genre_kx['genre_split'].unique()
all_df_split_genre_kx.head()


#Same as the pie
all_df_split_genre_kx['genre_split'].value_counts().plot(kind='bar', color='g')
plt.title('Movies by Genre, 2000-2020', size=18)
plt.xlabel('Genre', size=12)
plt.ylabel('Movie count', size=12)
plt.show()

#pie
all_df_split_genre_kx['genre_split'].value_counts().plot(kind='pie', figsize=(8,8))
plt.title("Movies by Genre 2000-2020", bbox={'facecolor':'0.8', 'pad':5})
plt.show()


print("\nStep 6: Top 5 director base on revenue of the movie:")
ekz = all_df[["title_x","director","revenue"]]
vkz= ekz.nlargest(5, "revenue") 
print(vkz)

print("\nStep 7: Top 5 director base on popularity of the movie:")
#Which directors are popular based on top 5 popularity movies
lekz = all_df[["director","title_x","popularity"]]
hkz = lekz.dropna()
rekz = hkz.astype({"popularity":float})
vlkz= rekz.nlargest(5, "popularity")
print(vlkz)

print("\nStep 8: Top 5 director base on budget of the movie:")
leekz = all_df[["director","title_x","budget_y"]]
hkzz = leekz.dropna()
rekzz = hkzz.astype({"budget_y":float})
vkzz= rekzz.nlargest(5, "budget_y")
print(vkzz)

print("\nStep 9: Which actors appeared in the top 5 most profitable movies:")
eqkz = all_df[["actors","title_x","revenue"]]
vqkz= eqkz.nlargest(5, "revenue") 
#e.sort_values("revenue", ascending = False, inplace = True) 
#c = e.head(5)
print(vqkz)

print("\nStep 10: Which actors apepared in the top most popular movies:")
leekz = all_df[["actors","title_x","popularity"]]
hekz = leekz.dropna()
reekz = hekz.astype({"popularity":float})
vekz= reekz.nlargest(5, "popularity")
print(vekz)

#Have user to input the name of the movie and get an overview of the movie
print("\nStep 11")
print("Enter Title of Movie for an overview")
titleLP=input("Title of Movie:")
enteredmovieLP=all_df[(all_df["title_x"]==titleLP)]
overviewLP=enteredmovieLP["overview"]
print(overviewLP.values)

#User will enter language to get a list movies in the language chosen, country of released and genre
print("\nStep 12")
print("Enter desire Language to know what movies fall into the desired range for your options")
LanguageLP=input("Language:")
enteredLANGLP=all_df[(all_df["language"]==LanguageLP)]
langMOVIESLP=enteredLANGLP[['title_x','genre','country','popularity']]
print(langMOVIESLP)
langMOVIESLP2=langMOVIESLP['title_x'] #just to count how many movies were produced in one langauge
print("There was a total of", langMOVIESLP2.count(), "movies produced in",LanguageLP, "language" )


#Recommending what movie user should watch based on number of reviews by critics 
print("\nStep 13")
print("========================")
print("if you want to watch a movie based on popularity and in", LanguageLP, " then we suggest the following:")
print("\n")
maxiUserLP=langMOVIESLP.astype({"popularity":float})
maxresultLP= maxiUserLP.nlargest(5, "popularity")
print("most popular movies to watch are:","\n",maxresultLP)

print("\nStep 14")
miniUserLP=langMOVIESLP.astype({"popularity":float})
minresultLP= maxiUserLP.nsmallest(5, "popularity")
print("least popular movies in", LanguageLP, "are:","\n",minresultLP)

print("\nStep 15: Most popular actors") ## based on top 500 most popular movies
actor_SW = all_df[["title_x", "actors", "genre", "popularity"]]
actor_SW["popularity"] = actor_SW["popularity"].astype("float")
actor_SW = actor_SW.sort_values(by = ["popularity"], ascending = False)
actor_SW = actor_SW.head(500)

# print(actorSW["actors"])
allActor_SW = (actor_SW.set_index(['title_x', 'genre', 'popularity'])
           .apply(lambda x: x.str.split(', ').explode())
           .reset_index())

topActor_SW = allActor_SW.groupby(["actors"]).agg({"title_x": "count",
                                                   "popularity": "mean"})
topActor_SW = topActor_SW.sort_values(by = ["title_x", "popularity"], ascending = False)
topActor_SW = topActor_SW.head(10)

print(topActor_SW)


import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

##### Metadata (dfm) #####
dfm = pd.read_csv('movies_metadata.csv')


## Use dfm if you need to choose specific columns for questions
dfm= dfm[["imdb_id", "release_date", "revenue"]]

dfm.drop_duplicates(subset =["imdb_id"], keep = "last", inplace = True)
#print(dfm)

## Filters out all NAs for dfm
dfm_perf = dfm.dropna() # drop null values

##### IMDb (imdb) #####
imdb_movie = pd.read_csv('IMDb movies.csv')

## Use imdb_movie if you need to choose specific columns for questions
imdb_movie = imdb_movie[["title","year", "genre", "duration", "country", "production_company", "budget", "imdb_title_id"]] 
imdb_movie = imdb_movie.rename(columns={'imdb_title_id': 'imdb_id'})
imdb_movie["year"].replace({"TV Movie 2019":"2019"}, inplace=True)
imdb_movie["year"]=imdb_movie["year"].astype(int)
## Filters out all NAs for imdb_movie
imdb_movie_perf = imdb_movie.dropna()

## Filters out all NAs for imdb_movie
imdb_movie_perf = imdb_movie.dropna()

## Merged imdb_movie and dfm - Data Cleaning
all_df = pd.merge(imdb_movie, dfm, on='imdb_id')
all_df=all_df.set_index("imdb_id")
all_df = all_df.dropna()
all_df = all_df[all_df.country == "USA"]
all_df['budget'] = all_df['budget'].str.replace(',', '')
all_df['budget'] = all_df['budget'].str.replace('$', '')
all_df['budget'] = all_df['budget'].str.replace('GBP', '')
all_df['budget'] = all_df['budget'].str.replace('CAD', '')
all_df['budget'] = all_df['budget'].str.replace('ESP', '')
all_df['budget'] = all_df['budget'].str.replace('EUR', '')
all_df['budget'] = all_df['budget'].astype(float)
all_df = all_df[all_df.revenue != 0]
all_df = all_df[all_df.year >= 2000]
all_df.to_csv("Combined.csv")

print("\nStep 16")
all_df["genre"] = all_df["genre"].astype('category')
all_df["production_company"] = all_df["production_company"].astype('category')
all_df["genre_cat"] = all_df["genre"].cat.codes
all_df["production_company_cat"] = all_df["production_company"].cat.codes
genre_data = all_df[['genre','genre_cat']].sort_values('genre_cat').reset_index(drop=True)# refer which code represents what
production_data = all_df[['production_company','production_company_cat']].sort_values('production_company_cat').reset_index(drop=True)
genre_data = genre_data.drop_duplicates()
production_data = production_data.drop_duplicates()
genre_data.to_csv("Genre_Code.csv")
production_data.to_csv("Production_Code.csv")


corrMatrix =all_df.corr()
sn.set(rc={'figure.figsize':(11.7,8.27)})
sn.heatmap(corrMatrix, annot=True)
plt.show()

train_df = all_df.iloc[:1450,:] 
test_df= all_df.iloc[1451:,:]
titles = test_df["title"]
train_x = train_df.drop(["year","title","release_date","revenue","country", 'genre','production_company'], axis = 1)
test_df = test_df.drop(["year","title","release_date", "country",'genre','production_company'], axis = 1)
test_actual = test_df
test_df = test_df.drop(["revenue"], axis = 1)
train_y = train_df["revenue"]
lm = LinearRegression()
lm.fit(train_x,train_y)
test_df['Predicted_Revenue'] = lm.predict(test_df)

compare_pred = pd.merge(test_df, test_actual, on='imdb_id')
compare_pred= pd.merge(compare_pred,titles, on='imdb_id')

plt.plot(compare_pred.title, compare_pred.revenue, label = "Actual Revenue")
plt.plot(compare_pred.title,compare_pred.Predicted_Revenue , label = "Predicted Revenue")
plt.xticks(rotation=90, fontsize="x-small")
plt.legend()
plt.show()

print("R2 Score: ", r2_score(compare_pred.revenue, compare_pred.Predicted_Revenue))

#User input

"""
my_list = genre_data.columns.values.tolist()
corrMatrix =genre_data.corr()
sn.heatmap(corrMatrix, annot=True)
plt.show()
#print(genre_data.head())

print(genre_data.corr(method='pearson', min_periods=1))
correlation_matrix = all_df.corr()
print(correlation_matrix)
Genre = input('Enter Desired Genre')
Production_company = input('Enter Desired Production_company')
Duration = float(input("Duration"))
Budget  = float(input("Budget"))

pred_df = pd.DataFrame(columns = ["duration","budget"])

"""





















