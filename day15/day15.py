def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2 
    return abs(x2-x1) + abs(y2-y1)

def union(intervals):
    merged_intervals = []
    for begin,end in sorted(intervals):
        if merged_intervals and merged_intervals[-1][1] >= begin - 1:
            merged_intervals[-1][1] = max(merged_intervals[-1][1], end)
        else:
            merged_intervals.append([begin, end])
    return merged_intervals

with open('input.txt') as f:
    sensor_to_beacon = {}
    beacons = set()
    sensors = set()
    for line in f.readlines():
        line = line.strip()
        sensor, at, xs, ys, closest, beacon, be, at, xb, yb = line.split(" ")
        xs = int(xs.split("=")[1].strip(","))
        ys = int(ys.split("=")[1].strip(":"))
        xb = int(xb.split("=")[1].strip(","))
        yb = int(yb.split("=")[1].strip())
        sensor_to_beacon[(xs,ys)] = (xb,yb)
        beacons.add((xb,yb))
        sensors.add((xs,ys))
    
    searched = set()
    for sensor in sensors:
        xs, ys = sensor
        beacon = sensor_to_beacon[sensor]
        radius = distance(beacon, sensor)
        y_bar = 2_000_000
        if ys + radius < y_bar:
            continue
        xmin = xs - (radius - abs(y_bar-ys))
        xmax = xs + (radius - abs(y_bar-ys))

        for x in range(xmin, xmax+1):
            searched.add((x,y_bar))

    print(f"Part 1: {len(searched - beacons)}")

    y_max = 4_000_000
    for i in range(y_max + 1):
        intervals = []
        for sensor in sensors:
            xs, ys = sensor
            beacon = sensor_to_beacon[sensor]
            radius = distance(beacon, sensor)
            y_bar = i
            if y_bar > ys and ys + radius < y_bar:
                continue
            if y_bar < ys and ys - radius > y_bar:
                continue
            xmin = xs - (radius - abs(y_bar-ys))
            xmax = xs + (radius - abs(y_bar-ys))
            intervals.append((xmin,xmax))
        intervals = union(intervals)

        if len(intervals) > 1:
            print(f"Part 2: {intervals[0][1]*y_max + i}")
            break
    
    