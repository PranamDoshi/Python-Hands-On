"""
https://codeforces.com/problemset/problem/250/A
"""

def paper_work_splitter(profile_loss_of_last_days: list[int])-> list[int]:
    folders = []

    curr_folder, loss_days = [], 0
    for profit_or_loss in profile_loss_of_last_days:

        if profit_or_loss < 0:
            if loss_days == 2:
                folders.append(curr_folder)
                loss_days = 1
                curr_folder = []

            else:
                loss_days += 1

        curr_folder.append(profit_or_loss)
        # print(folders, curr_folder, loss_days)

    if curr_folder:
        folders.append(curr_folder)

    return folders

if __name__ == "__main__":
    days_of_work = int(input())
    profit_loss_of_last_days = list(map(int, input().split(' ')))

    separated_folders = paper_work_splitter(profit_loss_of_last_days)
    print(len(separated_folders))
    print(' '.join([str(len(folder)) for folder in separated_folders]))
