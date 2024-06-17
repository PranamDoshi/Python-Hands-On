#import time


def same_array(arr, arr2, n):
    for i in range(n):
        if arr[i] != arr2[i]:
            return False
    return True


def all_zero(arr, n):
    for i in range(n):
        if arr[i] == 1:
            return False
    return True


def shift_array(arr, n, d):
    arr2 = []
    
    for i in range(n):
        arr2.append(arr[(i + n - d) % n])
    
    return arr2


def bitwiseEnd_array(arr, arr2):
    out_process = []

    for i in range(len(arr)):
        out_process.append(arr[i] & arr2[i])
    
    return out_process


def process(arr, n, d):
    step_count = 0

    while True:
        step2_arr = []

        # step1_arr = shift_array(arr, n, d)
        # step2_arr = bitwiseEnd_array(arr, step1_arr)
        step2_arr = [(arr[i] & arr[(i + n - d) % n]) for i in range(n)]
        step_count += 1

        print(arr, '\n', step2_arr, '\n', step_count, '\n')

        if all_zero(step2_arr, n):
            break
        elif same_array(arr, step2_arr, n):
            step_count = -1
            break
        else:
            arr = step2_arr
    
    return step_count


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

            if cur == i:
                break
        
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


#def main():
T = int(input())
#t1 = time.time()

for i in range(T):
    n, d = list(map(int, input().split()))
    input_arr = list(map(int, input().split()))
    assert n == len(input_arr)
    
    print(codeForce_sol(input_arr, n, d))
    # if not all_zero(input_arr, n):
    #     print(process(input_arr, n, d))
    # else:
    #     print(0)

#print((time.time() - t1))


# if __name__ == "__main__":
#     main()

#include <bits/stdc++.h>
"""
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n, d;
        cin >> n >> d;
        vector<int> a(n);
        for (int i = 0; i < n; i++)
            cin >> a[i];
        vector<bool> used(n, false);
        bool fail = false;
        int res = 0;
        for (int i = 0; i < n; i++) {
            if (used[i])
                continue;
            int cur = i, pref = 0, last = 0, iter = 0, ans = 0;
            do {
                used[cur] = true;
                if (a[cur] == 0) {
                    ans = max(ans, last);
                    last = 0;
                } else {
                    last++;
                    if (iter == pref) {
                        pref++;
                    }
                }
                cur = (cur + d) % n;
                iter++;
            } while (cur != i);
            if (iter != pref)
                ans = max(ans, pref + last);
            else {
                fail = true;
                break;
            }
            res = max(res, ans);
        }
        if (fail)
            cout << "-1\n";
        else
            cout << res << '\n';
    }
}
"""