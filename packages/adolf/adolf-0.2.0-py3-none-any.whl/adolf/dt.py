def DT():
    return [
        """
        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.tree import DecisionTreeClassifier, export_graphviz
        import pydotplus as pdot
        from IPython.display import Image
        """,
        """
        df = pd.read_csv('german.csv')
        """,
        """
        y = df['credit_risk']
        X = pd.get_dummies(df.drop(['credit_risk'], axis = 1), drop_first = True)
        """,
        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
        """,
        """
        clf_tree = DecisionTreeClassifier(criterion = 'gini', max_depth = 3).fit(X_train, y_train)
        """,
        """
        # Export the tree into odt file
        export_graphviz(clf_tree, out_file = "chd_tree.odt", feature_names = X.columns, filled = True)
        """,
        """
        # Read the create the image file
        chd_tree_graph = pdot.graphviz.graph_from_dot_file('chd_tree.odt')
        chd_tree_graph.write_jpg('chd_tree.png')
        """,
        """
        # Render the png file
        Image(filename = 'chd_tree.png')
        """,
        """
        from sklearn.model_selection import GridSearchCV
        tuned_parameters=[{'criterion':['gini','entropy'],'max_depth':range(2,10)}]
        clf_tree=DecisionTreeClassifier()
        clf=GridSearchCV(clf_tree,tuned_parameters,cv=10,scoring='roc_auc').fit(X_train,y_train)
        print(clf.best_score_)
        print(clf.best_params_)
        """
    ]

DT()