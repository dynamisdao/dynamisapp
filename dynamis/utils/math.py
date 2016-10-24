def approximately_equal(first_num, second_num, dispersion_value):
    if first_num == second_num:
        return True
    elif first_num > second_num and ((first_num - second_num) <= dispersion_value):
        return True
    elif second_num > first_num and ((second_num - first_num) <= dispersion_value):
        return True
    return False
