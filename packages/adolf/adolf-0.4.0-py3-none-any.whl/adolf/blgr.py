def blgr():
    return [
        """
        #import libraries
        import numpy as np
        import pandas as pd
        import statsmodels.api as sm
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import confusion_matrix,roc_curve,roc_auc_score
        import seaborn as sns
        import matplotlib.pyplot as plt
        import warnings
        warnings.filterwarnings('ignore')

        """,
        """
        df=pd.read_csv('German.csv')
        df.head()
        """,
        """
        #selecting the features
        X_features=list(df.columns)
        X_features.remove('credit_risk')
        X_features
        """,
        """
        encoded_df=pd.get_dummies(df[X_features],drop_first=True)
        """,
        """
        X=sm.add_constant(encoded_df)
        y=df['credit_risk']
        """,
        """
        X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=42,train_size=0.7)
        """,
        """
        model=sm.Logit(y_train,X_train).fit()
        """,
        """
        y_predict=model.predict(X_test)
        y_predict=y_predict.map(lambda x: 1 if x>0.5 else 0)
        def builtCM(y_test,y_predict):
            print("Confusion matrix is: ")
            cm=confusion_matrix(y_test,y_predict,[1,0])
            labels=['Bad Credits','Good credits']
            sns.heatmap(cm,annot=True,fmt='.2f',xticklabels=labels,yticklabels=labels)
            plt.xlabel('Predicted label')
            plt.ylabel('Actual label')
            plt.show()
        builtCM(y_test,y_predict)
        """,
        """
        vars_p_vals_df=pd.DataFrame(model.pvalues)
        vars_p_vals_df['vars']=vars_p_vals_df.index
        vars_p_vals_df.columns=['pvals','vars']
        signi_fea=list(vars_p_vals_df[vars_p_vals_df.pvals<=0.05]['vars'])
        signi_fea
        """,
        """
        model2=sm.Logit(y_train,sm.add_constant(X_train[signi_fea])).fit()
        X_test_signi=X_test[signi_fea]

        """,
        """
        y_predict2=model2.predict(sm.add_constant(X_test_signi))
        y_predict2=y_predict2.map(lambda x: 1 if x>0.5 else 0)
        """,
        """
        builtCM(y_test,y_predict2)
        """,
        """    
        def draw_roc(actual,predict):
            fpr,tpr,thresholds=roc_curve(actual,predict,drop_intermediate=False)
            auc_score=roc_auc_score(actual,predict)
            plt.figure(figsize=(8,6))
            plt.plot(fpr,tpr,label=f"ROC curve(area={auc_score})")
            plt.plot([0,1],[0,1],'k--')
            plt.xlim([0.0,1.0])
            plt.ylim([0.0,1.05])
            plt.xlabel('FPR')
            plt.ylabel('TPR')
            plt.legend(loc='lower right')
            plt.show()
        y_predict2=y_predict2.map(lambda x: 1 if x>0.5 else 0)
        draw_roc(y_test,y_predict2)
        """
    ]
