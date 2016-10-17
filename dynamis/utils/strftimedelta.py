def timedelta_to_str_years_days(time_delta):
    years, days = divmod(time_delta.days, 365)
    months, days = divmod(days, 30)
    formatted_duration = ''
    if years:
        if years >= 2:
            formatted_duration += "{} years ".format(years)
        elif years == 1:
            formatted_duration += "{} year ".format(years)
    if months:
        if months >= 2:
            formatted_duration += "{} months".format(months)
        elif months == 1:
            formatted_duration += "{} month".format(months)
    return formatted_duration
