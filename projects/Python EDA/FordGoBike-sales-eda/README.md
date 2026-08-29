# Ford GoBike Data Exploration

## Dataset

This data set includes information about individual rides made in a bike-sharing  system covering the greater San Francisco Bay area for the month of February 2019. 
The dataset can be found in the following link provided by Udacity 
[here](https://docs.google.com/document/d/e/2PACX-1vQmkX4iOT6Rcrin42vslquX2_wQCjIa_hbwD0xmxrERPSOJYDtpNc_3wwK_p9_KpOsfA6QVyEHdxxq7/pub),


## Summary of Findings

In the exploration, I found that 
- Male users encompassed 75% of all users, female users 23%.
- The bike share service is also quite popular with the users as it has 91% of them as subscribers.
- Most users of the service are between 30 and 40 years old with the youngest being 21 years and the oldest being 95 years after cleaning the data. 
- The day with the most rides is Thursday followed closely by Tuesday, Wednesday and Friday. The days with the lowest rides are Sunday and Saturday. 
- Most users prefer to start their rides at 0800h and 1700h followed by 1800h and 0900h.
- To measure the distance coverd by the users, I created a column for distance in kilometers, based on the longitude and latitude start and end points.It was clear from the distance covered by the users that most of them could only manage an average of 1.5km. The longest distance covered was 63km.
- Most rides last an average of 11 minutes and most people don't go beyond 13 minutes.The longest ride is 1409 minutes which is about 23 hours

I went on to look at how subscribers use the service compared to the customers. The analysis indicates that 
- Customers use the service mostly on Thursday, Friday, Sunday, Monday and Tuesday. Subscribers however use the service mostly on weekdays and occasionally on the weekends, that is, Saturday and Sunday.
- Subscribers mostly start their rides at 1700h and 0800h which could indicate they use it to go to work in the morning and back home in the evening while customers mostly start their rides at 1700h
- Interestingly enough though was discovering that customers covered more distance than the subscribers which in my opinion confirms that subscribers use it for commuting to work because the usage decreases significantly on weekends while customers use it for work and other activities perhaps.
- The mean for customers is 1.67 km, and the mean for subscribers is 1.46 km.

An analysis of the relationship between age of the users and the distance covered shows that the longest and shortest rides fluctuate between the older users who are above 70 years of age.

- Most female customers start their rides at 1700h followed by 0800h and 1300h and 1600h
- Most male customers start their rides at 1700h followed by 1600h and 0800h.
- Most customers who identify as other start their rides at 1700h and 0800h
- Most female subscribers start their rides at 0800h followed by 1700h and 0900h and 1800h
- Most male subscribers start their rides at 1700h followed by 0800h and 0900h.
- Most subscribers who identify as other start their rides at 1700h followed by 1800h and 0800h
- Most users from both categories aged 34 years preferred to ride on Thursdays at 1700h.

Male customers prefer to ride on Thursdays and Fridays while female customers prefer to ride on Thursday and Sunday. Customers who identify as other prefer to ride on Thursdays and Fridays while subscribers of the same category prefer to ride on Wednesdays and Thursdays.


## Key Insights for Presentation

For the presentation, I focus on the usage of the service by users according to their gender, user category and age. I start by plotting a pie chart showing the gender distribution of the users followed by introducing a new column called start_hour that extracts the hour of the day when the users use the service. This is an important insight because it could help the service providers know what time of day to do repairs or maintenance for their bikes with affecting their users negatively.

![image](https://github.com/Irene-arch/FordGoBike-Dataset-Udacity/assets/56026296/23385df9-d47d-4f62-a74c-87ae716205d7)

Afterwards, I looked at how each category of users uses the service per day and plotted it on a bar chart which showed clearly the most popular days. I went ahead and broke it down further into the most popular hour of the day and what age of users were associated with it. I used a heatmap for this and the darker shades on the heatmap provided the required insights.

![image](https://github.com/Irene-arch/FordGoBike-Dataset-Udacity/assets/56026296/1e89fada-4362-438c-a925-6d2004494457)

You can view more insights by downloading and opening [this file](https://github.com/Irene-arch/FordGoBike-Dataset-Udacity/blob/main/Part%201%20-%20FordGo%20Bike%20System%20Data.html) in your browser.

