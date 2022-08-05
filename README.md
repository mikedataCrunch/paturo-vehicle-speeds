# paturo-vehicle-speeds
The repository for codes and notebooks used in the prediction of probe vehicle speeds deployed in Cauayan City, Philippines. Funded by the project PATURO &mdash; a collaboration of the Asian Institute of Management ACCeSs Lab, DOST, and Cauayan LGU.


## Project Members
1. Michael Dorosan - machine learning pipeline, processing of data points, model interpretation, vizualization, writing
2. Damian Dailisan PhD - code optimization, geodata processing expert, vizualization, writing
3. Jesus Felix Valenzuela PhD - scoping of the problem to be solved, data collection and cleaning, writing

## Objectives:
1. Predict the temporal (1-min window) average of vehicle speeds using surrounding land-use profile (200-m), and time variables as inputs
2. Identify rank variables according to SHAP impact on the prediction


## Extended Abstract

The rapid urbanization of cities brings with it a host of challenges, particularly for health, security, mobility, and employment; among these, access to safe, affordable, accessible and sustainable public transportation will be critical in the near-to-medium term. 

To address these challenges, policy-makers have been making use of smart city concepts. Aspiring smart cities in developing countries however, face particular challenges. Smart cities rely on large-scale and real-time data collection and processing to generate actionable insights, which presupposes the prior existence of dedicated infrastructure. While the latter can reasonably be expected in developed countries, the needed infrastructure (such as sensors, telemetry, and stable network connections) is often rudimentary in developing cities, if at all present. The data collected from such cities thus offer unique opportunities not present in older and more mature ones, including observations of the interactions between a developing city’s public transportation system and its land-use profile.

In this work, we examine the interplay between land use and public transportation in a developing city in a developing country (Cauayan City, Philippines) from a machine learning perspective. We obtained land-use data for the city (including building footprints manually-traced from satellite imagery and tagged according to their usage - residential, industrial, commercial or institutional), the city’s road network from OpenStreetMap and GPS tracks obtained from a sample of 200 motorized tricycles serving Cauayan’s public transport system from February to November 2021. From these datasets, we trained a machine learning model to predict the average speeds of vehicles from features that reflect the land use distribution (i.e., areas of the nearby buildings segmented according to usage), road segment properties, time of the day, and the day of week. Of the combined dataset, we set aside 20 percent (the *test set*) for model performance evaluation, and use the remaining (the *training set*) for model training and hyperparameter optimization (average root-mean-square (RMS) error across 10-fold cross-validation). With a trained Gradient Boosting Machine model [1], we obtain a test R2 between predicted and actual average vehicle speeds of 0.76 and an RMS error of 5.74 km/hour, an improvement over a baseline model which uses the historical average speeds on each street for each day of the week with hourly temporal resolution (test R2: 0.74, test RMS error: 5.92 km/hour; see Figure 1, left).


![Alt text](figures/abstract-fig.png?raw=true "abstract-figure")

Figure 1: Prediction performance of a tuned LightGBM nodel (left), feature importance according to SHAP values (center) and distributions of SHAP values (right). Details in the main text.

Finally, we determined the most important predictors using Shapley additive explanations (SHAP) [2], a game theoretic approach to explain the output of any machine learning model. We find that, besides the street properties such as the speed limit, concentrations of nearby commercial and residential buildings are also strong (negative) predictors of vehicle speeds (see Figure 1, center and right). Our approach and results demonstrate the use of interpretable machine learning models for understanding urban transport in developing cities, and have implications for policy-makers seeking to adjust land-use plans to improve urban mobility.


### References
[1] G. Ke, Q. Meng, T. Finley, T. Wang, W. Chen, W. Ma, Q. Ye, T.-Y. Liu, Lightgbm: A highly efficient gradient boosting decision tree, in: Advances in Neural Information Processing Systems, Vol. 30, Curran Associates, Inc., 2017, pp. 3149–3157.
[2] S. M. Lundberg, S.-I. Lee, A unified approach to interpreting model predictions, in: I. Guyon, U. V. Luxburg, S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, R. Garnett (Eds.), Advances in Neural Information Processing Systems 30, Curran Associates, Inc., 2017, pp. 4765–4774.


### Python Tools Used
1. lightgbm - a tree-based package used in regression
2. SHAP - Shapley additive explanations package is a post-hoc machine learning interpretation tool. This was used in surfacing impactful features using SHAP score.
3. matplotlib - basic plotting package for python
4. pandas - for handling tabluar data (e.g., .csv files)
5. networkx and osmnx - for handling road network data. Used in taggign data points with road info (i.e., number of lanes, speed limit)
6. geopandas - for handlang geodata used for tagging data points with land-use data from 




