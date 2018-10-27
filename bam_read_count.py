from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import open
from builtins import int
from future import standard_library
standard_library.install_aliases()
import csv
import argparse
import sys
import re

def process_csv(input_path, dest_csv, input_delimiter='\t', output_delimiter='\t'):
    """
    read the CSV file
    Each row looks like
    
    ChrI	131602	A	43	Err:510	A:1:60.00:41.00:60.00:1:0:0.97:0.00:0.00:1:0.51:116.00:0.44	C:42:20.64:40.21:20.64:42:0:0.54:0.12:376.74:42:0.62:76.90:0.38	G:0:0.00:0.00:0.00:0:0:0.00:0.00:0.00:0:0.00:0.00:0.00	T:0:0.00:0.00:0.00:0:0:0.00:0.00:0.00:0:0.00:0.00:0.00	N:0:0.00:0.00:0.00:0:0:0.00:0.00:0.00:0:0.00:0.00:0.00
    Do:
    * skip the 5th column
    * Keep columns 1-4
    * Take the first number after A, C, G, T, N

    There will be 9 columns in the output file.

    * input_path: path to the input CSV file
    * dest_csv: path to the destination file to write
    """
    pat = re.compile('(.+?):(.*)')
    with open(input_path, 'r') as csvfile,\
        open(dest_csv, 'w') as dest:
        csvreader = csv.reader(csvfile, delimiter=input_delimiter, quotechar='"')
        csvwriter = csv.writer(dest, delimiter=output_delimiter, quotechar='"')

        row_ind = 1
        for inrow in csvreader:
            if len(inrow) <= 10:
                try:
                    outrow = []
                    outrow.extend(inrow[:4])

                    # According to an expert, this column is supposed to be the sum
                    # of the following 4 numbers to be extracted (all non-negative
                    # integers).
                    fourth_col = int(inrow[3])
                    # skip the 5th column (index = 4)
                    sum_value = 0
                    for i, colv in enumerate(inrow[5:]):
                        # colv looks like 
                        # G:0:0.00:0.00:0.00:0:0:0.00:0.00:0.00:0:0.00:0.00:0.00
                        # Want to take only the first number after the first letter
                        colv = colv.strip()
                        # skip the first two characters
                        colv2 = colv[2:]
                        m = pat.match(colv2)
                        first_num = m.group(1)
                        first_num = int(first_num)
                        outrow.append(first_num)
                        sum_value += first_num
                    assert sum_value == fourth_col

                    # Write the output row
                    csvwriter.writerow(outrow)
                except:
                    raise ValueError('{}: {}'.format(row_ind, inrow))
            else:
                print('Ignoring row {} because there are more than 10 columns.'.format(row_ind))

            row_ind += 1


def main():
    # parser = argparse.ArgumentParser(description='PyTorch GKMM on MNIST. Some paths are relative to the "(share_path)/prob_models/". See settings.ini for (share_path).')

    # parser.add_argument('--input', type=str, help='Path to the input CSV file',
    #         required=True)
    # args = parser.parse_args()
    # args_dict = vars(args)
    if len(sys.argv) < 3:
        print('Usage: {} path_to_input_text_file  path_to_output_csv'.format(sys.argv[0]))
        print('Both input and output files are tab separated.')
        sys.exit(1)
    input_path = sys.argv[1]
    dest_path = sys.argv[2]
    process_csv(input_path, dest_path)


if __name__ == '__main__':
    main()
