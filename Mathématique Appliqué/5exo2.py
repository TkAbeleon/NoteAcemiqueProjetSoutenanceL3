def division_euclidienne(a:int,b:int):
    q:int=a//b
    r:int=a%b
    if r>=0:
        return (q, r)
    else:
        q+=1
        r=a- (b*(q))
        return (q,r)

def modulo(a: int,b: int, c: int):
    print(f"- {a} = {a%b} mod{b}---{c}")
    return a%b

x = 0
while True:
    print("***************")
    print(f"\tx = {x}")
    a = modulo(x, 7, 3)
    b = modulo(x, 11, 1)
    c = modulo(x, 13, 5)
    d = modulo(x, 17, 15)
    e =modulo(x, 23, 12)
    if a==3 and b==1 and c==5 and d==15 and e==12:
        break

    x+=1
print(f"$$$$$$$$$$$$$$$$$$$$$$$$$$")
print(f"x = {x}")