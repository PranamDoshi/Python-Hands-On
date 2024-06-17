from pytest import fail

p = int(input())
cnt = 0
for i in range(p):
    lst = list(map(int, input().split()))
    if len(list(filter(lambda x: x == 1, lst))) >= 2:
        cnt = cnt + 1

print(cnt)


def codeForce_sol(arr, n, d):
    fail = False
    res = 0
    used = [False] * n

    for i in range(n):
        if used[i]:
            continue
        
        cur = i
        pref = 0
        iter = 0
        last = 0
        ans = 0

        while True:
            if cur == i:
                break

            used[cur] = True
            
            if arr[cur] == 0:
                ans = max(ans, last)
                last = 0
            else:
                last += 1
                if iter == pref:
                    pref += 1
            
            cur = (cur + d) % n
            iter += 1
        
        if iter != pref:
            ans = max(ans, pref + last)
        else:
            fail = True
            break

        res = max(res, ans)
    
    if fail:
        return -1
    else:
        return res