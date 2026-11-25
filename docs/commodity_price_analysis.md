# Commodity Price Analytics

## 1\. Project Overview

This module analyzes commodity prices across different markets
to help compare the prices of agricultural commodities.

## 2\. Dataset

Dataset file: data/raw/commodity\_prices.csv

The dataset contains 8 sample records.

Commodities:

* Rice
* Wheat
* Corn
* Coffee

Markets:

* Tirupati
* Bengaluru

Currency: INR
Unit: KG
Data date: 12 November 2026

Note: The dataset contains sample data, not verified live market prices.

## 3\. Implementation

The analysis was developed using Python, Pandas and Plotly.

Main tasks:

* Read commodity price data from CSV.
* Check required columns.
* Validate numeric prices and dates.
* Remove invalid and duplicate records.
* Calculate average, minimum and maximum prices.
* Calculate price differences between markets.
* Generate an interactive comparison chart.

## 4\. Analysis Results

|Commodity|Average Price|Price Difference|
|-|-:|-:|
|Coffee|330.00|20.00|
|Corn|29.00|2.00|
|Rice|43.25|1.50|
|Wheat|36.00|2.00|

All prices are in INR per KG.

## 5\. Key Findings

* Coffee has the highest average price.
* Corn has the lowest average price.
* Bengaluru has higher sample prices for all four commodities.
* Coffee has the largest price difference.

## 6\. Generated Outputs

* processed/commodity\_price\_summary.csv
* static/charts/commodity\_price\_comparison.html

## 7\. Testing

Automated tests were created using Python unittest.

Commodity analytics tests: 11

Sensor validation tests: 3

Total tests passed: 14

Test command:

python -m pytest -v



Test result:

14 passed

## 8\. Conclusion

The Commodity Price Analytics module successfully
compares sample commodity prices across two markets.

It generates a summary CSV and an interactive
price comparison chart for further analysis.

