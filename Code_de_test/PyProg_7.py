import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# N_rows = 4
# N_cols = 4
# ar = np.zeros((N_rows, N_cols))

# df = pd.DataFrame(ar, index=['delta 1', 'delta 2', 'delta 3'], columns=['F1', 'F2', 'F3', 'F4'])
df = pd.DataFrame(index=range(0, 4), columns=range(0, 5), dtype=float)
# df = pd.DataFrame(ar)

# print(df)

list_x = [0, 1, 2, 3]
list_y = [0, 1, 2, 3, 4]
id_l = 0
id_c = 0
for ligne in list_x:
    for colonne in list_y:
        df[id_c][id_l] = np.random.randn(1)
        id_c += 1
    id_c = 0
    id_l += 1

vx = df.columns.values
y = df[0]
#print(y)

df.rename(columns = {0: 'Deltas', 1: 'F1', 2: 'F2', 3: 'F3', 4:'F4'}, inplace=True)
#df.rename(index = {0: 'delta 1', 1: 'delta 2', 2: 'delta 3', 3: 'delta 4'}, inplace=True)
print(df)

#df.plot.scatter(x='F1', y='F2')
#plt.show()

# installer openpyxl
# df.to_excel(r'C:\Users\Cl3ment\Desktop\PyProg_7.xlsx', sheet_name='dataframe_1')
# df.to_csv(r'C:\Users\Cl3ment\Desktop\PyProg_7.csv', index = False)

plt.plot(y)
plt.show()