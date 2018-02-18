import csv
import json
import sys

from ruamel.yaml import YAML

unusable = [
    # 1, 2,  # empty
    41,  # spam
    0, 3, 4, 10,  # test
    30,  # empty
    18, 19, 24, 26, 27,  # no project title
    5, 6,  # missing fields
    20, 43, 44, 47, 74, 75, 78, 188, 198, 204,  # not sure
    215, 217, 220, 230, 233, 260,  # not sure
    38, 61, 62,  # rejected/needs editing
]

last_processed = 260

yaml = YAML()
yaml.width = 4096


def print_list(data):
    for i, row in enumerate(reversed(data)):
        print('%d - %s - %s' %
              (i, row['nama'] or
                  row['auth_name'] or
                  row['email'],
               row['proyek']))


def show_missing_list(data):
    for i, row in enumerate(reversed(data)):
        if i in unusable:
            print('%d - %s - %s - %s' %
                  (i, row['created_at'],
                   row['nama'] or row['auth_name'] or row['email'],
                   row['proyek']))
            if not row['nama'] and not row['proyek'] and not row['auth_name']:
                print('   %r' % row)


def get_filename(nomor):
    return '_hibahcme/%0.3d.md' % nomor


def load_yaml_file(nomor):
    filename = get_filename(nomor)
    with open(filename, 'r') as f:
        docs = list(yaml.load_all(f))
        return docs[0]


def create_yaml_file(row, nomor, add_private=False):
    row = row.copy()
    if 'foto' in row and row['foto']:
        row['foto'] = json.loads(row['foto'])
    if 'file' in row and row['file']:
        row['file'] = json.loads(row['file'])

    if not add_private:
        del row['ip']
        del row['telp']
        del row['ktp']
        del row['user_agent']
        del row['email']
        del row['auth_name']
        del row['created_at']

    filename = get_filename(nomor)

    try:
        data = load_yaml_file(nomor)
    except Exception as e:
        print('File for %d missing: %s' % (nomor, e))
        data = {'nomor': nomor}

    for key, value in dict(row).items():
        if key not in data or data[key] != value:
            data[key] = value

    with open(filename, 'w') as f:
        f.write('---\n')
        yaml.dump(data, f)
        f.write('---\n')


def output_yaml_files(data, last=last_processed, add_private=True):
    for i, row in enumerate(reversed(data)):
        if i in unusable:
            continue
        if i > last:
            break
        print('Processing %d' % i)
        if i < 7:
            create_yaml_file(row, i, add_private=add_private)
        else:
            create_yaml_file(row, i + 9, add_private=add_private)


def load_csv(filename):
    with open(filename) as f:
        reader = csv.DictReader(f)
        return list(reader)


def main(argv=None):
    filename = argv[1] if len(argv) == 2 else '../netlify-data.csv'
    data = list(load_csv(filename))
    output_yaml_files(data, add_private=True)


if __name__ == '__main__':
    main(sys.argv)
