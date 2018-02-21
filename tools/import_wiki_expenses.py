import os
import sys

import requests
import yaml
from slugify import slugify

WIKI_URL = 'https://wiki.ciptamedia.org/wiki/'
DOWNLOAD_DIR = '/home/jayvdb/Downloads/'

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


def load_saved_wikitext(code):
    filename = os.path.join(DOWNLOAD_DIR, code)
    with open(filename) as f:
        wikitext = f.read()
        return wikitext

def strip_wiki_filelink(wikitext):
    wikitext = wikitext.replace('[[:Berkas:', '').replace(']', '')
    if '|' in wikitext:
        filename = wikitext.split('|', 1)[0].strip()
    else:
        filename = wikitext.strip()

    return 'https://wiki.ciptamedia.org/wiki/File:%s' % filename


def parse_date_string(wikitext):
    if not wikitext:
        return ''

    parts = wikitext.split(' ')
    if len(parts) != 3:
        raise ValueError('Unknown date %r' % parts)

    if parts[1].title() in INDONESIAN_MONTH_NAMES:
        month_id = INDONESIAN_MONTH_NAMES[parts[1].title()]
    else:
        raise ValueError('Unknown date %r' % parts)

    assert len(parts[2]) == 4
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

def parse_wikitext(wikitext):
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
                records.append(record)
                # print(record)  # do stuff

            record = {}
        elif '-->' in line:
            prefix, value = line.rsplit('-->', 1)
            value = value.strip()
            value = value.replace('  ', ' ')
            if not value or value == '-':
                continue

            if '<!--Tanggal transaksi' in prefix:
                record['tanggal'] = parse_date_string(value)
            elif '-Nama-->' in prefix and value:
                value = value
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
                        else:
                            print('unknown rincian line: %r' % parts)
                            continue
                    print('Unusual name/title rincian line parsed as : %r' % parts)

                record['nama'] = parts[0].strip().strip('.').replace('  ', ' ')
                record['title'] = parts[1].strip('.').replace('  ', ' ')
            elif '<!--Biaya' in prefix:
                record['biaya'] = value
            elif '<!--Pranala nota' in prefix:
                record['nota'] = strip_wiki_filelink(value)
            elif '<!--Tanggal pembayaran' in prefix:
                record['tanggalpelunasan'] = parse_date_string(value)
            elif '<!--Pranala bukti transfer' in prefix:
                value = value.strip()
                if value and value.lower() != 'lunas':
                    record['notapelunasan'] = strip_wiki_filelink(value)
            else:
                print('unknown template line: %s' % line)
        else:
            print('unknown line: %s' % line)

    return records


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
def create_record(data_dir, record, project_name, code, code_name):
    record = record.copy()
    record['proyek'] = project_name
    record['anggaran'] = code_name
    record['kode'] = code
    record['biaya'] = record['biaya'].replace(',', '')
    if 'tanggalpelunasan' not in record:
        record['tanggalpelunasan'] = ''
    if 'notapelunasan' not in record:
        record['notapelunasan'] = ''

    name_id = ''
    name_parts = record['nama'].split(' ')
    for part in name_parts:
        if len(part) > len(name_id):
            name_id = part.title()

    if name_id == 'Anda':
        name_id = 'Pradyta'
    elif name_id == 'Bily':
        name_id = 'Billy'
    elif name_id in ('Akbar', 'Pribadi', 'M.Akbar'):
        name_id = 'Akbar_P'

    filename = '%s-%s-%s-%s.markdown' % (
        project_name,
        code,
        name_id,
        slugify(record['title']),
    )
    path = os.path.join(data_dir, filename)
    if os.path.exists(path):
        # Should check if the file contents are identical
        filename = '%s-%s-%s-%s-%s.markdown' % (
            project_name,
            code,
            name_id,
            slugify(record['title']),
            record['tanggal'],
        )
        path = os.path.join(data_dir, filename)
        if os.path.exists(path):
            # Should check if the file contents are identical
            filename = '%s-%s-%s-%s-%s.markdown' % (
                project_name,
                code,
                name_id,
                slugify(record['title']),
                abs(hash(record['nota'])),
            )
            path = os.path.join(data_dir, filename)
            if os.path.exists(path):
                raise ValueError('path %s already exists before %r' % (path, record))

    s = record_template.format_map(record)
    s2 = ''
    for line in s.splitlines():
        s2 += line.strip() + '\n'


    with open(path, 'w') as f:
        f.write(s2)

    print('Created %s' % path)
    return path


def create_records(data_dir, structure_section, records, project_name, code):
    if code == 'X':
        code_name = 'Biaya Lain'
    else:
        code_name = structure_section['subkode'][code]

    for record in records:
        try:
            create_record(data_dir, record, project_name, code, code_name)
        except Exception as e:
            print('Failed record: %r' % record)
            raise


def main(argv=None):
    year = argv[1]  # 2016
    grant_round = argv[2] #  CMS
    grantee = argv[3]  # Kerjabilitas
    code = argv[4]  # B1

    structure = load_structure(grantee)
    structure_section = structure['laporan'][code[0]]

    pagename = '2016/CMS/Kerjabilitas/Laporan_Penggunaan_Dana/B1'
    data_dir = '_laporan-keuangan-%s/' % grant_round.lower()

    wikitext = load_saved_wikitext(code)
    records = parse_wikitext(wikitext)
    create_records(data_dir, structure_section, records, project_name=grantee.lower(), code=code)


if __name__ == '__main__':
    main(sys.argv)
