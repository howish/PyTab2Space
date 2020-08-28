# Tab to space

Convert all tabs in your code bases to spaces as visually identical. 
(Monospaced Font is assumed) \
It may runs not so fast on big project but in correct way.

# Get started
Clone to repository, and run the following script:
```bash
python t2s.py <path_to_file>
```
Feel free to try, it will create new file/folder instead of overwriting it:


# Optional arguments
- \[-f\| --is_folder]: Convert the tabs in whole project.
- \[-o\| --overwrite]: Run in unsafe mode. It overwrite the original file/folder structure. 
- \[-w\| --tab_width]: Assign tab size if you need. (default = 4)
- \[-e\| --code_ext]: Assign code extension types if you need. \
(default = ('.c', '.cc', '.h', '.py', '.cs'))


# Known issue
- Those file with unicode reading problem will be ignored.
