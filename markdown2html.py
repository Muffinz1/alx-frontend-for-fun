"""
Module for the html convertor
"""
import argparse
import pathlib
import re


def html_convertor(input_file, output_file):
    """
    Executes the conversion of the code into an html file
    """
    with open(input_file, encoding='utf-8') as f:
        mark_down_file = f.readlines()

    html_contents = []
    for line in mark_down_file:
        match = re.match(r'(#){1,6} (.*)', line)
        if match:
            header_stat = len(match.group(1))
            header_cont = match.group(2)
            html_contents.append(f'<h{header_stat}>{header_cont}</h{header_stat}>\n')
        else:
            html_contents.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(html_contents)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert markdown to HTML')
    parser.add_argument('input_file', help='path to input markdown file')
    parser.add_argument('output_file', help='path to output HTML file')
    args = parser.parse_args()

    input_path = pathlib.Path(args.input_file)
    if not input_path.is_file():
        print(f'Missing {input_path}', file=sys.stderr)
        sys.exit(1)

    html_convertor(args.input_file, args.output_file)