snafu_to_dec = {'=':-2, '-':-1, '0': 0, '1': 1, '2': 2}

def to_snafu(dec):
    rem = dec % 5
    dec = dec // 5
    base5 = [str(rem)]
    while dec != 0:
        rem = dec % 5
        dec = dec // 5
        base5.append(str(rem))

    snafu = ""
    carry = 0
    for num in base5:
        num = int(num) + carry
        if int(num) < 3:
            snafu = str(num) + snafu
            carry = 0
        elif int(num) == 3:
            snafu = "=" + snafu
            carry = 1
        elif int(num) == 4:
            snafu = "-" + snafu
            carry = 1
        elif int(num) == 5:
            snafu = "0" + snafu
            carry = 1

    return snafu

def to_dec(snafu):
    num = [*snafu]
    a = num.pop()
    pow = 0
    total = snafu_to_dec[a]*(5**pow)
    while len(num) > 0:
        pow += 1
        a = num.pop()
        total += snafu_to_dec[a]*(5**pow)
    return total
    
with open('input.txt') as f:
    total = 0
    for line in f.readlines():
        line = line.strip()
        total += to_dec(line)

    print(f"Part 1: {to_snafu(total)} Merry Christmas!!")
