filename = input("Enter filename:")
with open(filename, 'r') as f:
    i = 0
    j = 0
    while True:
        buf = ''
        char = f.read(1)
        if not char:
            break
        if char == '\n':
            print(ord(char))






