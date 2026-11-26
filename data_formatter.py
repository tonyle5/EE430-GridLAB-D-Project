import pandas as pd

FILE = 'inputs/house_profile_1.csv'

df = pd.read_csv(FILE, comment='#', header=None)
# df[0] = df[0].str.replace('2021-12-25', '2025-09-01')
df[1] = df[1].astype(float) * 1000

# df = df.drop_duplicates(subset=0, keep="first")
df.to_csv(FILE, header=False, index=False)


