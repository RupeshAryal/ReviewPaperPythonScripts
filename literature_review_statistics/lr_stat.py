import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import re

df = pd.read_excel('assets/doi_file.xlsx', sheet_name=['with Abstract'])
df = df['with Abstract']

bibtex = list(df['bibtex'])


def get_bib_enteries(entrytype):

    valid_entry = ['year', 'author', 'publisher', 'journal', 'title']

    if str(entrytype).lower().strip() not in valid_entry:
        print(f"{entrytype} is not a valid entry. Please enter any one of f{valid_entry}")
        return

    pattern = f'{entrytype}' + '[\s]*=[\s]*\{.*?\}'
    enteries = []
    
    for bib in bibtex:
        try:
            matches = re.findall(pattern, bib)
            if matches: 
                journal_pattern = r'\{(.*?)\}'
                final_match = re.findall(journal_pattern, matches[0])
                enteries.append(final_match[0])
            else:
                enteries.append(np.nan)

        except TypeError:
            enteries.append(np.nan)
            pass
    return enteries


year = get_bib_enteries('year')
publisher = get_bib_enteries('publisher')
journal = get_bib_enteries('journal')
author = get_bib_enteries('author')
title = list(df['Title'])
paper_type = list(df['Paper Type'])

new_dataset = pd.DataFrame({
    'title': title,
    'year': year,
    
    'journal': journal,
    'publisher': publisher,
    'paper_type': paper_type,
})

new_dataset.to_csv('assets/bib_enteries.csv', sep=',')




