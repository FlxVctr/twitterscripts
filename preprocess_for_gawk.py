# processes arbitrarily formatted csv file with tweet data
# (with two columns named 'text' and 'id')
# so that Axel Bruns' gawk scripts can digest it

# usage:
# python3 [path/to/]script.py [path/to/]inputfile [path/to/]outputfile.tab

# fvmuench@gmail.com

import pandas as pd
import csv
from sys import argv

input_file = argv[1]
output_file = argv[2]

tweettable = pd.read_csv(input_file)

# replace tabs with [tab] and newlines with [newline] in text
tweettable['text'] = tweettable['text'].str.replace('\r\n', '[windowsnewline]')
tweettable['text'] = tweettable['text'].str.replace('\n', '[newline]')
tweettable['text'] = tweettable['text'].str.replace('\t', '[tab]')

# write only id and text column without quotes to output file (tab separated)
tweettable.to_csv(path_or_buf=output_file, sep='\t', index=False,
                  columns=['id', 'text'], float_format='%.0f',
                  encoding='utf-8', quoting=csv.QUOTE_NONE, escapechar='\\')
