# Model Strategy Document
This document explains the machine learning model I plan to use in Week 3.

## Selected Model  
**Linear Regression**

## Purpose  
To forecast the next day’s total energy output using recent historical data.

## Input  
The model will use the following input features:
- 7-day rolling average of energy output  
- Previous day's energy value  
- Day of the week (e.g., Monday, Tuesday)

## Output  
The model will generate:
- A single predicted value (in kWh) for the next day's energy output

## Preprocessing Steps  
Before training or using the model, I will:
- Remove or fill missing values in the input features  
- Format the date into a usable weekday label  
- Apply one-hot encoding for day-of-week (categorical variable)  
- Normalize numeric values (if needed)

## Why This Model?  
- It is simple and fast to implement  
- Easy to explain to non-technical users  
- Works well with time-series data when trends are stable  
- A good baseline before trying more advanced models