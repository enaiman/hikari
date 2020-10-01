import csv

print("Starting\n")
ak_list = []
search_value = str('app_key:')

f_in = open('C:\code\shopify.csv', 'r')
with f_in:
    reader = csv.reader(f_in)
    for row in reader:
        for e in row:
            if search_value in e:
                if e not in ak_list:
                  ak_list.append(e)
                # print(e)

print("Input file completed")

f_out = open("C:\code\output.csv", 'w', newline='')
with f_out as outfile:
    writer = csv.writer(f_out)
    for item in ak_list:
        writer.writerow([item])

print("\nDone")
