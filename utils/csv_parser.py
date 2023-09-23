import csv
import codecs


def parse_file(file):
    csv_reader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    data = []

    for row in csv_reader:
        data.append({'item_list': row['item_list'], 'date': row['date']})
    file.file.close()
    return data