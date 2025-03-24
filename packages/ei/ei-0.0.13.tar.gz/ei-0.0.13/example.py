def main():
    a = 123
    b = 0
    return a / b

if __name__ == '__main__':
    import ei
    a = 123
    b = 123
    ei.embed(soft_ns={'a': 234}, hard_ns={'b': 345}, resume=False)
    
    # def f1():
    #     x1 = 1
    #     def f2():
    #         x2 = 2
    #         ei.embed(True, 1)
    #     f2()
    # f1()
    # with ei.capture(): # overwrites sys.excepthook
    main()
