# #Write your code here
# import pandas as pd
# import numpy as np


# heights_A = pd.Series([176.2, 158.4, 167.6, 156.2, 161.4], ['s1', 's2', 's3', 's4', 's5'])
# print(heights_A.shape)


# weights_A = pd.Series([85.1, 90.2, 76.8, 80.4, 78.9], ['s1', 's2', 's3', 's4', 's5'])
# print(weights_A.dtype)


# df_A = pd.DataFrame([heights_A, weights_A], columns = ['Student_height', 'Student_weight'])
# print(df_A.shape)



# np.random.seed(100)
# heightArr_B = 25.0*np.random.randn(5) + 170.0
# heights_B = pd.Series(heightArr_B, ['s1', 's2', 's3', 's4', 's5'])
# np.random.seed(100)
# weightArr_B =  12.0*np.random.randn(5) + 75.0
# weights_B = pd.Series(weightArr_B, ['s1', 's2', 's3', 's4', 's5'])
# print(round(heights_B.mean(axis = 0), 2))
# #print(heights_B.mean(axis = 0))


# df_B = pd.DataFrame({'Student_height' : heights_B, 'Student_weight' : weights_B})
# print(list(df_B.columns))
# import re
# from collections import defaultdict

# """
# Input:
# n = 3
# m = 6
# 0:start:0
# 1:start:3
# 1:end:6
# 2:start:8
# 2:end:10
# 0:end:12
# """

# if __name__ == "__main__":
#     number_of_functions = int(re.findall(r"n\s*=\s*\d+", input().strip(), re.I)[0].split('=')[1].strip())
#     number_of_instructions = int(re.findall(r"m\s*=\s*\d+", input().strip(), re.I)[0].split('=')[1].strip())

#     index = 0
#     # inProgress, timings, lastTimeStamps = set(), defaultdict(dict), 0
#     inProgress, funcStack, runningFuncBySecond = set(), [], defaultdict(int)
#     count = 0
#     while index < number_of_instructions:
#         instruction = re.findall(r"(\d+:start:\d+|\d+:end:\d+)", input().strip(), re.I)[0]

#         funcId, startOrEnd, timestamp = instruction.split(':')
#         print(funcId, startOrEnd, timestamp)

#         if startOrEnd == 'start':
#             funcStack.append((funcId, timestamp))

#         elif startOrEnd == 'end':
#             if funcStack and funcStack[-1] == funcId:
#                 funcStartTime = int(funcStack.pop(len(funcStack)-1)[0])
#                 runningFuncBySecond[funcId] = (int(timestamp) - funcStartTime) + 1
#                 count += runningFuncBySecond[funcId]

        # if startOrEnd == 'start':
        #     inProgress.add(funcId)

        # elif startOrEnd == 'end':
        #     inProgress.remove(funcId)

# def maxMeetings(effectiveness):

#     effectiveness.sort()
#     effectiveness = reversed(effectiveness)
    
#     current_index = 0
#     max_meetings = 0
    
#     for value in effectiveness:
#         if current_index + value > 0:
#             current_index += value
#             max_meetings += 1
#         else:
#             break
    
#     return max_meetings

# if __name__ == "__main__":
#     print(maxMeetings([1, 3, 5, 10, -3, -5, -10, -20]))

if __name__ == "__main__":

    def getTotalExecutionTime(n, logs):
        # Initialize the results list for each function's execution time
        execution_times = [0] * n
        
        # Stack to keep track of the current function and its start time
        stack = []
        
        # To keep track of the previous timestamp
        prev_timestamp = 0
        
        for log in logs:
            # Parse the log entry
            function_id, event, timestamp = log.split(':')
            function_id = int(function_id)
            timestamp = int(timestamp)
            
            if event == 'start':
                # If stack is not empty, it means there is a function currently executing
                if stack:
                    # Accumulate the time of the currently executing function
                    executing_function_id, _ = stack[-1]
                    print(executing_function_id, timestamp - prev_timestamp - 1)
                    execution_times[executing_function_id] += timestamp - prev_timestamp - 1

                # Push the current function onto the stack with its start time
                stack.append((function_id, timestamp))
                prev_timestamp = timestamp
            
            elif event == 'end':
                # Pop the function from the stack
                executing_function_id, start_time = stack.pop()
                # Calculate the execution time for the function
                execution_times[executing_function_id] += timestamp - prev_timestamp + 1
                prev_timestamp = timestamp

            print(execution_times, stack, timestamp, prev_timestamp)
        
        return execution_times
    
    def calculate_durations(intervals):
        # Initialize a dictionary to hold start and end times
        times = {}
        
        # Process the intervals
        for interval in intervals:
            # Split each interval into its components
            parts = interval.split(':')
            item_id = int(parts[0])
            type_of_interval = parts[1]
            time = int(parts[2])
            
            if item_id not in times:
                times[item_id] = {'start': None, 'end': None}
            
            if type_of_interval == 'start':
                times[item_id]['start'] = time
            elif type_of_interval == 'end':
                times[item_id]['end'] = time
        
        # Calculate durations
        durations = []
        for item_id in sorted(times.keys()):
            start = times[item_id]['start']
            end = times[item_id]['end']
            if start is not None and end is not None:
                durations.append(end - start)
        
        return durations
    
    print(getTotalExecutionTime(3, ["0:start:0", "1:start:3", "1:end:6", "2:start:8","2:end:10", "0:end:12"]))
    # print(calculate_durations(["0:start:0", "2:start:4", "2:end:5", "1:start:7","1:end:10", "0:end:11"]))
