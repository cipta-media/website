import collections
import csv
import os
import sys

from ruamel.yaml import YAML

yaml = YAML()
yaml.width = 4096


province_names = {
    '11': 'ACEH',
    '12': 'SUMATERA UTARA',
    '13': 'SUMATERA BARAT',
    '14': 'RIAU',
    '15': 'JAMBI',
    '16': 'SUMATERA SELATAN',
    '17': 'BENGKULU',
    '18': 'LAMPUNG',
    '19': 'KEPULAUAN BANGKA BELITUNG',
    '21': 'KEPULAUAN RIAU',
    '31': 'DKI JAKARTA',
    '32': 'JAWA BARAT',
    '33': 'JAWA TENGAH',
    '34': 'DI YOGYAKARTA',
    '35': 'JAWA TIMUR',
    '36': 'BANTEN',
    '51': 'BALI',
    '52': 'NUSA TENGGARA BARAT',
    '53': 'NUSA TENGGARA TIMUR',
    '61': 'KALIMANTAN BARAT',
    '62': 'KALIMANTAN TENGAH',
    '63': 'KALIMANTAN SELATAN',
    '64': 'KALIMANTAN TIMUR',
    '65': 'KALIMANTAN UTARA',
    '71': 'SULAWESI UTARA',
    '72': 'SULAWESI TENGAH',
    '73': 'SULAWESI SELATAN',
    '74': 'SULAWESI TENGGARA',
    '75': 'GORONTALO',
    '76': 'SULAWESI BARAT',
    '81': 'MALUKU',
    '82': 'MALUKU UTARA',
    '91': 'PAPUA',
    '92': 'PAPUA BARAT',
}

current_regency_code = {
    '6405': '6503',  # Nunukan https://www.wikidata.org/wiki/Q14481
}

def load_yaml_file(filename):
    with open(filename, 'r') as f:
        docs = list(yaml.load_all(f))
        return docs[0]


def load_yaml_dir(dirname):
    dataset = {}
    for filename in os.listdir(dirname):
        path = os.path.join(dirname, filename)
        if os.path.isdir(path):
            continue

        nomor = os.path.basename(filename).split('.')[0]
        nomor = int(nomor)

        data = load_yaml_file(path)
        dataset[nomor] = data

    return dataset


def get_niks(dataset, regencies):
    niks = {}
    for nomor, value in dataset.items():
        if 'ktp' not in value:
            print('%d: ktp missing' % nomor)
            continue

        nik = value['ktp']
        regency = nik[0:4]
        if regency in current_regency_code:
            print('nik %s is being moved ...' % nik)
            nik = current_regency_code[regency] + nik[4:]
            print('... to %s' % nik)
            assert len(nik) == 16

        value['nik_location'] = nik[0:6]
        province = nik[0:2]
        value['nik_province'] = province
        if province not in province_names:
            print('%s: unknown province' % nik)
            continue

        province_name = province_names[province]
        value['nik_province_name'] = province_name

        regency_code = nik[0:4]
        if regency_code not in regencies:
            print('%s: unknown regency' % nik)
            continue

        value['nik_regency'] = regency_code
        regency_data = regencies[regency_code]
        value['nik_regency_name'] = regency_data['itemLabel']
        qid = regency_data['item'][31:]
        value['nik_regency_qid'] = qid
        value['nik_coord'] = regency_data['coord']

        niks[nomor] = nik

    return niks


def get_nik_provinces(niks):
    provinces = {}
    for nomor, nik in niks.items():
        province = nik[0:2]
        provinces[nomor] = province

    return provinces


def get_nik_regencies(niks):
    data = {}
    for nomor, nik in niks.items():
        data[nomor] = nik[0:4]

    return data


def count_values(data):
    counts = collections.Counter()
    counts.update(data.values())
    return counts


def print_counter_stats(counts, names):
    """Determine how frequently a code will identify a unique applicant."""
    unique = 0
    not_unique = 0
    for code, count in counts.most_common():
        name = names[code]
        print('%s %s: %d' % (code, name, count))
        if count == 1:
            unique += 1
        else:
            not_unique += count

    print('Unique: %d' % unique)
    print('Not-Unique: %d' % not_unique)


def load_csv(filename, fieldnames=None):
    with open(filename) as f:
        reader = csv.DictReader(f, fieldnames=fieldnames)
        return list(reader)


def get_wdq_regencies():
    # This file is export of http://tinyurl.com/y9nacntd
    filename = os.path.join('..', 'wdq-regencies.csv')

    data = {}
    for row in load_csv(filename):
        data[row['rawcode']] = row

    return data

def emit_map_markers(nik_regencies, regencies):
    used_regencies = {}
    for code, count in nik_regencies.most_common():
        regency_data = regencies[code]
        regency_data['count'] = count
        used_regencies[code] = regency_data

    print('var addressPoints = [')
    for code, regency_data in sorted(used_regencies.items()):
        coord_str = regency_data['coord']
        coord_str = coord_str.replace('Point(', '')[:-1]
        coord_str = coord_str.replace(' ', ',')
        a, b = coord_str.split(',')
        count = regency_data['count']
        name = regency_data['itemLabel']
        print('[%s, %s, "%d %s", "%s"],' % (b, a, count, name, code))

    print('];')

def main(argv=None):
    dataset = load_yaml_dir('_hibahcme')
    regencies = get_wdq_regencies()

    niks = get_niks(dataset, regencies)
    provinces = get_nik_provinces(niks)
    counts = count_values(provinces)

    print_counter_stats(counts, province_names)
    # add_provinces(dataset, provinces)
    # print_location_info(dataset)

    nik_regencies = get_nik_regencies(niks)
    counts = count_values(nik_regencies)

    regency_names = dict()
    for code, data in regencies.items():
        regency_names[code] = data['itemLabel']

    print_counter_stats(counts, regency_names)
    emit_map_markers(counts, regencies)


if __name__ == '__main__':
    main(sys.argv)
