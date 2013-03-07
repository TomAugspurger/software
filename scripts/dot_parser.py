with open('f.dot', 'w') as fout:
    with open('test.dot', 'r') as fin:
        for l in fin.readlines():
            li = l.split(' ')
            if len(li) > 1:
            	fout.write(l)
    fout.write('\n}')
            
