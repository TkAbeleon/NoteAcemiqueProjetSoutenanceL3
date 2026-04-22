from exo import modulo
solution = []
x = 0
a = 750005
b = 1500010
c = 9876545
while True:
    print(f"############# x = {x} #############")
    y = modulo(a*x, c, b)
    if x==c: break
    if y==b:
        solution.append(x)
    x+=1
print()
print()
print()
print()
print()
print()

print(f"$$$$$$$$$$$$$$$$$$$$$$$$$$")
print(f"x = {solution}")

x = [2, 1975311, 3950620, 5925929, 7901238]
