def main():
    # Variables temporales
    t2 = None
    t3 = None
    t1 = None
    t5 = None
    t6 = None
    t4 = None
    t0 = None
    
    x = 5
    y = 3
    t0 = x + y
    t1 = t0 * 2
    z = t1
    if z < 5:
        print(y)
    elif z > 5:
        print(x)
    for i in range(0, 3):
        print(i)
    while x > 0:
        x = x - 1
        print(x)

if __name__ == '__main__':
    main()