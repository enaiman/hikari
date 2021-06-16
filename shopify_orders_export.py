import requests
import csv

# Fill the domain and xsa_token values (lines 6 and 7)
# Apply the relevant fields filters under params (lines 9-11)
domain = 'enaiman.myshopify.com'
xsa_token = 'shpat_8xb9393f8f711e8db668c0f54c31c4ae2x'
headers = {"Content-Type": "applic"
                           "ation/json", "X-Shopify-Access-Token": f"{xsa_token}"}
params = {'fields': 'name,order_number,email,processed_at',
          'status': 'any', 'fulfillment_status': 'shipped', 'financial_status': 'any',
          'processed_at_min': '2020-05-01T00:00:00+00:00'}
url = f"https://{domain}/admin/api/2021-01/orders.json"

response = requests.request("GET", url, headers=headers, params=params)

orders = response.json()['orders']
print(orders)

data_file = open('shopify_orders_utz.csv', 'w', newline='')
csv_writer = csv.writer(data_file)

count = 0
for order in orders:
    if count == 0:
        header = order.keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(order.values())

if response.links:
    print(response.links)
    try:
        while (response.links['next'])['url']:
            link = (response.links['next'])['url']
            print(link)
            url = link
            params = {'fields': 'name,order_number,email,processed_at'}
            response = requests.request("GET", url, headers=headers)
            print(response.json())
            orders = response.json()['orders']
            for order in orders:
                csv_writer.writerow(order.values())
    except:
        print("\nJob finished")

data_file.close()
