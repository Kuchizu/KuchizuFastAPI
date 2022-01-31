import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# print(os.listdir('files'))
print(*filter(lambda xpath: os.path.isfile('files/'+xpath), os.listdir('files')))
# for filename in filter(lambda xpath: os.path.isdir(xpath), os.listdir('files')):
#     print(filename)
