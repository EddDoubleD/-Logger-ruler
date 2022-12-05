import os
import re
from sys import argv
from datetime import datetime

now = datetime.now().strftime('%c')

if __name__ == '__main__':
    script, directory, name = argv
    print(f'Статистика по процедуре {name}')
    regExp = "<%s> завершен за \d{1,100} мс" % name
    pattern = re.compile(regExp)
    for current_dir, dirs, files in os.walk(directory):  # передаем в качестве аргумента текущую директорию
        for file in files:
            with open(directory + "/" + file, "r") as f, open(f'out/{name}_{now}.txt', "a") as output:
                i = 0
                for line in f:
                    arr = pattern.findall(line)
                    if arr.__len__() > 0:
                        output.write(arr[0] + "\n")
    # init
    above = [0, 0, 0, 0]
    sum = max = below = 0
    avg = float(0)
    with open(f'out/{name}_{now}.txt', "r") as f:
        text = f.read()
        arr = re.findall("\d{1,100}", text)
        int_lst = [int(x) for x in arr]
        for x in int_lst:
            sum += x
            if max < x:
                max = x
        avg = sum/int_lst.__len__()
        for x in int_lst:
            if x > avg * 10:
                above[3] += 1
            elif x > avg * 3:
                above[2] += 1
            elif x > avg * 2:
                above[1] += 1
            elif x > avg:
                above[0] += 1
            else:
                below += 1

    with open(f'out/{name}_{now}.txt', "a") as f:
        f.write(f'max: {max}, avg: {avg}, above: {above[0]}|{above[1]}|{above[2]}|{above[3]}, below: {below}')