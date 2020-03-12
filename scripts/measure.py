#!/usr/bin/env python3

import subprocess
import sys

def mean(l):
    m = 0
    for i in l:
        m += i
    return m / len(l)

def main(argv):

    test_len = len(argv[2:]) # How much methods to be tested
    fib_len = 93             # How much fibonacci numbers
    num_measurement = 150    # How much times of measurement of each fibonacci number
    num_drop = 25            # Drop num_drop * 2 outliers

    # Three dimensional list
    # len(time_record)       -> test_len
    # len(time_record[i])    -> fib_len
    # len(time_record[i][j]) -> num_measurement - 2 * num_drop
    time_record = [[[] for i in range(fib_len)] for j in range(test_len)]
    
    '''
    Reload module
    '''
    subprocess.run(['make', 'unload'])
    subprocess.run('make')
    subprocess.run(['make', 'load'])

    '''
    Measure
    '''
    for method in range(test_len):
        for _ in range(num_measurement):
            subprocess.run(['sudo', 'dmesg', '-C'])
            result = subprocess.check_output(['taskset', '0x1', 'sudo', './client', str(argv[2 + method])]).decode('utf-8').strip().split('\n')
            time = subprocess.check_output(['sudo', 'dmesg']).decode('utf-8').strip().split('\n')

            '''
            Verify
            '''
            a = 0
            b = 1
            idx = 0
            for lines in result[1:]:
                lines = lines.split(',')
                offset = int(lines[0].split(' ')[-1], 10)
                fib = int(lines[1][:-1].split(' ')[-1], 10)

                if offset != idx or fib != a:
                    print('Error!')
                    print(f'Expect: fib({idx}) = {a}')
                    print(f'   Get: fib({offset}) = {fib}')
                    sys.exit(1)

                idx += 1
                b += a
                a = b - a

            '''
            Record
            '''
            for i in range(len(time)):
                time[i] = time[i].split('] ')[1]
                time_record[method][i].append(int(time[i], 10))
    '''
    Output
    '''
    with open(argv[1], 'w') as f:
        for i in range(fib_len):
            f.write(str(i))
            for method in range(test_len):
                f.write(f' {mean(time_record[method][i][num_drop:-num_drop])}')
            f.write('\n')

if __name__ == '__main__':
    argv = sys.argv
    if len(argv) < 3:
        print(f'Usage: {argv[0]} <output_name> <num>')
        print('<num> can be 1 or more numbers.')
        sys.exit(1)
    main(argv)
