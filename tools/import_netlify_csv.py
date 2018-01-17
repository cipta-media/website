import csv
import json
import sys

import yaml

test = [0, 3, 4]

unusable = [
    30,  # empty
    18, 19, 24, 26, 27,  # no project title
]

dups = [
]

imported = {
    5: 14,  # 14 - sanchia tryphosa hamidjaja - Seragam Merah Jambu ...
    6: 15,
    7: 16,
    8: 17,
    9: 18,
    10: 19,
    11: 20,
    12: 21,
    13: 22,
    14: 23,
    15: 24,
    16: 25,
    17: 26,  # 26 - HJ.I.G.A.AJU NITYA DHARMANI,SST,SE,MM - LUDRUK ZAMAN NOW

    31: 40,  # 40 - Krisha Vi Anindita - NIMAMO ...
    32: 41,
    33: 42,
    34: 43,
    35: 44,
    36: 45,
    37: 46,
    38: 47,
    39: 48,
    40: 49,
    41: 50,
    42: 51,  # 51 - Anies Marsudiati Purbadiri, S.H., M.H. - Eksistensi ...

    48: 57,  # 57 - Reny santika - Lagenda batu sindu
}

missing = {
    1: 1,
    2: 2,

    20: 20 + 9,
    21: 21 + 9,
    22: 22 + 9,
    23: 23 + 9,

    25: 25 + 9,

    28: 28 + 9,
    29: 29 + 9,

    43: 43 + 9,
    44: 44 + 9,
    45: 45 + 9,
    46: 46 + 9,
}

max_problem_row = max(imported.keys()) - 1


def print_list(data):
    for i, row in enumerate(reversed(data)):
        print('%d - %s - %s' %
              (i, row['nama'] or
                  row['auth_name'] or
                  row['email'],
               row['proyek']))


def show_missing_list(data):
    for i, row in enumerate(reversed(data)):
        if i == max_problem_row:
            break

        if i not in imported and i not in test and i not in unusable:
            assert i in missing
            print('%d - %s - %s - %s' %
                  (i, row['created_at'],
                   row['nama'] or row['auth_name'] or row['email'],
                   row['proyek']))
            if not row['nama'] and not row['proyek'] and not row['auth_name']:
                print('   %r' % row)


def create_yaml_file(row, nomor):
    row = row.copy()
    row['layout'] = 'hibahcme'
    row['foto'] = json.loads(row['foto'])
    if 'file' in row and row['file']:
        row['file'] = json.loads(row['file'])

    del row['ip']
    del row['telp']
    del row['ktp']
    del row['user_agent']
    del row['email']
    del row['auth_name']
    del row['created_at']
    s = yaml.dump(dict(row), default_flow_style=False)
    filename = '_hibahcme/%0.3d.md' % nomor
    with open(filename, 'w') as f:
        f.write('---\n')
        f.write('nomor: %d\n' % nomor)
        f.write(s)
        f.write('---\n')


def print_missing_list(data):
    for i, row in enumerate(reversed(data)):
        if i == max_problem_row:
            break

        if i in missing:
            print('%d - %s - %s - %s - %s - %s' %
                  (missing[i], row['created_at'], row['nama'],
                   row['ktp'], row['email'], row['proyek']))

            create_yaml_file(row, missing[i])


def fetch_data(reader):
    rows = []
    for row in reader:
        rows.append(row)

    return rows


def load_csv(filename):
    with open(filename) as f:
        reader = csv.DictReader(f)
        return list(reader)


def main(argv=None):
    filename = argv[1] if len(argv) == 2 else 'netlify-data.csv'
    data = list(load_csv(filename))
    headers = list(data[0].keys())
    print(headers)
    print_missing_list(data)


if __name__ == '__main__':
    main(sys.argv)
