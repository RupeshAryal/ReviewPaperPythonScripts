import pandas as pd

df = pd.read_excel('../assets/doi_file.xlsx', sheet_name=['with Abstract'])
df = df['with Abstract']['Abstract ']

all_abstract = list(df)

for abst in all_abstract:
    with open("assets/abstract_file.txt", 'a') as f:
        abstract = str(abst).strip().replace('\n', ' ')
        f.write('\n')
        f.write(abstract)
