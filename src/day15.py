from src.utils import print_ans, read_aoc, AOCFILE, Coordinate


aoc_file = list(read_aoc(15, use_test_data=True))

def get_sensor_beacon(aoc_file:list[str]) -> tuple[list[Coordinate], list[Coordinate]]:
    sensor:list[Coordinate] = []
    beacon:list[Coordinate] = []
    for line in aoc_file:
        sensor_part, beacon_part = line.split(":")
        raw_sensor_x, raw_sensor_y = sensor_part.split("at")[1].split(",")
        raw_beacon_x, raw_beacon_y = beacon_part.split("at")[1].split(",")
        sensor.append(Coordinate(x = int(raw_sensor_x.replace("x=", "")), y = int(raw_sensor_y.replace("y=", ""))))
        beacon.append(Coordinate(x = int(raw_beacon_x.replace("x=", "")), y = int(raw_beacon_y.replace("y=", ""))))
    return sensor, beacon

def get_distance(a:Coordinate, b:Coordinate) -> int:
    return int(abs(a.x - b.x) + abs(a.y - b.y))

def combine_range(tangent_list:[list[tuple[int, int]]]) -> list[tuple[int, int]]:
    min, max = 0, 0
    whole_list =
    for tmin, tmax in tangent_list:
        if tmin < min:
            min = tmin
        if tmax > max:
            max = tmax


def get_tangent_points(sensor:Coordinate, radius:int, target:int) -> tuple[int, int]:
    sensor_y = sensor.y
    if sensor_y + radius < target or sensor_y - radius > target:
        return (0, 0)
    dist = sensor_y - target if sensor_y > target else target - sensor_y
    points = radius - dist
    return (int(sensor.x - points), int(sensor.x + points))


def Q1():
    sensor, beacon = get_sensor_beacon(aoc_file=aoc_file)
    all_point = set()
    for s, b in zip(sensor, beacon):
        print(get_tangent_points(s, get_distance(s,b), 10))


if __name__ == "__main__":
    Q1()
