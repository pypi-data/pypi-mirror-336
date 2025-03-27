def NB():
    return [
        """
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sn
        from sklearn.feature_extraction.text import CountVectorizer
        import warnings
        warnings.filterwarnings('ignore')
        """,
        """
        train_ds = pd.read_csv("sentiment_train", delimiter="\t")
        train_ds.head(5)
        """,
        """
        pd.set_option('max_colwidth', 800)
        """,
        """
        # To check for imbalance
        train_ds.sentiment.value_counts()
        """,
        """
        # Create count plot
        ax = sn.countplot(x='sentiment', data=train_ds)
        plt.show()
        """,
        """
        # Initialize the CountVectorizer
        count_vectorizer = CountVectorizer()

        # Create the dictionary from the corpus
        feature_vector = count_vectorizer.fit(train_ds.text)
        train_ds_features = count_vectorizer.transform(train_ds.text)

        # Get the feature names
        features = feature_vector.get_feature_names_out()
        print("Total number of features: ", len(features))
        """,
        """
        # Converting the matrix to a dataframe
        train_ds_df = pd.DataFrame(train_ds_features.todense())
        
        # Setting the column names to the features i.e. words
        train_ds_df.columns = features
        """,
        """
        # Removing low-frequency words
        features_counts = np.sum(train_ds_features.toarray(), axis = 0)
        feature_counts_df = pd.DataFrame( dict(features = features,
        counts = features_counts))
        len(feature_counts_df[feature_counts_df.counts == 1])
        """,
        """
        count_vectorizer = CountVectorizer(max_features=1000)
        
        # Create the dictionary from the corpus
        feature_vector = count_vectorizer.fit(train_ds.text)
        
        # Get the feature names
        features = feature_vector.get_feature_names_out()
        
        # Transform the document into vectors
        train_ds_features = count_vectorizer.transform(train_ds.text)
        
        # Count the frequency of the features
        features_counts = np.sum(train_ds_features.toarray(), axis = 0)
        feature_counts = pd.DataFrame(dict( features = features,
        counts = features_counts))
        """,
        """
        feature_counts.sort_values( 'counts', ascending = False)[0:15]
        """,
        """
        from sklearn.feature_extraction import text
        my_stop_words = text.ENGLISH_STOP_WORDS
        
        # Adding custom words to the list of stop words
        my_stop_words = text.ENGLISH_STOP_WORDS.union(['harry', 'potter',
        'code', 'vinci', 'da','harry', 'mountain', 'movie', 'movies'])
        """,
        """
        # Setting stop words list
        count_vectorizer = CountVectorizer(stop_words = 'english',
        max_features = 1000)
        feature_vector = count_vectorizer.fit(train_ds.text)
        train_ds_features = count_vectorizer.transform(train_ds.text)
        features = feature_vector.get_feature_names_out()
        features_counts = np.sum(train_ds_features.toarray(), axis = 0)
        feature_counts = pd.DataFrame(dict( features = features,
        counts = features_counts))
        """,
        """
        feature_counts.sort_values("counts", ascending = False)[0:15]
        """,
        """
        # Words like loved and love; suck and sucked are derived from same root word. They are to be removed.
        from nltk.stem.snowball import PorterStemmer
        stemmer = PorterStemmer()
        analyzer = CountVectorizer().build_analyzer()
        
        #Custom function for stemming and stop word removal
        def stemmed_words(doc):
            ### Stemming of words
            stemmed_words = [stemmer.stem(w) for w in analyzer(doc)]
            ### Remove the words in stop words list
            non_stop_words = [ word for word in stemmed_words if word not in my_stop_words]
            return non_stop_words
        """,
        """
        count_vectorizer = CountVectorizer(analyzer=stemmed_words,
        max_features = 1000)
        feature_vector = count_vectorizer.fit(train_ds.text)
        train_ds_features = count_vectorizer.transform(train_ds.text)
        features = feature_vector.get_feature_names_out()
        features_counts = np.sum(train_ds_features.toarray(), axis = 0)
        feature_counts = pd.DataFrame(dict( features = features,
        counts = features_counts))
        feature_counts.sort_values("counts", ascending = False)[0:15]
        """,
        """
        # Convert the document vector matrix into dataframe
        train_ds_df = pd.DataFrame(train_ds_features.todense())
        
        # Assign the features names to the column
        train_ds_df.columns = features
        
        # Assign the sentiment labels to the train_ds
        train_ds_df['sentiment'] = train_ds.sentiment
        """,
        """
        from sklearn.model_selection import train_test_split
        """,
        """
        train_X, test_X, train_y, test_y = train_test_split(train_ds_features,
        train_ds.sentiment,
        test_size = 0.3,
        random_state = 42)
        """,
        """
        from sklearn.naive_bayes import BernoulliNB
        nb_clf = BernoulliNB()
        nb_clf.fit(train_X.toarray(), train_y)
        """,
        """
        test_ds_predicted = nb_clf.predict(test_X.toarray())
        """,
        """
        from sklearn import metrics
        print(metrics.classification_report(test_y, test_ds_predicted))
        """,
        """
        from sklearn import metrics
        cm = metrics.confusion_matrix(test_y, test_ds_predicted)
        sn.heatmap(cm, annot=True, fmt='.2f')
        """
    ]

print(NB())