import math

yes = [(0.46, 1), (0.376, 1), (0.264, 1), (0.318, 1), (0.215, 1), (0.237, 1),
       (0.149, 1), (0.211, 1)]
yes = [e[0] for e in yes]
no = [0.091, 0.267, 0.057, 0.099, 0.161, 0.198, 0.37, 0.042, 0.103]
cc = {}
for y in yes:
    cc[y] = 1
for n in no:
    cc[n] = 0

total = yes + no
total.sort()

min_ent, cut_point = math.inf, 0

for i in range(1, len(total)):
    bar = (total[i] + total[i-1])/2
    left_yes = sum(cc[total[j]] for j in range(i)) / i
    left_no = 1 - left_yes
    right_yes = sum(cc[total[j]] for j in range(i, len(total))) / (len(total) - i)
    right_no = 1 - right_yes
    # print(i, left_yes, left_no, right_yes, right_no)
    left_ent = 0 if left_yes * left_no == 0 else -left_yes * math.log(left_yes, 2) - left_no * math.log(left_no, 2)
    right_ent = 0 if right_yes * right_no == 0 else -right_yes * math.log(right_yes, 2) - right_no * math.log(right_no, 2)
    ent = (left_ent * i + right_ent * (len(total) - i)) / len(total)
    if ent < min_ent:
        min_ent = ent
        cut_point = bar
    print(bar, ent)

print(f"切分点位于 {cut_point}")
