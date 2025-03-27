def km():
    return [
        """
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sns
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
        import warnings
        warnings.filterwarnings('ignore')
        """,
        """
        df=pd.read_csv('Income Data.csv')
        df.head()
        """,
        """
        sns.lmplot(x="age" , y="income",fit_reg=False,data=df)
        plt.show()
        """,
        """
        cluster1=KMeans(3)
        cluster1.fit(df)
        """,
        """
        df['clusterid']=cluster1.labels_
        df.head()
        """,
        """
        sns.lmplot(x='age',y='income',data=df,hue='clusterid',fit_reg=False)
        plt.show()
        """,
        """
        scaler=StandardScaler()
        scaled_df=scaler.fit_transform(df[['age','income']])
        scaled_df[0:5]
        """,
        """
        cluster2=KMeans(3,random_state=42)
        cluster2.fit(scaled_df)
        """,
        """
        df['clusterid_new']=cluster2.labels_
        df.head()
        """,
        """
        sns.lmplot(x='age',y='income',data=df,hue='clusterid_new',fit_reg=False)
        plt.show()
        """,
        """
        #finding optimal clusters
        cluster_range=range(1,10)
        errors=[]
        for x in cluster_range:
            clusters=KMeans(x)
            clusters.fit(scaled_df)
            errors.append(clusters.inertia_)
        plt.figure(figsize=(8,6))
        plt.plot(cluster_range,errors,marker='o')
        #giving 3 as minimum
        """,
        """
        --------OPTIONAL-----------
        """,
        """
        def get_silhouette_score(X,labels):
            # Compute silhouette score
            silhouette_avg = silhouette_score(X, labels)
            print(f"Silhouette Score: {silhouette_avg:.4f}")
            return silhouette_avg
        """,
        """
        get_silhouette_score(X,kmeans.labels_)
        """,
        """
        k_value = range(2,11)

        scores = []
        cluster_errors = []
        for k in k_value:
            k_means = KMeans(n_clusters=k)
            k_means.fit(X)
            silhouette_avg = get_silhouette_score(X, k_means.labels_)
            print(f"Silhouette Score: {silhouette_avg:.4f}",k)
            scores.append(silhouette_avg)
            cluster_errors.append(k_means.inertia_)
        import numpy as np
        optimal  = k_value[np.argmax(scores)]
        print(optimal)
        """
    ]
