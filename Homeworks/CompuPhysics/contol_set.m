%递归主函数
def plotset = set_main(n,set):
    if n == 1:
        plotset = set
    else:
        set = [set ./ 3 , 3/2 + set ./ 3]