snafu_to_dec = {'=':-2, '-':-1, '0': 0, '1': 1, '2': 2}

def to_snafu(dec):
    rem = dec % 5
    dec = dec // 5
    base5 = [rem]
    while dec != 0:
        rem = dec % 5
        dec = dec // 5
        base5.append(rem)

    snafu = ""
    carry = 0
    base5_to_snafu = {0:'0', 1:'1', 2:'2', 3:'=', 4:'-', 5:'0'}
    for num in base5:
        num = num + carry
        snafu = base5_to_snafu[num] + snafu
        if num < 3:
            carry = 0
        else:
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

    print(f"Part 1: {to_snafu(total)} - Merry Christmas!!")
