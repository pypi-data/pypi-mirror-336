def KNN():
    return [
        """
        # Importing necessary libraries
        import numpy as np
        import pandas as pd
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import train_test_split,GridSearchCV
        from sklearn.utils import resample,shuffle
        import matplotlib.pyplot as plt
        from sklearn.neighbors import KNeighborsClassifier
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
        '''to deal with imbalanced dataset is we will do bootstrapping'''
        bank_zero=df[df['y']==0]
        bank_one=df[df['y']==1]
        df_minority=resample(bank_one,replace=True,n_samples=20000)
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
        X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=42,train_size=0.8)
        """,
        """
        knn_clf=KNeighborsClassifier()
        knn_clf.fit(X_train,y_train)
        """,
        """
        def draw_roc_curve(model,X_test,y_test):
            test_df=pd.DataFrame({'actual':y_test})
            test_df=test_df.reset_index()
            predict_df=pd.DataFrame(model.predict_proba(X_test))
            print(predict_df.head())
            test_df['class1']=predict_df.iloc[:,1:2]
            fpr,tpr,thresholds=roc_curve(test_df['actual'],test_df['class1'],drop_intermediate=False)
            auc_score=roc_auc_score(test_df['actual'],test_df['class1'])
            plt.figure(figsize=(8,6))
            plt.plot(fpr,tpr,label=f"ROC Curve (area= {round(auc_score,2)})")
            plt.plot([0,1],[0,1],'k--')
            plt.xlim([0.0,1.0])
            plt.ylim([0.0,1.05])
            plt.xlabel("FPR")
            plt.ylabel("TPR")
            plt.title("ROC curve")
            plt.legend(loc="lower right")
            plt.show()
            return auc_score,fpr,tpr,thresholds
        auc_score,fpr,tpr,thresholds=draw_roc_curve(knn_clf,X_test,y_test)
        """,
        """
        def draw_cm(actual,predict):
            cm=confusion_matrix(actual,predict)
            sns.heatmap(cm,annot=True,fmt='.2f',xticklabels=['0','1'],yticklabels=['0','1'])
            plt.xlabel('Predicted Label')
            plt.ylabel('actual label')
            plt.show()
        """,
        """
        y_predict=knn_clf.predict(X_test)
        # draw_cm()
        print(confusion_matrix(y_test,y_predict))
        """,
        """
        tuned_parameters=[{'n_neighbors':range(3,10),'metric':['canberra','euclidean','minkowski']}]
        clf=GridSearchCV(KNeighborsClassifier(),tuned_parameters,cv=10,scoring='roc_auc')
        clf.fit(X_train,y_train)
        """,
        """
        clf.best_score_
        """,
        """
        clf.best_params_
        """
    ]
