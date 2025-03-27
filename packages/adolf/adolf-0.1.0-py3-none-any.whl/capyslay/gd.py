def GD():
    return [
        """
        # Importing necessary libraries
        import numpy as np
        import pandas as pd
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import train_test_split
        import random
        import matplotlib.pyplot as plt
        """,
        """
        # Reading the data
        df=pd.read_csv('/content/sample_data/Advertising.csv')
        #display the first 5 rows
        df.head()
        """,
        """
        X = df[['TV','radio','newspaper']]
        y = df['sales']
        """,
        """
        # Standardization of values using StandardScaler()
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        y=np.array((y-y.mean())/y.std())
        """,
        """
        # Step -1: Random initialization of weights and bias
        def initialize(no_features):
            np.random.seed(seed=42)
            random.seed(42)
            #bias(value between 0 and 1)
            bias=random.random()
            #weights
            weights=np.random.rand(no_features)
            return bias,weights
        b,w=initialize(3)
        print("Bias: ",b," Weights: ",w)
        """,
        """
        # Step 2: Predict the y values from bias and weights
        def predict_y(b,w,X):
            return b+np.matmul(X,w)
        b,w=initialize(3)
        y_predict=predict_y(b,w,X)
        y_predict[0:10]

        """,
        """
        # Step 3: Calculate Cost Function (MSE)
        def calculate_cost(y,y_predict):
            y_resid=y-y_predict
            return np.sum(np.matmul(y_resid.T,y_resid))/len(y_resid)
        calculate_cost(y,y_predict)
        """,
        """
        # Step 4: Update the bias and weights
        def update(x,y,y_predict,b0,w0,alpha):
            #gradient of bias
            bias=(np.sum(y_predict-y)*2)/len(y)
            weights=(np.matmul((y_predict-y),x)*2)/len(y)
            newBias=b0-alpha*bias
            newWeights=w0-alpha*weights
            return newBias,newWeights
        b,w=update(X,y,y_predict,b,w,0.01)
        print(b,w)
        """,
        """
        def gradient_descent(X,y,alpha=0.01,iterations=100):
            b,w=initialize(X.shape[1]) #Step1
            count=0
            gd_df=pd.DataFrame(columns=['Iteration','Cost'])
            index=0
            for i in range(iterations):
                y_predict=predict_y(b,w,X) #Step2
                cost=calculate_cost(y,y_predict) #Step3
                prev_b=b
                prev_w=w
                b,w=update(X,y,y_predict,prev_b,prev_w,alpha) #Step4
                if count%10==0:
                gd_df.loc[index]=[i,cost]
                index+=1
                count+=1
            print("Final values of b,w are: ",b,w)
            return gd_df
        gd_df=gradient_descent(X,y,alpha=0.001,iterations=200)
        """,
        """
        gd_df.head(10)
        """,
        """
        alphas=[0.0001,0.001,0.01] #Checking for various values of alpha
        for alpha in alphas:
            gd_df=gradient_descent(X,y,alpha,iterations=1000)
            plt.plot(gd_df['Iteration'],gd_df['Cost'],label=f"alpha={alpha}")
            plt.xlabel("number of iterations")
            plt.ylabel("cost or mse")
            plt.legend()
        """
    ]