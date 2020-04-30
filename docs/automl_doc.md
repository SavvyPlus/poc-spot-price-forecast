# AWS Resources 
* SageMaker Autopilot https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-automate-model-development.html

* Example notebook https://github.com/awslabs/amazon-sagemaker-examples/blob/master/autopilot/autopilot_customer_churn.ipynb

# Data 

## Format

* The input data must be in CSV format and contain at least 1000 rows
* There must be a target column to predict in the dataset
* Other columns called feature columns 

## Columns
### Target column
 * spot price

### Features columns
* demand
* pv
* season (0, 1, 2, 3, 4)  
* daytype (weekdays, Staturday, Sunday/Public holidays)
* ... inter connector, offerbands ...

# How it works

## Train
* Provide input data in CSV format 
* X = all features columns
* y = target value which is spot price
  
## Predict

Provide X in future -> y in future

## Example
We train 2017 and 2018 data.

Columns in CSV are:

* spotprice
* demand
* daytype
  
The frequency is 5min.

Training data has more than 200,000 rows.

After traning, we want to predict all spot prices every 5min in 2019. We provide 2019 data in CSV format (around 100,000 rows) with columns:

* demand
* daytype

We put that data into predictor then we get list of all spot prices every 5min (~100,000) in 2019.









