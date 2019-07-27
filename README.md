# Predicting The Costs Of Used Cars Hackathon By Imarticus
This repo contains the solution for ML hackathon (Predicting The Costs Of Used Cars ) by Imarticus. The solution ranks at no. 64 on the leaderboard with a score of 0.935173

![img](https://imgur.com/mtCJsgu.png)

## Problem Statement
Driverless cars are getting closer to reality and at a faster pace than ever. But it is still a bit far fetched dream to have one in your garage. For the time being, there are still a lot of combustion and hybrid cars that roar around the road, for some it chills. Though the overall data on sales of automobiles shows a huge drop in sales in the last couple of years, cars are still a big attraction for many. Cars are more than just a utility for many. They are often the pride and status of the family. We all have different tastes when it comes to owning a car or at least when thinking of owning one.

Well here of course as the name suggests we are not concentrating on a new car, rather our interest is in knowing the prices of used cars across the country whether it is a royal l luxury sedan or a cheap budget utility vehicle. In this hackathon, you will be predicting the costs of used cars given the data collected from various sources and distributed across various locations in India. 

## Approach

It's a standard regression problem of predicting the prices of old car. The imputation of null values was rather tricky. The null values were not visible as 'Nan'. They were kind of hidden in way that it was difficult to find using normal pandas utility. The null values were visible only through graphical means. For ex. value of 0 bhp for 'Power' column etc.

Also some columns that were categorical had high cardinality so encoding them was difficult. The use of *target encoding (with smoothing to prevent overfitting)* gave a boost in the score.

I tried many models : tree based models , regularized linear regression model and artificial neural network. Well tuned Lightgbm performed the best for me.

## Scripts
- data_clean.py : contains the initial data cleaning parts (imputing the null values).
- cars_utils.py : contains utility functions used within the scripts.
- old_car_price_prediction.ipynb : contains the exploratory data analysis ,  further cleaning (to make it suitable for modelling) and modelling part.
- submissions: contains the csv files that were submitted to the competition.
