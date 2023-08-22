import time

def findFactors(num):
    factors = []
    for i in range(1, num+1):
        if len(factors) == 2:
            return factors
        if i % 1000000 == 0:
            print(i)
        if num % i == 0:
            if i == num or i == 1:
                continue
            factors.append(i)

initTime = time.perf_counter()      
print(findFactors(13425857578998206661131))
print(time.perf_counter() - initTime)