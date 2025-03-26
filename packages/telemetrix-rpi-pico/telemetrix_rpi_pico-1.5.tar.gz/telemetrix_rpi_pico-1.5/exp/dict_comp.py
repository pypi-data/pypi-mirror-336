# numbers = range(10)
new_dict_comp = {n: 255 for n in range(23)}
# new_dict_comp = {n:255 for n in numbers if n%2 == 0}
new_dict_comp[26] = 255
for n in range(26, 29):
    new_dict_comp[n]=255

print(new_dict_comp)