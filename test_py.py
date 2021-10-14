# ((ab){3}(cd){2}){4}
# (((ab){3}c){3}cd){3}
arr = '(ab){2}(cd){3}'
main = ''
i = 0
while i < len(arr):
    if arr[i] == ')':
        j = i - 1
        stri = ''
        while arr[j] != '(':
            stri += arr[j]
            j-=1
        stri = stri[::-1]
        j = i+2
        k= 0
        while j != '}':
            try:
                k = k*10 + int(arr[j])
                j+=1
            except:
                break
        print(k,stri)
        strrep = stri*k
        arr = arr.replace('(' + stri + ')',strrep,1)
        arr = arr.replace('{' + str(k) + '}','',1)
    else:
        print(i)
        i+=1
print(arr)
        