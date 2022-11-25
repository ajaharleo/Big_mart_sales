# Big mart sales prediction

## Table of Content

  * [Demo](#demo)
  * [Overview](#overview)
  * [Motivation](#motivation)
  * [Technical Aspect](#technical-aspect)
  * [Technologies Used](#technologies-used)
  * [Credits](#credits)

## Demo
Deployment link: [https://big-mart-sales1.herokuapp.com/](https://big-mart-sales1.herokuapp.com/)


<img src="images\projectUI.png" alt="Project UI/UX" />



## Overview
This is an End to End machine learning Regression project with CI/CD pipeline which takes information related to product in the store as input and predict the sales of that product.
The [dataset](https://www.kaggle.com/datasets/brijbhushannanda1979/bigmart-sales-data) used for model training is from kaggle, contains 8523 entries of data of various items , 11 independent features and 1 feature sales as output feature. 


## Motivation
Shoping malls and Big Marts keep track of individual item sales data in order to forcast future client demand and adjust inventory management.During fastive seasons it is difficult to manage inventory manually but by using Machine Learning we can give information regarding Item as input to model and it will predict the sales of that item which ultimatly help to inventory management and increase in the sales.

## Technical Aspect
Step by step overview of complete project implementation.
1. Data Ingestion
    - [Downloaded](https://www.kaggle.com/datasets/brijbhushannanda1979/bigmart-sales-data) dataset from kaggle website. 
2. Exploratory data analysis
    - Analyzed data using visual & Statistical techniques 
    - Univarient Analysis observations 
        - Items with low fat are bought more 
            <img src="images\fat_content.png" alt="FAT_CONTENT" />
        - Fruits and vegetables largely sold and snacks also have good sales 
            <img src="images\fruits&veg.png" alt="fruits" />
        - Medium size stores have much more sales than others.
            <img src="images\outlet_size.png" alt="outlet_sizw" />
        - more number of stores/malls located in tier 3 cities 
            <img src="images\stores_in_tier3.png" alt="tier3" />
        - most of the stores are more of Supermarket type 1
            <img src="images\more_supermarket1.png" alt="supermarket" />
    - Bivarient Analysis obseravations 
        - sales are high for both low and regular fat items
            <img src="images\high_sales_for_low_n_reg_fat.png" alt="fat_sales" /> 

3. Feature Engineering 
    - Data Cleaning 
        - KNN imputer is used to handle missing values 
        - Lable Encoding is used to convert categorical values into numerical values 
        - Outliers checking done by BoxPlot Method
    - Feature Scaling 
        - Standard Scaling operations are applied to scale the data 
4. Feature Selection 
    - Correlation method is used to check internal correlated features.
    - Used RandomForest Feature Importance to select important features  
5. Model Building
    - Trained data using various Machine Learning algorithams.
    - Model Hyperparameter tuning done with GridSearchCV.
    - Models Evaluated with R2 Score and RMSE score.
6. Pipeline 
    Sequence of data preprocessing components is called data pipeline. 
    1. Data Ingestion 
        - Download the data from source, extract it, split into train and test dataset and store in the destination
    2. Data Validation 
        - Validate data so noise data will not come in the piepline 
    3. Data Transformation 
        - Apply Feature Engineering , Feature Selction processes on data and store transformed data into required format/scale. 
    4. Model Trainer 
        - Training the Best model with tuned parameters.
    5. Model Evaluation 
        - Evaluation done by comparing model's accuracy with base accuracy and recent model. 
    6. Model Pusher 
        - If accuracy of trained model is higher than previous deployed model then push model into working.


## Technologies Used
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png" alt="Python" width="200"/>
<img src="https://static.tildacdn.com/tild3536-6337-4235-a664-373965303839/evidently_ai_logo_fi.png" alt="evidently" width="350"/>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Scikit_learn_logo_small.svg/1200px-Scikit_learn_logo_small.svg.png" alt="sklearn" width="350"/>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Pandas_logo.svg/2560px-Pandas_logo.svg.png" alt="pandas" width="350"/>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/NumPy_logo_2020.svg/2560px-NumPy_logo_2020.svg.png" alt="Numpy" width="350"/>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Heroku_logo.svg/2560px-Heroku_logo.svg.png" alt="Heroku" width="350"/>
<img src="https://www.docker.com/wp-content/uploads/2022/03/vertical-logo-monochromatic.png" alt="docker" width="350"/>
<img src="https://www.parasoft.com/wp-content/uploads/2021/04/CICD_CICD.png" alt="CICD" width="350"/>

=======
# Item_sales_predictions
Full Stack End to End Machine Learning Project with CI/CD Piepline
Working Link : https://big-mart-sales1.herokuapp.com/ 