# CIS 9650- Media Industry
Team: Antonio Reybol Jr, Apurva Sharma, Klejsierta Xhumari, Laura Pacas, Samantha Wang, and Zi jian Zheng

## Movie Industry
Have you ever wonder what what it takes for movies to perfrom well?\
Where and in how many langauges your favorite movie has been released on?\
This program will help you to dive deep into the movie industry!\
Our goal is to analyze what factors influence the revenue of a movie. 
Our goal is to improve/enhance the revenue basis of the movie industry based on our analysis of the ratings and to create better metrics for data analysis to sell focused content.

## Datasets:
### Dataset 1: Metadata
This dataset contains information on over 45,000 movies including budget, overview, and more. \
Link: https://www.kaggle.com/ibtesama/getting-started-with-a-movie-recommendation-system/data?select=movies_metadata.csv  
### Dataset 2: IMDb Movies
This dataset contains information on over 85,000 movies including production company, actors, directors, genre, and more. \
Link: https://www.kaggle.com/stefanoleone992/imdb-extensive-dataset?select=IMDb+movies.csv

All our datasets can be accessed in this repository in the "movie_industry_datasets.rar" file.

## Program: 
The program leverages both the aforementioned datasets and is filtered to include only movies released between the years 2000 and 2020. Users will be informed of the following:

 - Top 10 movies based on revenue 
 - Top 10 movies based on user rating 
 - Total count of movies by year (bar chart)
 - Total count of movies by genre (pie chart)
 - Top 5 directors based on movies' revenue 
 - Top 5 directors based on movies' popularity (popularity defined by viewers' reviews)
 - Top 5 directors based on movies' budget 
 - Actors that appeared in the top 5 profitable movies 
 - Actors that appeared in the top 5 popular movies 
 - Movie recommendations based on users selected language and movies' popularity rating
 - Least popular movies based on users selected language and movies' popularity rating 
 - List of popular actors based on the popularity rating 

The program also seeks engagement from the user to input, for example: 
 - Input: "Enter movie title of interest"
 - Output: inputted movie's description 
 
 - Input: "Learn more about movies in specific language" (user inputs a specific language: i.e., "English")
 - Output: list of movies in selected language and preliminary information 

## Multilinear Regression Model 
There is also a multilinear regression model analyzing which variables have the strongest correlation. Here is the list of the variables analyzed: 
- revenue 
- budget
- year
- genre
- production company

Based on the R squared, the strongest correlation among these variables were (in order of strongest correlation): 
1. Revenue ~ Budget 
2. Genre ~ Budget 
3. Budget ~ Duration 

From all movies released between the years 2000 and 2020, we predicted the movies' revenue and calculated an R square of about 83% between actual revenue and predicted revenue. Therefore, our model has a strong significance in predicting the revenue of a movie. 
