def MLGR():
    return [
        """
        # Importing necessary libraries
        import numpy as np
        import pandas as pd
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import train_test_split
        from sklearn.utils import resample,shuffle
        import matplotlib.pyplot as plt
        from sklearn.linear_model import LogisticRegression
        import seaborn as sns
        from sklearn.metrics import roc_curve,roc_auc_score,accuracy_score,confusion_matrix
        """,
        """        
        # Reading the data
        df=pd.read_csv('bank.csv')
        # Display the first 5 rows
        df.head()
        """,
        """
        df['y'].value_counts()
        """,
        """
        # To deal with imbalanced dataset is we will do bootstrapping
        bank_zero=df[df['y']==0]
        bank_one=df[df['y']==1]
        df_minority=resample(bank_one,replace=True,n_samples=15000)
        new_df=pd.concat([bank_zero,df_minority])
        """,
        """
        # To deal with imbalanced dataset is we will do bootstrapping
        bank_zero=df[df['y']==0]
        bank_one=df[df['y']==1]
        df_minority=resample(bank_one,replace=True,n_samples=15000)
        new_df=pd.concat([bank_zero,df_minority])
        """,
        """
        #To shuffle the dataset
        new_df=shuffle(new_df)
        new_df.head()
        """,
        """
        X_features=list(new_df.columns)
        X_features.remove('y')
        X_features
        """,
        """
        X=new_df.drop('y',axis=1)
        y=new_df['y']
        """,
        """
        df=pd.get_dummies(new_df[X_features])
        X=df
        X.head()
        """,
        """
        X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=42,train_size=0.7)
        """,
        """
        model=LogisticRegression()
        model.fit(X_train,y_train)
        """,
        """
        y_predict=model.predict(X_test)
        """,
        """
        def draw_cm(actual,predict):
            cm=confusion_matrix(actual,predict)
            sns.heatmap(cm,annot=True,fmt='.2f',xticklabels=['0','1'],yticklabels=['0','1'])
            plt.xlabel('Predicted Label')
            plt.ylabel('actual label')
            plt.show()
        draw_cm(y_test,y_predict)
        """,
        """
        def draw_roc(actual,predict):
            fpr,tpr,thresholds=roc_curve(actual,predict,drop_intermediate=False)
            auc_score=roc_auc_score(actual,predict)
            plt.figure(figsize=(8,6))
            plt.plot(fpr,tpr,label=f"ROC curve(area={round(auc_score,4)})")
            plt.plot([0,1],[0,1],'k--')
            plt.xlim([0.0,1.0])
            plt.ylim([0.0,1.05])
            plt.xlabel('FPR')
            plt.ylabel('TPR')
            plt.legend(loc='lower right')
            plt.show()
        y_predict_prob=pd.DataFrame(model.predict_proba(X_test))
        y_predict_prob.head()
        test=pd.DataFrame({'actual':y_test})
        test=test.reset_index()
        test['cat1']=y_predict_prob.iloc[:,1:2]
        draw_roc(test['actual'],test['cat1'])
        """
    ]
