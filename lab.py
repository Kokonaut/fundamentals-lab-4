def get_distance_to_goal(monster):
    diff_x = abs(monster.x - monster.dest_x)
    diff_y = abs(monster.y - monster.dest_y)
    return (diff_x ** 2 + diff_y ** 2) ** 0.5


def get_remaining_monster_health(monster):
    return monster.current_health

# ------------------ Lab Small ---------------------


def lab_run_small(monsters):
    pass

# ------------------ Lab Med ---------------------


def lab_run_med(monsters):
    pass

# ------------------ Lab Big ---------------------


def lab_run_big_1(monsters):
    pass


def lab_run_big_2(monsters):
    pass


def lab_run_big_3(monsters):
    pass


def lab_run_big_4(monsters):
    pass
