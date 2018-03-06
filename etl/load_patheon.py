
PANTHEON_FILE = '../data/pantheon.csv'
OUTPUT_PANTHEON = '../data/output_pantheon.csv'
import csv
import wikipedia
import json


counter = 3
curr = 0

to_write = {}
with open(PANTHEON_FILE, 'r') as inputfile:
    reader = csv.DictReader(inputfile)
    for row in reader:
        try:
            wp = wikipedia.page(pageid=row['article_id'])
            data = {
                'full_name': row['full_name'],
                'plain_txt': wp.content,
                'html': wp.html(),
                'industry': row['industry'],
                'domain': row['domain'],
                'birth_year': row['birth_year'],
                'popularity_score': row['historical_popularity_index']}
            to_write[row.get('article_id')] = data
        except Exception as e:
            print ('Error ', e.__str__())
            continue

with open(OUTPUT_PANTHEON, 'w') as outputfile:
    json.dump(to_write, outputfile)

