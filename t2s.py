import argparse
import os
import re
from wcwidth import wcswidth


class Tab2Space:
    linesep = '\n'
    tab_width = 4
    code_exts = ('.c', '.cc', '.h', '.py', '.cs')
    safe_mode = True

    def __init__(self):
        pass

    def tab2space_line(self, line: str):
        line_idx = 0
        newline = ''
        while line:
            # Find tab index
            tab_idx = line.find('\t')
            if tab_idx == -1:
                newline += line
                break
            # Get valid part before tab
            valid_part = line[:tab_idx]
            valid_width = wcswidth(valid_part)
            if valid_width == -1:
                raise ValueError('Unexpected character in valid part:\n {}'.format(repr(valid_part)))
            line_idx += valid_width
            line = line[tab_idx:]
            newline += valid_part

            # Find first not tab idx
            search_result = re.search(r'[^\t]', line)
            tab_num = search_result.start() if search_result is not None else len(line)
            space_num = tab_num * self.tab_width - line_idx % self.tab_width
            line = line[tab_num:]
            newline += space_num * ' '
        return newline

    def tab2space_file(self, input_file_path, output_file_path=None):
        print('[Process] Parsing', input_file_path)
        if output_file_path is None:
            if self.safe_mode:
                p1, p2 = os.path.splitext(input_file_path)
                output_file_path = p1 + '_notab' + p2
            else:
                input_file_path = output_file_path
        with open(input_file_path, 'r') as infile:
            try:
                content = infile.read()
            except UnicodeDecodeError:
                print('[Error 0] Parse failed. Unicode decode error')
                return
        new_content = self.linesep.join([self.tab2space_line(line) for line in content.splitlines()])
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w') as file:
            file.write(new_content)

    def all_code_file(self, folder):
        for name in os.listdir(folder):
            name_path = os.path.join(folder, name)
            if os.path.isdir(name_path):
                for file in self.all_code_file(name_path):
                    yield os.path.join(name, file)
            else:
                _, ext = os.path.splitext(name)
                if ext in self.code_exts:
                    yield name

    def tab2space_allcodes(self, input_folder):
        if self.safe_mode:
            output_folder = input_folder + '_notab'
        else:
            output_folder = input_folder
        for file_name in self.all_code_file(input_folder):
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, file_name)
            self.tab2space_file(input_file_path, output_file_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='The path of target.')
    parser.add_argument('-f', '--is_folder', help='Add flag if target is folder', action='store_true')
    parser.add_argument('-o', '--overwrite', help='Use unsafe mode', action='store_true')
    parser.add_argument('-w', '--tab_width', help='Width of tab', type=int, default=4)
    parser.add_argument('-e', '--code_ext', help='The target code extensions', nargs='+')
    args = parser.parse_args()
    if args.path:
        t2s = Tab2Space()
        t2s.safe_mode = not args.overwrite
        if args.code_ext is not None:
            t2s.code_exts += args.code_ext
        t2s.tab_width = args.tab_width
        if args.is_folder:
            t2s.tab2space_allcodes(args.path)
        else:
            t2s.tab2space_file(args.path)


if __name__ == '__main__':
    main()
