from ProccessTurnoverTest import proccess_turnover_test

class Stats:
    def __init__(this):
        this.fn = 0
        this.fp = 0
        this.t = 0
        this.f = 0
        this.o = 0

def assert_equals(expected, result, stat):
    print("Expected ", expected, " got ", result)

    if expected[0] is True and result[0] is False:
        stat.fn = stat.fn + 1 # false negative
    if expected[0] is False and result[0] is True:
        stat.fp = stat.fp + 1 # false positive
    if expected[0] is False and result[0] is False:
        stat.f = stat.f + 1
        
    if expected[0] is True and result[0] is True:
        if expected[1] != result[1]: # other - mislabeled 
            stat.o = stat.o + 1
        else:
            stat.t = stat.t + 1

    return stat
    

stats = Stats() 
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_1.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_2.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_3.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_4.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_5.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_6.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_7.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_8.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_9.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_10.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_11.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_12.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_13.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_14.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_15.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_16.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_17.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_18.mp4'), stats)

stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_fake_19.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_fake_20.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_fake_21.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_fake_22.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_fake_23.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/dribble_fake_24.mp4'), stats)

stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/not_double_dribble_1.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/not_double_dribble_2.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/not_double_dribble_3.mp4'), stats)
stats = assert_equals((False, 1), proccess_turnover_test('vids/videos/not_double_dribble_4.mp4'), stats)

stats = assert_equals((True, 0), proccess_turnover_test('vids/videos/travel_1.mp4'), stats)
stats = assert_equals((True, 0), proccess_turnover_test('vids/videos/travel_2.mp4'), stats)
stats = assert_equals((True, 0), proccess_turnover_test('vids/videos/travel_3.mp4'), stats)
stats = assert_equals((True, 0), proccess_turnover_test('vids/videos/travel_4.mp4'), stats)
stats = assert_equals((True, 0), proccess_turnover_test('vids/videos/travel_5.mp4'), stats)
stats = assert_equals((True, 0), proccess_turnover_test('vids/videos/travel_6.mp4'), stats)
stats = assert_equals((True, 0), proccess_turnover_test('vids/videos/travel_7.mp4'), stats)
stats = assert_equals((True, 0), proccess_turnover_test('vids/videos/travel_8.mp4'), stats)
stats = assert_equals((True, 0), proccess_turnover_test('vids/videos/travel_9.mp4'), stats)
stats = assert_equals((True, 0), proccess_turnover_test('vids/videos/travel_10.mp4'), stats)
stats = assert_equals((True, 0), proccess_turnover_test('vids/videos/travel_11.mp4'), stats)
stats = assert_equals((True, 0), proccess_turnover_test('vids/videos/travel_12.mp4'), stats)


stats = assert_equals((True, 1), proccess_turnover_test('vids/videos/double_dribble_1.mp4'), stats)
stats = assert_equals((True, 1), proccess_turnover_test('vids/videos/double_dribble_2.mp4'), stats)
stats = assert_equals((True, 1), proccess_turnover_test('vids/videos/double_dribble_3.mp4'), stats)
stats = assert_equals((True, 1), proccess_turnover_test('vids/videos/double_dribble_4.mp4'), stats)
stats = assert_equals((True, 1), proccess_turnover_test('vids/videos/double_dribble_5.mp4'), stats)
stats = assert_equals((True, 1), proccess_turnover_test('vids/videos/double_dribble_6.mp4'), stats)
stats = assert_equals((True, 1), proccess_turnover_test('vids/videos/double_dribble_7.mp4'), stats)
stats = assert_equals((True, 1), proccess_turnover_test('vids/videos/double_dribble_throw_8.mp4'), stats)
stats = assert_equals((True, 1), proccess_turnover_test('vids/videos/double_dribble_9.mp4'), stats)
stats = assert_equals((True, 1), proccess_turnover_test('vids/videos/double_dribble_throw_10.mp4'), stats)
stats = assert_equals((True, 1), proccess_turnover_test('vids/videos/double_dribble_throw_11.mp4'), stats)
stats = assert_equals((True, 1), proccess_turnover_test('vids/videos/double_dribble_throw_12.mp4'), stats)
stats = assert_equals((True, 1), proccess_turnover_test('vids/videos/double_dribble_throw_13.mp4'), stats)


print("fn", stats.fn, "fp", stats.fp, "t", stats.t, "f", stats.f, "o", stats.o)