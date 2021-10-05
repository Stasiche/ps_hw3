import numpy as np
import pandas as pd
from scipy.stats import rankdata
from os.path import exists

def round_to_int(x):
    return np.round(x).astype(int)

def main():
    if not exists('./in.txt'):
        raise FileNotFoundError('Файл с входными данными не найден')
        
    sorted_data = pd.read_table('./in.txt', sep=' ', header=None, names=['x','y']).sort_values('x')
    
    if sorted_data.shape[0] < 9:
        raise ValueError('Слишком мало входных данных')
    
    ranks = rankdata(sorted_data['y'].values, method='average')
    table = pd.concat([sorted_data, 
                       pd.Series(ranks, name='r', index=sorted_data.index)], axis=1).sort_values('x')
    # Поправим порядок ранков с "минимальный к максимальному" на "максимальный к минимальному"
    table.r -= table.r.max() + 1
    table.r *= -1 
    
    N = len(sorted_data)
    p = round(N/3)
    
    R1, R2 = sum(table.r[:p]),sum(table.r[-p:])
    
    diff = R1 - R2
    err = (N + 1/2) * np.sqrt(p/6)
    
    coef = diff / (p*(N-p))

    with open('out.txt', 'w') as f:
        f.writelines(f'{round_to_int(diff)} {round_to_int(err)} {np.round(coef,2)}\n')

if __name__ == "__main__":
    main()