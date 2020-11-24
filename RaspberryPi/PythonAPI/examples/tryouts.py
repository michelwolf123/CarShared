
def func():
    flag1 = True

    flag = True


    if flag1 == True:
        print("TRUE")
        #nonlocal flag
        flag = False

    else:

        if flag == True:
            print("else")

    print()
func()







def func2():
    cat = 1
    
    def func3():
        nonlocal cat
        cat = 2
        print(cat)
    func3()
func2()


flag = True
hund = 1
if flag:
    hund = 2
    print(hund)
print(hund)
