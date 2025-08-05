import os

p1, p2, p3 = [], [], []
foam_gen_dir = 'C:/Users/jacke/PycharmProjects/foam_gen/Data/user_data'
for dir in os.walk(foam_gen_dir):
    if 'physical1' in dir:
        p1.append(dir[0])
    elif 'physical2' in dir[0]:
        p2.append(dir)
    elif 'physical3' in dir[0]:
        p3.append(dir)