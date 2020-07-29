line = 'a,b,c,d,e,f,g,h,i'

lines = ''
for x in range(100005):
    lines += line + '\n'

with open('BigFile.csv', 'w+') as f:
    f.write(lines)
f.close()
