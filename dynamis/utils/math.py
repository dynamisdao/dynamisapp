def approximately_equal(first_num, second_num, dispersion_value):
    if first_num == second_num:
        return True
    elif first_num > second_num:
        min_value = first_num - first_num * dispersion_value
        if second_num >= min_value:
            return True
    elif second_num > first_num:
        min_value = second_num - second_num * dispersion_value
        if first_num >= min_value:
            return True
    return False
