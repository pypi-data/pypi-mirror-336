def mlr():
    return [
        """
        import pandas as pd
        import numpy as np
        import statsmodels.api as sm
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import r2_score, mean_squared_error
        from statsmodels.stats.outliers_influence import variance_inflation_factor

        # Load the dataset
        df = pd.read_csv('ipl.csv')
        df.head()

        """,
        """
        # Selecting only relevant features to build our model
        X_features = [ 'AGE', 'COUNTRY', 'PLAYING ROLE', 'T-RUNS', 'T-WKTS',
        'ODI-RUNS-S', 'ODI-SR-B', 'ODI-WKTS', 'ODI-SR-BL',
        'CAPTAINCY EXP', 'RUNS-S', 'HS', 'AVE', 'SR-B',
        'SIXERS', 'RUNS-C', 'WKTS', 'AVE-BL', 'ECON', 'SR-BL']
        categorical_features = ['AGE', 'COUNTRY', 'PLAYING ROLE', 'CAPTAINCY EXP']
        
        # Using get_dummies() to convert categorical features into numeric features
        encoded_df = pd.get_dummies(df[X_features], columns = categorical_features, drop_first = True)
        """,
        """
        X_features = encoded_df.columns

        # Add constant to build the model
        X = sm.add_constant(encoded_df)
        y = df['SOLD PRICE']
        
        # Splitting of training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.8, random_state = 42)
        
        # Building the model
        model1 = sm.OLS(y_train, X_train).fit()
        """,
        """
        y_pred = model1.predict(X_test)
        
        # Performing Metric Evaluation
        print("R-squared =",np.abs(round(r2_score(y_test, y_pred), 2)))
        print("RMSE =",round(np.sqrt(mean_squared_error(y_test, y_pred)), 2))
        """,
        """        
        # Finding about the existence of multi-collinearity
        # If VIF > 4, then there exists multi-collinearity
        from statsmodels.stats.outliers_influence import variance_inflation_factor
        
        def get_vif_factors(X):
            vif = [variance_inflation_factor (X.values, i) for i in range(X.shape[1])]
            vif_factors = pd.DataFrame()
            vif_factors['column'] = X.columns
            vif_factors['VIF'] = vif
            return vif_factors
        vif_factors = get_vif_factors(encoded_df)
        vif_factors

        """,
        """
        columns_to_be_removed = ['T-RUNS', 'T-WKTS', 'RUNS-S', 'HS', 'AVE', 'RUNS-C', 'SR-B', 'AVE-BL', 'ECON', 'ODI-SR-B', 'ODI-RUNS-S', 'AGE_2', 'SR-BL']
        X_new_features = list(set(X_features) - set(columns_to_be_removed))
        get_vif_factors(X[X_new_features])
        """,
        """
        # Building a new model after removing multi-collinearity
        X_train = X_train[X_new_features]
        model2 = sm.OLS(y_train, X_train).fit()
        y_pred = model2.predict(X_test[X_new_features])

        # Performing Metric Evaluation after removing multi-collinearity
        print("R-squared =",np.abs(round(r2_score(y_test, y_pred), 2)))
        print("RMSE =",round(np.sqrt(mean_squared_error(y_test, y_pred)), 2))
        """
    ]