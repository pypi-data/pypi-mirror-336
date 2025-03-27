def slr():
    return [
        """
        import numpy as np
        import pandas as pd
        import statsmodels.api as sm
        from sklearn.model_selection import train_test_split
        mba_salary_df = pd.read_csv('/content/sample_data/MBA Salary.csv')
        """,
        """
        # Add constant 1 to the dataset
        X = sm.add_constant(mba_salary_df['Percentge in Grade 10'])
        y = mba_salary_df['Salary']

        # Split dataset into train and test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.8, random_state = 100)
        
        # Fit the regression model
        model = sm.OLS(y_train, X_train).fit()
        print(f"Our SLR Model is: Y = {round(model.params[0],2)} + {round(model.params[1],2)} X")
        print(f"i.e., For every 1 unit increase in Percentage in Grade 10, Salary is increased by {round(model.params[1],2)} times")
        """,
        """        
        # Calculation R2_score and RMSE
        from sklearn.metrics import r2_score, mean_squared_error
        y_pred = model.predict(X_test)
        print("R-squared =",np.abs(round(r2_score(y_test, y_pred), 2)))
        print("RMSE =",round(np.sqrt(mean_squared_error(y_test, y_pred)), 2))
        """,
        """
        # Residual Analysis
        import scipy.stats as se
        import matplotlib.pyplot as plt
        model_residuals = model.resid
        se.probplot(model_residuals, plot = plt)
        plt.show()
        """,
        """
        # Standaridizing the values
        def standard(vals):
            return (vals - vals.mean())/vals.std()
        plt.scatter(standard(model.fittedvalues), standard(model.resid))
        plt.title("Residual Plot: MBA Salary Prediction")
        plt.xlabel("Standardized predicted values")
        plt.ylabel("Standardized Residuals")
        plt.show()

        """,
        """
        # Outliers Removal using Z-Score
        from scipy.stats import zscore
        mba_salary_df['z_score_salary'] = zscore(mba_salary_df.Salary)
        mba_salary_df[ (mba_salary_df.z_score_salary > 3.0) | (mba_salary_df.z_score_salary < -3.0)]

        """,
        """
        # Outliers Removal using IQR
        def remove_outliers_iqr(data):
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return (data >= lower_bound) & (data <= upper_bound)
        mba_salary_df = mba_salary_df[remove_outliers_iqr(mba_salary_df['Salary'])]
        """,
        """
        # Add constant 1 to the dataset
        X = sm.add_constant(mba_salary_df['Percentge in Grade 10'])
        y = mba_salary_df['Salary']
        
        # Split dataset into train and test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.8, random_state = 100)
        
        # Fit the regression model
        model = sm.OLS(y_train, X_train).fit()
        y_pred = model.predict(X_test)
        
        print("R-squared for new model =",np.abs(round(r2_score(y_test, y_pred), 2)))
        print("RMSE for new model =",round(np.sqrt(mean_squared_error(y_test, y_pred)), 2))
        """
    ]