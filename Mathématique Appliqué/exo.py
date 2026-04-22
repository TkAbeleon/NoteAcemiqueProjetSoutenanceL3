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