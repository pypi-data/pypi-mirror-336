def AR():
    return [
        """
        txns = []
        with open('/content/groceries.csv') as f:
            temp = [x.strip() for x in f.readlines()]
            for i in temp:
                txns.append(i.split(','))
        """,
        """
        # Importing necessary libraries
        import pandas as pd
        import numpy as np
        from mlxtend.preprocessing import TransactionEncoder
        from mlxtend.frequent_patterns import apriori, association_rules
        """,
        """
        # Initialize OnehotTransactions
        encoder = TransactionEncoder()
        # Transforming our transactions into one-hot-encoding format
        hot_txns = encoder.fit_transform(txns)
        # Converting the matrix into a DataFrame
        df = pd.DataFrame(hot_txns, columns=encoder.columns_)
        """,
        """
        df.head()
        """,
        """
        items = apriori(df, min_support = 0.02, use_colnames = True)
        # Displaying 10 random samples
        items.sample(10, random_state=90)
        """,
        """
        rules = association_rules(items, metric='lift', min_threshold=1)
        # Displaying 5 random samples
        rules.sample(5)
        """,
        """
        # Displaying top 10 Association rules
        rules.sort_values('confidence', ascending = False)[0:10]
        """
    ]
