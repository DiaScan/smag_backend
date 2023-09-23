import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori


# dataset = [['Milk','Onion', 'Bread', 'Kidney Beans','Eggs','Bread'],
#            ['Fish','Onion','Bread','Kidney Beans','Eggs','Bread'],
#            ['Milk', 'Apples', 'Kidney Beans’, ‘Eggs'],
#            ['Milk', 'Sugar', 'Tea Leaves', 'Kidney Beans', 'Bread'],
#            ['Tea Leaves','Onion','Kidney Beans', 'Ice cream', 'Eggs'],]



def get_frequent_patterns(transactions):
    """Takes input as the plain transaction object"""
    # print(transactions[0])
    dataset = []
    for transaction in transactions:
        item_list = transaction['item_list']
        items = item_list.split(',')
        cleaned_items = [item.strip() for item in items]
        dataset.append(cleaned_items)

    # for row in dataset:
        # print(row)
    # print(dataset)
    # return ''

    transacts = []
    for i in range(len(dataset)):
        transacts.append([dataset[i][j] for j in range(len(dataset[i]))])

    rule = apriori(transactions = transacts, min_support = 0.03, min_confidence = 0.35, min_lift = 3, min_length = 2, max_length = 1000)
    results=list(rule)

    def inspect(results):
        lhs         = [tuple(result[2][0][0])[0] for result in results]
        rhs         = [tuple(result[2][0][1])[0] for result in results]
        support    = [result[1] for result in results]
        confidence = [result[2][0][2] for result in results]
        lift       = [result[2][0][3] for result in results]
        return list(zip(lhs, rhs, support, confidence, lift))


    output_DataFrame = pd.DataFrame(inspect(results), columns = ['Left_Hand_Side', 'Right_Hand_Side', 'Support', 'Confidence', 'Lift'])
    df = output_DataFrame[['Left_Hand_Side', 'Right_Hand_Side', 'Confidence']]

    patterns = []

    def split_rec(items):
        split_items = items.split(',')
        cleaned_items = []

        for item in split_items:
            clean_item = item.strip().replace("‘", "").replace("’", "")
            cleaned_items.append(clean_item)

        return split_items
    for index in df.index:
        patterns.append({'src_items' : [df['Left_Hand_Side'][index]], 'rec_items' : [split_rec(df['Right_Hand_Side'][index])], 'confidence' : df['Confidence'][index]})

    patterns.sort(key = lambda x: x['confidence'], reverse=True)
    limit = min(len(patterns), 10)
    return patterns[:limit]

# get_frequent_patterns()