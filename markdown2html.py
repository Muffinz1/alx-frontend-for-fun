#!/usr/bin/python3
"""
Module for the html convertor
"""


import sys
import os
import re
import hashlib


def process_line(line, unordered_start, ordered_start, paragraph):
    """
    Executes the conversion of the code into an html file
    """
    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
    line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)

    md5_matches = re.findall(r'\[\[(.+?)\]\]', line)
    for match in md5_matches:
        hashed = hashlib.md5(match.encode()).hexdigest()
        line = line.replace(f'[[{match}]]', hashed)

    remove_c_matches = re.findall(r'\(\((.+?)\)\)', line)
    for match in remove_c_matches:
        cleaned = re.sub(r'[cC]', '', match)
        line = line.replace(f'(({match}))', cleaned)

    length = len(line)
    headings = line.lstrip('#')
    heading_num = length - len(headings)
    unordered = line.lstrip('-')
    unordered_num = length - len(unordered)
    ordered = line.lstrip('*')
    ordered_num = length - len(ordered)

    if 1 <= heading_num <= 6:
        line = f'<h{heading_num}>{headings.strip()}</h{heading_num}>\n'

    if unordered_num:
        if not unordered_start:
            line = '<ul>\n<li>' + unordered.strip() + '</li>\n'
            unordered_start = True
        else:
            line = '<li>' + unordered.strip() + '</li>\n'

    if unordered_start and not unordered_num:
        line = '</ul>\n' + line
        unordered_start = False

    if ordered_num:
        if not ordered_start:
            line = '<ol>\n<li>' + ordered.strip() + '</li>\n'
            ordered_start = True
        else:
            line = '<li>' + ordered.strip() + '</li>\n'

    if ordered_start and not ordered_num:
        line = '</ol>\n' + line
        ordered_start = False

    if not (heading_num or unordered_start or ordered_start):
        if not paragraph and length > 1:
            line = '<p>\n' + line
            paragraph = True
        elif length > 1:
            line = line + '<br/>\n'
        elif paragraph:
            line = '</p>\n' + line
            paragraph = False

    return line, unordered_start, ordered_start, paragraph


if __name__ == '__main__':
    if len(sys.argv) < 3:
        text = " ./markdown2html.py README.md README.html"
        print('Usage:' + text, file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        print(f'Missing {sys.argv[1]}', file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as read_file:
        with open(sys.argv[2], 'w') as html_file:
            unordered_start = False
            ordered_start = False
            paragraph = False

            for line in read_file:
                line, unordered_start, ordered_start, paragraph = process_line(
                    line, unordered_start, ordered_start, paragraph)
                html_file.write(line)

            if unordered_start:
                html_file.write('</ul>\n')
            if ordered_start:
                html_file.write('</ol>\n')
            if paragraph:
                html_file.write('</p>\n')

    sys.exit(0)
