First project of a SVM machine learning model using python in collaboration with @katyazano

The project was about getting league of legends teams data and trying to make our model guess if they were going to the worlds tournament.

With help of web scraping we got the dataset for training and another for testing.
The data sets got turned into dataframes with help of pandas.
The data got separated in.
  x: feature matrix, which contains the input features. 
  y: target vector, which contains the output labels.
This x and y got standarized for our model.
With help of an imported SVC class we made our model.
Then trained our model with x and y from our training dataframe.
With the model finished, we have it our x testing data.
The output it gave we compared it with y testing data.
Then using Flask we made an very pretty webpage which displays our results on a beautiful beach with a check column to check our model performance.

Issues
The web scrapping part takes a lot of time to process
Not enough data to train and test the model
Not very accurate since the data we got was limited
