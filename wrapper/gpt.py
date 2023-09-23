import openai
import os 


def improve_top_product_sales(product_name):
    openai.api_key = os.environ.get('OPEN_AI_KEY')
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-16k',
        messages=[
            {
                "role": "system",
                "content": "You are an intelligent marketing agent with vast experience running small small to medium scale supermarkets and stores, help answer the following question based on your marketing knowledge while also taking into account the economic feasibility by focussing more on in store appliable solutions and not online marketing and expensive options",
                "role": "user",
                "content": f"{product_name} is a top selling product in a store, how to further improve it's sales? Provide a suggestion in under 50 words"
            }
        ]
    )

    return completion.choices[0]["message"]["content"]

def improve_low_product_sales(product_name):
    openai.api_key = os.environ.get('OPEN_AI_KEY')
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-16k',
        messages=[
            {
                "role": "system",
                "content": "You are an intelligent marketing agent with vast experience running small small to medium scale supermarkets and stores, help answer the following question based on your marketing knowledge while also taking into account the economic feasibility by focussing more on in store appliable solutions and not online marketing and expensive options",
                "role": "user",
                "content": f"{product_name} is a very low selling product in the store, how to improve it's sales? Provide a suggestion in under 50 words"
            }
        ]
    )

    return completion.choices[0]["message"]["content"]


def start_new_store_at_location(top_products, location):
    openai.api_key = os.environ.get('OPEN_AI_KEY')
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-16k',
        messages=[
            {
                "role": "system",
                "content": "You are an intelligent marketing agent with vast experience running small small to medium scale supermarkets and stores, help answer the following question based on your marketing knowledge while also taking into account the economic feasibility by focussing more on in store appliable solutions and not online marketing and expensive options",
                "role": "user",
                "content": f"Provide suggestion on how to start a store at location {location} where the top selling products are {top_products}"
            }
        ]
    )

    return completion.choices[0]["message"]["content"]

