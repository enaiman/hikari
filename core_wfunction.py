"""
░░░░░░░░░░░░░░░░ATTENTION: THIS PROCESS IS IRREVERSIBLE!░░░░░░░░░░░░░░░░
Required actions:
- Insert the shop_domain (=domain) and shop_token (=xsa_token) - ANCHOR_1
- Insert the metafield keys that you would like to delete from Shopify (offload keys prepopulated) - ANCHOR_2
Script's workflow:
- Get all product IDs from Shopify
- Get all metafields that should be deleted based on the inserted keys
- Delete all the relevant metafields
- Summarize and print the outcome of the process
"""

import requests
import json

# ANCHOR_1: Insert the store credentials in the lines below (must have valid token)
domain = 'enaiman.myshopify.com'
xsa_token = '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'
headers = {"Content-Type": "application/json", "X-Shopify-Access-Token": f"{xsa_token}"}

# ANCHOR_2: Define the keys you would like to remove
filter_keys = ('1000', '1001', '1002', 'bottomline', 'qa_bottomline')


def make_call(verb='GET', url=None, headers=headers, params=None):
    return requests.request(verb, url, headers=headers, params=params)


# Get all product IDs from Shopify
response = make_call(url=f"https://{domain}/admin/api/2020-10/products.json", params={"fields": "id", "limit": "5"})
products = response.json()['products']
product_ids = []
for i in products:
    product_ids.append(i['id'])
if response.links:
    try:
        while (response.links['next'])['url']:
            link = (response.links['next'])['url']
            response = make_call(url=link)
            products = response.json()['products']
            for i in products:
                product_ids.append(i['id'])
    except:
        print("\nProducts pulling job finished.")
else:
    print("\nAll products were pulled in one run.")
print(f"A total of {len(product_ids)} products was pulled.\n")

# Get metafields IDs and delete the metafields
delete_counter, errors_counter = 0, 0
products_with_errors = []
for product_id in product_ids:
    response = make_call(url=f"https://{domain}/admin/api/2021-01/products/{product_id}/metafields.json", params={"fields": "id, namespace, key"})
    metafields = response.json()['metafields']
    ids_to_delete = []
    for item in metafields:
        for obj, value in item.items():
            if obj == 'key':
                if value in filter_keys:
                    ids_to_delete.append(item['id'])
    if len(ids_to_delete) > 0:
        for id in ids_to_delete:
            print(f"\nDeleting metafield {id} for product {product_id}.")
            response = make_call(verb='DELETE', url=f"https://{domain}/admin/api/2021-01/products/{product_id}/metafields/{id}.json")
            print(f"Metafield {id} deleted with response: {response.status_code}.\n")
            if response.status_code == 200:
                delete_counter += 1
            else:
                errors_counter += 1
                products_with_errors.append(product_id)
    else:
        print(f"No relevant metafields were found in product {product_id}.")
print("=" * 59)
print(f"\nProcess finished with {delete_counter} successful deletions and {errors_counter} errors.")
if errors_counter > 0:
    print(f"\nEncountered errors on product(s): {products_with_errors}.")

"""
    _   __                            __                 __                      _            
   / | / /__ _   _____  _____   _____/ /_____  ____     / /__  ____ __________  (_)___  ____ _
  /  |/ / _ \ | / / _ \/ ___/  / ___/ __/ __ \/ __ \   / / _ \/ __ `/ ___/ __ \/ / __ \/ __ `/
 / /|  /  __/ |/ /  __/ /     (__  ) /_/ /_/ / /_/ /  / /  __/ /_/ / /  / / / / / / / / /_/ / 
/_/ |_/\___/|___/\___/_/     /____/\__/\____/ .___/  /_/\___/\__,_/_/  /_/ /_/_/_/ /_/\__, (_)
                                           /_/                                       /____/   
"""
