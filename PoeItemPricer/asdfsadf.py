

s = "~price 60 chaos"

x = s.strip('~price ').split(' ', 1)[0]

print(x)
