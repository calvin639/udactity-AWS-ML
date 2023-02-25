# Report: Predict Bike Sharing Demand with AutoGluon Solution
#### Calvin Wright

## Initial Training
### What did you realize when you tried to submit your predictions? What changes were needed to the output of the predictor to submit your results?
Initially there was no issue with my predictions but for the second model the predictions had some values which were negative. 
Since negative values don't make sense in terms of predicted bike rentals we needed to set them to 0

### What was the top ranked model that performed?
My top ranked model was my second model, after training with an additional feature, setting the training time down to 200 seconds. 
The model that performed the best was: LightGBMXT_BAG_L2
This is some form of Gradient Boosting Macine 

## Exploratory data analysis and feature creation
### What did the exploratory analysis find and how did you add additional features?
Initial when I first ran the project I never converted the datetime column to the correct type so I went back and did that when reading the CSV
Then I had to convert the cathegorical features where being represented as ints which was seen when I plotted the histogram. 
The additional feature I thought would be useful is a more accurate "tempeture". One that took into account humidity and wind speed. Initially I thought humidity would increase tempeture and therefore make for more bike rentals, but at the very end I saw that they were negatively correlated so my new features calculation might need some work. 
Another new feature I thought might be useful would be something that takes into account working days vs holidays. So it it is not the weekend and a holiday then it is likely a bank holiday. Then see if this increases or decreases bike rentals. My thought is that it would increaes casual riders but decrease people using it for work. 

### How much better did your model preform after adding additional features and why do you think that is?
My model defitinetly got better after adding a new feature with a higher public score on Kaggle.   

## Hyper parameter tuning
### How much better did your model preform after trying different hyper parameters?
After playing around with the hyperparameters it got worse than teh previous model so the defaults were likely better choices, but I also decrease the training time which would have had an adverse effect too.

### If you were given more time with this dataset, where do you think you would spend more time?
As mentioned above I would try and create some new feature that depends on a mix of weather conditions. I searched for how Google's "Feels like" tempeture is calculated but couldn't find anything definitive. 
I would have plotted the correlation matrix of Count vs the features at the begining so I had a better understanding of which features I should spend more time with. I could have dropped unimportant features using Principal Component Analysis (PCA)

### Create a table with the models you ran, the hyperparameters modified, and the kaggle score.
|model|time|# of Models|Bag Folds|score|
|--|--|--|--|--|
|initial|600|15|8|1.80995|
|add_features|300|9|8|1.94865 |
|hpo|120|10|8|1.84672|

### Create a line plot showing the top model score for the three (or more) training runs during the project.


![model_test_score.png](img/model_train_score_final.png.png)

### Create a line plot showing the top kaggle score for the three (or more) prediction submissions during the project.


![model_test_score.png](img/model_test_score_final.png.png)

## Summary
- The final submission had a worse score than the tuned original New Feature model
- From the corelation matrix I calculated at teh end shows the original temp column has the greatest influnce on bike rides
- I should have used the correlation matrix earlier to help decide on new columns but just thought about it at the end so will do that in future
- Given more time I would test out more hyperparams or even use the Sagemaker Auto ML to see what insights it could get
