import time
from matplotlib.lines import lineStyles
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import numpy as np
# from sideway_alien_invasion import AlienInvasion

"""what I want to do is keep recording timestamps of while loop and how cpu try to execute the loop and want to discover any pattern if exist"""
# 한글 폰트를 지정 (Windows의 경우 Malgun Gothic, Mac의 경우 AppleGothic)
plt.rcParams['font.family'] = 'Malgun Gothic'  # 또는 'NanumGothic' 등

# 폰트에서 마이너스 기호가 제대로 표시되도록 설정
plt.rcParams['axes.unicode_minus'] = False
timestamp_cntn = []

def save_timediff():
    max_second = 1
    for p_cnt in range(10):
        s_time = time.time()

        while True:
            t = time.time ()
            timestamp_cntn.append(t)
            for _ in range(p_cnt):
                i = 100
                y = 100
                z = 10
                    
            if (time.time()-s_time > max_second):
                break
        
        df = pd.DataFrame({'timestamp': timestamp_cntn})

        # Calculate the elapsed time relative to the first timestamp
        df['elapsed_time'] = df['timestamp'].diff()
        
        # file_name
        f_name = f"timestamp_assignment_{p_cnt}.csv"
        current_file_path = os.path.abspath(__file__)
        # save the data to a CSV file
        df.to_csv(os.path.join(os.path.dirname(current_file_path), f_name), index=False)

def get_timestamp_files():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    files = glob.glob(os.path.join(current_dir, '*timestamp_assignment_*.csv'))
    
    return files


def show_graph(file_path):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        print(f"{e}")
    dir_path, filename = os.path.split(file_path)
    filenameonly, _ = os.path.splitext(filename)
    
    plt.figure()
    plt.plot(
        df['timestamp'].iloc[1:], 
        df['elapsed_time'].iloc[1:], 
        marker='o',
        markersize=1.5,
        linestyle='-'
    )
    plt.grid(True)
    plt.title(f"{filename}")
    plt.savefig(os.path.join(dir_path, filenameonly+'.png'), dpi=300, bbox_inches='tight')

def price_index():
    df = pd.read_excel(r"C:\Users\youngho\Downloads\소비자물가지수_2020100__20240810214013.xlsx")
    print(df.head())
    
    x = np.arange(1986, 2024)
    y = df[(df['시점'] >= 1986) & (df['시점'] <= 2023)]['전국']
    plt.figure(figsize=(18, 6))
    plt.plot(x, y, linestyle='-')
    plt.title('소비자물가지수(%)')
    plt.xlabel('연도')
    plt.grid(False)
    plt.show()
    
if __name__ == '__main__':
    # save_timediff()
    # 
    # files = get_timestamp_files()

    # for f in files:
    #     show_graph(f)
    price_index()