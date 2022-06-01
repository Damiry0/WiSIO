from pathlib import Path  #
import os

os.chdir('boards')

if not os.path.isdir('siurek'):
    os.mkdir('siurek')
# files = Path('output/').glob('*.*')
# howManyFiles = 0
#
# for file in files:
#     print(file)
#     howManyFiles +=1
#
# print(howManyFiles)

count = 0
dir_path = r'siurek/'
for path in os.scandir(dir_path):
    if path.is_file():
        print(path)
        count += 1
print('file count:', count)

os.remove('siurek/*')
