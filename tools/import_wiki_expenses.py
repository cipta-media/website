import os
import sys

import requests
import yaml
from slugify import slugify

WIKI_URL = 'https://wiki.ciptamedia.org/wiki/'

INDONESIAN_MONTH_NAMES = {
    'Januari': 0,
    'Februari': 1,  # Pebruari?
    'Maret': 2,
    'April': 3,
    'Mei': 4,
    'Juni': 5,
    'Juli': 6,
    'Agustus': 7,
    'September': 8,
    'Oktober': 9,
    'November': 10,
    'Desember': 11,
}

def load_yaml_file(filename):
    with open(filename) as f:
        return yaml.load(f)

def load_structure(grantee):
    filename = os.path.join('_data', grantee.lower() + '.yml')
    data = load_yaml_file(filename)
    return data

# doesnt work due to permissions
def load_live_wikitext(pagename):
    r = requests.get(WIKI_URL + pagename + '?action=raw')
    r.raise_for_status()
    return r.text


def load_saved_wikitext(source_dir, code):
    filename = os.path.join(source_dir, code)
    with open(filename) as f:
        wikitext = f.read()
        return wikitext


def strip_wiki_filelink(wikitext):
    if wikitext.lower().replace(' ', '') in ('[[:|nota]]', '[[:|:lunas]]', '[[:|lunas]]', 'lunas'):
        return ''

    filename = wikitext.replace('[[:Berkas:', '').replace(']', '')
    if '|' in filename:
        filename = filename.split('|', 1)[0].strip()
    else:
        filename = filename.strip()

    if len(filename) < 10:
        raise ValueError('Strange filename for %s' % wikitext)

    return 'https://wiki.ciptamedia.org/wiki/File:%s' % filename


def parse_date_string(wikitext):
    if not wikitext:
        return ''

    # Rapotivi A1
    if wikitext == '720,000':
        return '2014-08-08'

    parts = wikitext.split(' ')
    if len(parts) != 3:
        raise ValueError('Unknown date %r' % parts)

    if parts[1].title() in INDONESIAN_MONTH_NAMES:
        month_id = INDONESIAN_MONTH_NAMES[parts[1].title()]
    else:
        raise ValueError('Unknown date %r' % parts)

    if len(parts[2]) != 4:
        if len(parts[2].strip('-')) == 4:
            parts[2] = parts[2].strip('-')
        else:
            raise ValueError('Unknown date %r' % parts)

    year = int(parts[2])
    if year not in [2011, 2012, 2013, 2014, 2015, 2016, 2017]:
        if year == 2916:
            print('Fixing year 2916->2016')
            year = 2016
        elif year == 3017:
            print('Fixing year 3017->2017')
            year = 2017
        else:
            raise ValueError('Unknown date %r' % parts)

    day_id = int(parts[0])
    return '%s-%02d-%02d' % (
        parts[2],
        month_id + 1,
        day_id,
    )


def parse_wikitext(wikitext, grantee):
    records = []
    lines = wikitext.splitlines()
    record = {}
    for line in lines:
        if not line or line[0:2] in ['==', '{|', '|}', '! ']:
            continue
        if line.startswith('[[Kategori:'):
            continue

        if line == '|-':
            if record:
                if 'nama' not in record:
                    raise ValueError('no name in %r' % record)
                records.append(record)

            record = {}
        elif '-->' in line:
            prefix, value = line.rsplit('-->', 1)
            value = value.strip()
            value = value.replace('  ', ' ')
            if not value or value == '-':
                continue

            if '<!--Tanggal transaksi' in prefix:
                value = parse_date_string(value)
                if value:
                    record['tanggal'] = value
            elif '-Nama-->' in prefix and value:
                value = value.strip()
                if value.startswith('-'):
                    value = value[1:].strip()

                parts = value.split(' - ', 1)
                if not len(parts) == 2 or '-' in parts[0]:
                    parts = value.split('- ', 1)
                    if not len(parts) == 2 or '-' in parts[0]:
                        if value.startswith('Ndaru PP _ '):
                            parts = ['Ndaru PP', value[11:]]
                        elif value.startswith('Desta A -'):
                            parts = ['Desta A', value[9:]]
                        elif value.startswith('Billy PN -'):
                            parts = ['Billy PN', value[10:]]
                        elif value.startswith('Anda Pradyta -'):
                            parts = ['Billy PN', value[14:]]
                        elif value.startswith('Ludmilla W -'):
                            parts = ['Ludmilla W', value[12:]]
                        elif grantee == 'rapotivi' and ' a.n ' in value:
                            parts = ['Unknown', value]
                        elif value in (
                                'Reimbursh biaya konsumsi rapat pengelolaan rapotivi',
                                'Biaya konsumsi rapat video rapotivi',
                                'Biaya konsumsi rapat rapotivi',
                                'Reimbursh biaya konsumsi rapat',
                                'Biaya konsumsi rapat dgn web designer Rapotivi',
                                'Reimbursh biaya konsumsi rapat dengan web desainer rapotivi',
                                'Reimbursh biaya konsumsi rapat rapotivi',
                                ):
                            parts = ['Unknown', value]
                        else:
                            raise ValueError('unknown rincian line: %r' % parts)
                    print('Unusual name/title rincian line parsed as : %r' % parts)

                record['nama'] = parts[0].strip().strip('.').replace('  ', ' ')
                record['title'] = parts[1].strip('.').replace('  ', ' ')
            elif '<!--Biaya' in prefix:
                record['biaya'] = value
            elif '<!--Pranala nota' in prefix:
                value = strip_wiki_filelink(value)
                if value:
                    record['nota'] = value
            elif '<!--Tanggal pembayaran' in prefix:
                value = parse_date_string(value)
                if value:
                    record['tanggalpelunasan'] = value
            elif '<!--Pranala bukti transfer' in prefix:
                value = strip_wiki_filelink(value)
                if value:
                    record['notapelunasan'] = value
            else:
                print('unknown template line: %s' % line)
        else:
            print('unknown line: %s' % line)

    return records


