import subprocess
import os
import re

test_files = [x for x in os.listdir() if re.search(r'.*_test.py', x)]

for test in test_files:
    subprocess.Popen(f'pytest {test}', subprocess.STARTF_USESTDHANDLES | subprocess.STARTF_USESHOWWINDOW).communicate()