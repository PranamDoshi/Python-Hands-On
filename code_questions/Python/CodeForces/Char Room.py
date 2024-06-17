inp = input().lower()

msg = ['h', 'e', 'l', 'l', 'o']

msg_idx = 0
for i in range(len(inp)):
    if inp[i] == msg[msg_idx]:
        msg_idx += 1

    if msg_idx == len(msg):
        break

if msg_idx == len(msg):
    print('YES')
else:
    print('NO')