def get_name_id(record, grantee):

    name_id = ''
    name_parts = record['nama'].split(' ')

    for part in name_parts:
        if len(part) > len(name_id):
            name_id = part.title()

    if grantee == 'kerjabilitas':
        if name_id == 'Anda':
            name_id = 'Pradyta'
        elif name_id in ('Bily', 'Biily'):
            name_id = 'Billy'
        elif name_id in ('Akbar', 'Pribadi', 'M.Akbar'):
            name_id = 'Akbar_P'

    return name_id


record_template = """---
proyek: {proyek}
kode: {kode}
anggaran: {anggaran}
nama: {nama}
title: {title}
date: {tanggal}
biaya: {biaya}
nota: {nota}
tanggalpelunasan: {tanggalpelunasan}
notapelunasan: {notapelunasan}
---
"""
def create_record(filename, record):
    record = record.copy()
    record['biaya'] = record['biaya'].replace(',', '')
    if 'nota' not in record:
        record['nota'] = ''
    if 'tanggalpelunasan' not in record:
        record['tanggalpelunasan'] = ''
    if 'notapelunasan' not in record:
        record['notapelunasan'] = ''

    grantee = record['proyek']
    code = record['kode']

    s = record_template.format_map(record)
    s2 = ''
    for line in s.splitlines():
        s2 += line.strip() + '\n'

    with open(filename, 'w') as f:
        f.write(s2)


def name_records(grantee, records):
    named_records = {}

    for record in records:
        name_id = get_name_id(record, grantee)

        code = record['kode']

        title = record['title']
        if title.startswith('Pembayaran honor desainer infografis: "7 Jurus'):
            title = 'Pembayaran honor desainer infografis-2016-09-01'

        short_slug = '%s-%s-%s-%s' % (
            grantee,
            code,
            name_id,
            slugify(title),
        )
        if short_slug not in named_records:
            named_records[short_slug] = record
            continue

        same_slug_record = named_records[short_slug]
        if isinstance(same_slug_record, dict):
            # Prevent short slug from being used
            named_records[short_slug] = [same_slug_record]

            # Rename the pre-existing record with the same name
            slug = '%s-%s-%s-%s-%s' % (
                grantee,
                code,
                name_id,
                slugify(same_slug_record['title']),
                same_slug_record['tanggal'],
            )
            named_records[slug] = same_slug_record
        else:
            same_slug_record.append(record)

        slug = '%s-%s-%s-%s-%s' % (
            grantee,
            code,
            name_id,
            slugify(title),
            record['tanggal'],
        )
        if slug in named_records:
            same_slug_record = named_records[slug]
            if isinstance(same_slug_record, dict):
                named_records[slug + '-1'] = same_slug_record
                same_slug_record = [same_slug_record]
                named_records[slug] = same_slug_record

            named_records[slug + '-' + str(len(same_slug_record) + 1)] = record
            same_slug_record.append(record)
        else:
            named_records[slug] = record

    return named_records


def create_records(data_dir, records):
    for slug, record in records.items():
        if isinstance(record, list):
            continue

        filename = os.path.join(data_dir, slug + '.markdown')
        try:
            create_record(filename, record)
            print('Created %s' % filename)
        except Exception as e:
            print('Failed record: %r' % record)
            raise


def check_records(records, grantee):
    name_ids = set()
    for record in records:
        name_id = get_name_id(record, grantee)
        name_ids.add(name_id)

    print('name IDs: %s' % ','.join(sorted(name_ids)))


def main(argv=None):
    source_dir = argv[1]
    grant_round = argv[2] #  CMS
    grantee = argv[3].lower()  # Kerjabilitas

    structure = load_structure(grantee)

    pagename = '2016/CMS/Kerjabilitas/Laporan_Penggunaan_Dana/B1'
    data_dir = '_laporan-keuangan-%s/' % grant_round.lower()

    records = []
    for code, section in structure['laporan'].items():
        if 'subkode' not in section:
            print('No subcodes for %s' % code)
            wikitext = load_saved_wikitext(source_dir, code)
            code_records = parse_wikitext(wikitext, grantee)

            for record in code_records:
                record['proyek'] = grantee
                record['anggaran'] = section['nama']
                record['kode'] = code
                records.append(record)

            continue

        for code, code_name in section['subkode'].items():
            print('Parsing %s' % code)
            wikitext = load_saved_wikitext(source_dir, code)
            code_records = parse_wikitext(wikitext, grantee)

            for record in code_records:
                record['proyek'] = grantee
                record['anggaran'] = code_name
                record['kode'] = code
                records.append(record)

    check_records(records, grantee)
    records = name_records(grantee, records)
    print(records.keys())
    create_records(data_dir, records)


if __name__ == '__main__':
    main(sys.argv)
