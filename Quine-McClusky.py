from itertools import product,combinations
def QuineMcCluskey(mm, dd=[],showMode = 1):
    '''if F = (m0+m1+m2+m5)+(d4+d6), input is mm=[0,1,2,5],dd=[4,6]'''
    '''showMode == 1 -> F = ABC + CDE + ... '''
    '''showMode == 2 -> F = (A`+B`+C`)(C`+D`+E`)... '''
    '''showMode == 3 -> F = abc + cde + ... '''
    '''showMode == 4 -> F = (a`+b`+c`)(c`+d`+e`)... '''
    '''time complexity N means variableN, N is the smallest Number so that 2^N > ALL Elements in mm,dd'''
    '''O(pow(N,3)*pow(2,2N))'''
    variableN = 0
    maxnum = max(mm+dd)
    while 1:
        if maxnum > pow(2,variableN): 
            variableN += 1
        else:
            break
    if variableN > 20:
        return -1
    def num2Bits(num) -> str:
        '''O(N)'''
        num = str(bin(num))[2:]
        if len(num) < variableN:
            num = '0'*(variableN-len(num))+num
        # print(num)
        return num
    def bitsXORbits(num1: str, num2: str) -> int:
        '''O(N)'''
        count = 0
        for i in range(variableN):
            if num1[i] != num2[i] and 'x' not in [num1[i],num2[i]]:
                count += 1
        return count
    def bitsMergebits(num1: str, num2: str) -> int:
        '''O(N)'''
        if bitsXORbits(num1,num2) != 1 or sum([1 if num1[i] == num2[i] else 0 for i in range(variableN)]) != 3:
            return -1
        ans = ''
        for i in range(variableN):
            if num1[i] != num2[i]:
                ans += 'x'
            else:
                ans += num1[i]
        return ans
    def init():
        '''O(pow(N,3)*pow(2,2N))'''
        tmp = [{} for i in range(variableN+1)]
        for x in mm+dd:
            tmp[bitsXORbits(num2Bits(x),'0'*variableN)][num2Bits(x)] = [x]
        ans = {variableN+1:tmp}
        for i in range(variableN,0,-1):
            ans[i] = []       
            for j in range(1,i+1):
                t1 = product(ans[i+1][j-1],ans[i+1][j])
                ans[i].append({})
                if len(ans[i+1][j-1].keys())*len(ans[i+1][j].keys()) != 0:
                    for x in t1:
                        t2 = bitsMergebits(x[0],x[1])
                        if t2 != -1:
                            ans[i][j-1][t2] = ans[i+1][j-1][x[0]] + ans[i+1][j][x[1]]
        # print(ans)
        return ans
    def aaIncludebb(aa,bb):
        '''O(pow(2,N))'''
        t1 = {}
        for x in aa:
            t1[x] = 0
        for x in bb:
            try:
                t1[x] += 1
            except:
                return False
        return True
    def show(ans,showMode=showMode):
        showModeAlgebra = list(map(chr, range(65, 91)))
        if showMode > 0 and showMode <= 4 :
            print('mm =',mm,'dd =',dd)
            if showMode > 2 == 0:
                showModeAlgebra = [x.lower() for x in showModeAlgebra]
            for x in ans:
                anstmp = []
                for y in x:
                    tmp = ''
                    for i in range(26):
                        try:
                            if showMode % 2 == 1:
                                if y[i] == '0':
                                    tmp += f'{showModeAlgebra[i]}`'
                                elif y[i] == '1':
                                    tmp += f'{showModeAlgebra[i]}'
                            elif showMode % 2 == 0:
                                if y[i] == '0':
                                    tmp += f'{showModeAlgebra[i]} + '
                                elif y[i] == '1':
                                    tmp += f'{showModeAlgebra[i]}`+ '
                        except:
                            if showMode % 2 == 0:
                                tmp = tmp[:-3]
                            break
                    anstmp.append(tmp)
                if showMode % 2 == 1:
                    print('-> F =','+'.join(anstmp))
                if showMode % 2 == 0:
                    print('-> F =',"("+')('.join(anstmp)+")")
    def solution():
        tmp = init()
        ans = {}
        for x in tmp:
            t1 = {}
            for y in tmp[x]:
                for z in y:
                    t1[z] = y[z]
            ans[x] = t1
        for i in range(variableN, 0, -1):
            tmp = [x for x in ans[i+1].keys()]
            for x in ans[i]:
                for y in tmp:
                    if bitsXORbits(x,y) == 0 :
                            try:
                                tt = [z for z in ans[i+1][y] if z not in dd]
                                if len(tt) == sum([1 if z in ans[i][x] else 0 for z in tt]):
                                    ans[i+1].pop(y)
                            except:
                                pass
        tmp = ans
        ans = {}
        for x in tmp:
            for y in tmp[x]:
                ans[y] = tmp[x][y]
        tmp = {}
        for x in mm:
            tmp[x] = 0
        for x in ans:
            for y in [z for z in ans[x] if z not in dd]:
                tmp[y] += 1
        t1 = {'EPI':{},'PI':{}}
        for x in ans:
            door = 0
            tt = [z for z in ans[x] if z not in dd]
            for y in tt:
                if tmp[y] == 1:
                    door = 1
                    break
            if door:
                t1['EPI'][x] = ans[x]
            else:
                if len(tt) != 0:
                    t1['PI'][x] = ans[x]
        t1['m'] = mm
        t1['d'] = dd
        rr = [x for x in t1['PI'].keys()]
        ansPI = []
        ansEPI = []
        for x in t1['EPI']:
            ansEPI += t1['EPI'][x]
        for i in range(len(rr)):
            door = 0
            for x in combinations(rr, i+1):
                tmp = [k for k in ansEPI]
                for y in x:
                    tmp += t1['PI'][y]
                if aaIncludebb(tmp,mm):
                    door = 1
                    ansPI.append(list(x))
            if door:
                break
        tmp = [x for x in t1['EPI'].keys()]
        ans = []
        for x in ansPI:
            ans.append(tmp+x)
        if len(ans) == 0:
            ans = [tmp]
        if showMode > 0:
            show(ans)
        elif showMode == 0:
            print('mm =',mm,'dd =',dd)
            for x in ans:
                print('->',x)
            print('EPI :',t1['EPI'])
            print('PI :',t1['PI'])
        return ans
    return solution()


def F(sopmm, sopdd=[]):
    '''give SOP of F, using Quine-McClusky to solve'''
    ansmm = []
    while 1:
        try:
            x = sopmm.pop()
        except:
            break
        tmp = x.find('x')
        if tmp != -1:
            for i in range(2):
                y = x
                sopmm.append(y[:tmp]+str(i)+y[tmp+1:])
        else:
            ansmm.append(int(x,base=2))
        tmp = {}
        for x in ansmm:
            tmp[x] = 1
        try:
            sopdd = [int(x,base=2) for x in sopdd]
        except:
            pass
        ansmm = [x for x in tmp.keys() if x not in sopdd]
    return QuineMcCluskey(ansmm,sopdd)
from random import sample
if __name__ == '__main__':
    QuineMcCluskey([0,1,2,3,7,8,9,10,13],[5,15])
    QuineMcCluskey([0,1,2,5,6,7,8,9,10,14])
    QuineMcCluskey([0,3,4,8,9,11,12,13],[7,14])
    F(['x100','10xx','1x1x'],['1001','1110'])