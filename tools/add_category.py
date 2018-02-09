from io import StringIO
import os
import sys

import frontmatter

from ruamel.yaml import YAML

yaml = YAML()
yaml.width = 4096


class RuamelYAMLHandler(frontmatter.YAMLHandler):

    def load(self, fm, **kwargs):
        """
        Parse YAML front matter.
        """
        return yaml.load(fm, **kwargs)

    def export(self, metadata, **kwargs):
        """
        Export metadata as YAML.
        """
        f = StringIO()
        yaml.dump(metadata, f)

        return frontmatter.u(f.getvalue().strip())


def fix_post(data_file):
    handler = RuamelYAMLHandler()
    with open(data_file) as f:
        doc = frontmatter.load(f, handler=handler)

    if 'categories' not in doc.metadata:
        raise ValueError('no categories')

    categories = doc.metadata['categories']

    if 'laporan' not in categories:
        return

    if doc.metadata.get('layout') == 'laporancmb':
        category = 'CMB'
    else:
        category = 'CMS'

    if category not in categories:
        doc.metadata['categories'] = categories[0:-1] + [category, categories[-1]]

    with open(data_file, 'wb') as f:
        frontmatter.dump(doc, f, handler=handler)

    with open(data_file, 'ab') as f:
        f.write(b'\n')


errors = 0
for data_file in os.listdir('_posts'):
    data_file = os.path.join('_posts', data_file)

    if os.path.isdir(data_file):
        continue

    try:
        fix_post(data_file)
    except Exception as e:
        print(data_file, e)
        errors += 1


