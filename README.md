# InvestCraft: Intelligent Money Management  

## Team Members
- Harshil Bhatt
- Prince Kakkad

## Objective
InvestCraft aims to build a machine learning model that predicts investor risk tolerance. The model is trained on a dataset containing investor profiles, including demographic, financial, and behavioral attributes. By predicting risk tolerance on a scale from 1 to 10, InvestCraft facilitates tailored investment strategy recommendations.

## Data Source
The project utilizes data from the "Survey of Consumer Finances" conducted by the Federal Reserve Board. This dataset provides comprehensive information about individuals' financial situations, including income, net worth, age, education, and risk tolerance.

## Predicted Variable
InvestCraft predicts risk tolerance based on the ratio of risky assets to total assets, normalized with the average S&P500 values of 2007 and 2009. Investors with minimal changes in risk tolerance between 2007 and 2009 are identified as intelligent investors.

## Features
To filter features, intuitive variables are selected based on the Data Dictionary provided by the Federal Reserve Board. Key features include:
- Age
- Education
- Experience
- Marital Status
- Occupation
- Number of Kids
- Net Worth Category
- Income Category
- Willingness to Take Risk

## Methodology
1. **Data Preprocessing**: Clean and preprocess data, filtering intuitive features from 2007.
2. **Risk Tolerance Calculation**: Calculate risk tolerance based on the ratio of risky assets to total assets.
3. **Normalization**: Normalize risk tolerance using the average S&P500 values of 2007 and 2009.
4. **Model Training**: Train machine learning models to predict risk tolerance.
5. **Evaluation and Interpretation**: Evaluate model performance and interpret feature importance to gain insights into investor behavior.

## Conclusion
InvestCraft demonstrates the potential of machine learning in objectively analyzing investor behavior. By identifying key variables influencing risk tolerance, the model provides valuable insights for personalized investment strategies.

## References
- Federal Reserve Board: [Survey of Consumer Finances](https://www.federalreserve.gov/econres/scf_2009p.htm).
- Data Dictionaries: [2007](https://www.federalreserve.gov/econres/files/codebk2007.txt), [2009](https://www.federalreserve.gov/econres/files/codebk2009p.txt).
