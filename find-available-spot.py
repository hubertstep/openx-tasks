import sys
import getopt, os
from datetime import datetime, timedelta, time


def get_calendar_data(arg_calendar: str, min_people: str) -> dict:
    min_people = int(min_people)
    calendars_dict = {}
    current_dir = os.getcwd()
    directory = current_dir + arg_calendar
    filenames = os.listdir(directory)
    filenames = list(filter(lambda s: s[-3:] == 'txt', filenames))

    if len(filenames) == 0:
        raise Exception('No calendars in given directory')
    if len(filenames) < min_people:
        raise Exception('There are not enough calendars in directory. Their amount is smaller than minimum people '
                        'needed')

    for filename in filenames:
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding="utf8") as file:
            lines = file.readlines()
            for count, line in enumerate(lines):
                line = line.replace('\n', '')
                lines[count] = line.split(' - ')
            calendars_dict[filename] = lines

    return calendars_dict


def string_to_datetime(calendar_dict: dict):
    for key, value in calendar_dict.items():
        date_list = []
        for line in value:
            if len(line) == 1:
                date = datetime.strptime(line[0], '%Y-%m-%d')
                date_list.append(date)
            elif len(line) == 2:
                start_date = datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S')
                end_date = datetime.strptime(line[1], '%Y-%m-%d %H:%M:%S')
                date_list.append((start_date, end_date))
            else:
                raise ValueError('Wrong format file')
        calendar_dict[key] = date_list
    return calendar_dict


def employee_availability(possible_date, free_dates_dict, employee_key, duration_in_min):
    availability = []
    date_tuple = ()
    for date in free_dates_dict[employee_key]:
        if date[0].date() == possible_date:
            date_tuple = date
    if len(date_tuple) == 0:
        return [None, None]
    day_end = datetime.combine(date_tuple[0].date(), datetime.max.time())
    day_begin = datetime.combine(date_tuple[0].date(), datetime.min.time())
    if date_tuple[0] - day_begin > timedelta(minutes=duration_in_min):
        availability.append(date_tuple[0] - timedelta(minutes=duration_in_min))
    else:
        availability.append(None)
    if day_end - date_tuple[1] > timedelta(minutes=duration_in_min):
        availability.append(date_tuple[1])
    else:
        availability.append(None)

    return availability


def find_closest_timeslot(calendar_dict: dict, duration: str = '120', min_people: str = '2'):
    duration_in_min = int(duration)
    min_people = int(min_people)
    current_date = datetime.now()
    first_free_date = current_date
    free_dates = {}
    for name, dates in calendar_dict.items():
        free_dates[name] = list(filter(lambda d: type(d) is tuple, dates))

    all_possible_dates = []

    for date_list in free_dates.values():
        for date in date_list:
            if date[0] >= current_date:
                all_possible_dates.append(date[0].date())

    all_possible_dates = sorted(all_possible_dates)
    dates_with_enough_employees = []
    for date in all_possible_dates:
        if all_possible_dates.count(date) >= min_people:
            dates_with_enough_employees.append(date)

    dates_with_enough_employees = list(dict.fromkeys(dates_with_enough_employees))
    dates_with_enough_employees = sorted(dates_with_enough_employees)

    for possible_date in dates_with_enough_employees:
        availability = []
        for employee in free_dates.keys():
            empl_avail = employee_availability(possible_date, free_dates, employee, duration_in_min)
            if empl_avail[0] is not None:
                availability.append(0)
            if empl_avail[1] is not None:
                availability.append(empl_avail[1])
        if availability.count(0) >= min_people:
            return datetime.combine(possible_date, datetime.min.time())
        else:
            availability = list(filter(lambda e: e != 0, availability))
            availability = sorted(availability, reverse=True)
            if len(availability) >= min_people:
                return availability[0]
    else:
        raise Exception('There is no date described by calendars that suits given conditions')


def get_params(argv):
    arg_calendar = ""
    arg_duration = ""
    arg_minimum_people = ""
    arg_help = "{0} -c <calendars> -d <duration-in-minutes> -m <minimum-people>".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hc:d:m:",
                                   ["help", "calendars=", "duration-in-minutes=", "minimum-people="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)
            sys.exit(2)
        elif opt in ("-c", "--calendars"):
            arg_calendar = arg
        elif opt in ("-d", "--duration-in-minutes"):
            arg_duration = arg
        elif opt in ("-m", "--minimum-people"):
            arg_minimum_people = arg

    return arg_calendar, arg_duration, arg_minimum_people


if __name__ == '__main__':
    calendars, duration, min_people = get_params(sys.argv)
    data = get_calendar_data(calendars, min_people)
    date_data = string_to_datetime(data)
    print(find_closest_timeslot(date_data, duration, min_people))
