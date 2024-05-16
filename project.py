import time
from colorama import Fore, Back, Style
import os
import numpy as np
import psutil
from matplotlib import pyplot as plt

def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

def profile(func):
    def wrapper(*args, **kwargs):
        mem_before = process_memory()
        result = func(*args, **kwargs)
        mem_after = process_memory()
        print(Fore.CYAN+"Bellek Kullanımı: {:,}".format(
            mem_before, mem_after, mem_after - mem_before))
        memory_usages.append("{:,}".format(mem_before, mem_after, mem_after - mem_before))
        return result
    return wrapper

def f_turev(x,fminor):
    return 1+2*fminor

f0 = 0.5

results = []

@profile
def calc(iter,start_val,target_val):
    f0copy = f0
    diff = target_val - start_val
    diff /= iter
    print(Fore.RED,end='')
    print(f"İterasyon Sayısı:{iter} Δx={diff}")
    for i in range(iter):
        start_val = f0copy + f_turev(start_val,f0copy)*diff
        f0copy = start_val
    print(Fore.YELLOW,end='')
    print(f"f({target_val}) = {start_val}")

def measure_time(func, *args):
    start = time.perf_counter()
    func(*args)
    end = time.perf_counter()
    return end - start
   
memory_usages = []
runtimes = []
iterations = [2,5,10,20,50,100,200,500,1000]

for i in iterations:
    time_elapsed = measure_time(calc,i,0,0.2)
    print(Fore.GREEN,end='')
    print(f"Geçen Süre:{time_elapsed} seconds")
    runtimes.append(time_elapsed)    
print(Fore.WHITE)


fig, axs = plt.subplots(1, 2)

axs[0].plot(iterations, runtimes)
axs[0].set_title('Çalışma Zamanı')
axs[0].set_xlabel('Iterasyon Sayısı')
axs[0].set_ylabel('Çalışma Zamanı (saniye)')

axs[1].plot(iterations, memory_usages)
axs[1].set_title('Bellek Kullanımı')
axs[1].set_xlabel('Iterasyon Sayısı')
axs[1].set_ylabel('Bellek Kullanımı (byte)')


plt.tight_layout()
plt.show()