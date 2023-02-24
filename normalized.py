#distances = [0, 0, 0, 0, 1, 2, 0, 1, 3, 0, 3, 3, 2, 4, 3, 2, 1, 0]
distances = [0, 0, 0, 1, 0, 1]
max = -1
min = -1
for distance in distances:
    print("distance: ", distance)

    if distance > 0:
        if max <= 0:
            max = distance
            min = distance
        if distance > max:
            max = distance
        if distance < min:
            min = distance
    print("max: ", max)
    print("min: ", min)
    if distance > 0:
        normalized_d = 1
        if (max != min):
            normalized_d = (distance - min)/(max - min)
    else:
        normalized_d = 0
    print("Normalize distance: ", normalized_d)
    print("=====================================")