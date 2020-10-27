import random
import time

# set variables
x_min           = 1
x_max           = 10
step_min        = 5
step_max        = 10
x               = x_max
#
x_step_num      = int(random.uniform(step_min, step_max))
x_target        = random.uniform(x_min, x_max)
x_step          = (x_target - x) / x_step_num
step_count      = 0

while True:
    # debug
    print("x = {}\tto {}\tstep {} / {}".format(x, x_target, step_count, x_step_num))

    # perform step
    x += x_step
    step_count += 1

    # if we arrived at destination, reset target
    if(step_count == x_step_num + 1) :
        x           = x_target
        x_step_num  = int(random.uniform(step_min, step_max))
        x_target    = random.uniform(x_min, x_max)
        x_step      = (x_target - x) / x_step_num
        step_count = 0

    #
    time.sleep(0.5)
