"""
@Author: Conghao Wong
@Date: 2024-12-24 15:38:03
@LastEditors: Conghao Wong
@LastEditTime: 2024-12-24 16:03:31
@Github: https://cocoon2wong.github.io
@Copyright 2024 Conghao Wong, All Rights Reserved.
"""

import os
import sys
import json

sys.path.insert(0, os.path.abspath('.'))

DATA_FILE_PAPER = './scripts/pub_data.json'
TEMPLATE_FILE = './scripts/pub_template.html'
TARGET_FILE = './publications/index.md'


def load_one_paper(title, authors, status, journal, arxiv, template,
                   github=None, homepage=None, picture=None, **kwargs):
    
    if status == 'I':
        status = '<strong class="hf_03">In progress</strong>'
    elif status == 'C':
        status = '<strong class="hf_01">Conference</strong>'
    elif status == 'J':
        status = '<strong class="hf_02">Journal</strong>'
    else:
        status = ''

    github = '<a class="btn btn-colorful btn-lg" href="{}">GitHub</a>'.format(
        github) if github else ''

    homepage = '<a class="btn btn-colorful btn-lg" href="{}">Homepage</a>'.format(
        homepage) if homepage else ''

    picture = '<img src="/subassets/img/publications/{}">'.format(
        picture) if picture else ''

    return template.format(title,
                           authors,
                           status,
                           journal,
                           github,
                           arxiv,
                           homepage,
                           picture)


def read_papers(data_file: str):
    with open(TEMPLATE_FILE, 'r') as f:
        template_lines = f.readlines()

    template = ''.join(template_lines)

    with open(data_file, 'r') as f:
        data = json.load(f)

    all_repos: dict[int, str] = {}
    for _dat in data:
        year = _dat['year']
        if not year in all_repos.keys():
            all_repos[year] = []
            
        all_repos[year].append(load_one_paper(**_dat, template=template))

    for key, value in all_repos.items():
        all_repos[key] = ''.join(value)
    
    return all_repos

if __name__ == '__main__':
    papers = read_papers(DATA_FILE_PAPER)

    new_line = ''
    for key, value in papers.items():
        new_line += f'## {key}\n'
        new_line += value

    with open(TARGET_FILE, 'r') as f:
        current_lines = f.readlines()
    
    current_lines = ''.join(current_lines)
    current_lines = current_lines.format(new_line)

    with open(TARGET_FILE, 'w') as f:
        f.write(current_lines)
