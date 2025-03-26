# numbers = range(10)
sda_pins = {n: 255 for n in range(0, 21, 2)}
sda_pins[26] = 255

scl_pins = {n: 255 for n in range(1, 22, 2)}
scl_pins[27] = 255

print('a')
