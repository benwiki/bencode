def contains(a, b):
    how_much=0
    for item in a:
        if item in b:
            how_much+=1
    return how_much

def main():
    n, m, k = input().split()
    n, m, k = (int(x) for x in (n, m, k))
    conn = [input().split() for i in range(m)]
    conn = [[int(conn[i][j]) for j in range(2)] for i in range(m)]
    conn_strong=[[0,i+1] for i in range(m)]
    for item in conn:
        for j in item:
            conn_strong[j-1][0]+=1
    conn_strong.sort()
    #print(k)
    #print(conn_strong)
    #conn_strong= list(reversed(conn_strong))
    elit = [conn_strong[i] for i in range(m) if conn_strong[i][0]>=k]
    #print(elit)
    elit_conns = [[conn[i][j] for i in range(m) for j in range(2) if ((elit[z][1] in conn[i]) and (elit[z][1]!=conn[i][j]))] for z in range(len(elit))]
    #print(elit_conns)
    elit_mass = [item[1] for item in elit]
    #print(elit_mass)
    ready=[]
    for cons in elit_conns:
        if contains(cons, elit_mass)>=k:
            ready.append(elit[elit_conns.index(cons)][1])
    #print (ready)
    print (len(ready))
    ready.sort()
    #ready=reversed(ready)
    for item in ready:
        print(item, end=' ')
    return 0
                   
main()
