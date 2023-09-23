from collections import Counter

def get_top_k_most_sold_items(k, transactions):
    dataset = []
    for transaction in transactions:
        item_list = transaction['item_list']
        items = item_list.split(',')
        cleaned_items = [item.strip() for item in items]
        dataset.extend(cleaned_items)

        item_counter = Counter(dataset)
        item_counter_list  = list(item_counter.items())
        item_counter_list.sort(key = lambda x: x[1], reverse=True)
    
    k = min(k, len(dataset))

    res = []
    for i in range(k):
        res.append(item_counter_list[i][0])

    return res


    



    