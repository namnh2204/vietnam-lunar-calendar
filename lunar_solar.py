"""
Astronomical algorithms for Vietnamese Lunar Calendar
Based on the book "Astronomical Algorithms" by Jean Meeus, 1998
Adapted from https://github.com/quangvinh86/SolarLunarCalendar
"""

import math

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ",
       "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tí", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ",
       "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
CHI_MONTH = ["", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi",
             "Thân", "Dậu", "Tuất", "Hợi", "Tí", "Sửu"]


def julian_day_from_date(dd: int, mm: int, yy: int) -> int:
    """
    Compute the (integral) Julian day number of day dd/mm/yyyy,
    i.e., the number of days between 1/1/4713 BC (Julian calendar) and dd/mm/yyyy.
    """
    temp_a = int((14 - mm) / 12.)
    temp_year = yy + 4800 - temp_a
    temp_month = mm + 12 * temp_a - 3
    julian_day = (dd + int((153*temp_month + 2) / 5.) +
                  365 * temp_year + int(temp_year / 4.) -
                  int(temp_year/100.) + int(temp_year/400)
                  - 32045)
    if julian_day < 2299161:
        julian_day = dd + int((153*temp_month + 2)/5.) \
            + 365*temp_year + int(temp_year/4.) - 32083
    return julian_day


def julian_day_to_date(julian_day: int) -> list:
    """Convert a Julian day number to day/month/year."""
    if julian_day > 2299160:
        temp_a = julian_day + 32044
        temp_b = int((4 * temp_a + 3) / 146097.)
        temp_c = temp_a - int((temp_b * 146097) / 4.)
    else:
        temp_b = 0
        temp_c = julian_day + 32082
    temp_d = int((4 * temp_c + 3) / 1461.)
    temp_e = temp_c - int((1461 * temp_d) / 4.)
    temp_m = int((5 * temp_e + 2) / 153.)
    _day = temp_e - int((153 * temp_m + 2) / 5.) + 1
    _month = temp_m + 3 - 12 * int(temp_m / 10.)
    _year = temp_b * 100 + temp_d - 4800 + int(temp_m / 10.)
    return [_day, _month, _year]


def new_moon(k_th: float) -> float:
    """
    Compute the time of the k-th new moon after the new moon
    of 1/1/1900 13:52 UCT.
    """
    time_julian = k_th / 1236.85
    time_julian_2 = time_julian * time_julian
    time_julian_3 = time_julian_2 * time_julian
    degree_to_radian = math.pi / 180
    julian_day_1 = (2415020.75933 + 29.53058868 * k_th +
                    0.0001178 * time_julian_2 -
                    0.000000155 * time_julian_3)
    julian_day_1 = (julian_day_1 +
                    0.00033*math.sin((166.56 + 132.87*time_julian -
                                      0.009173 * time_julian_2) *
                                     degree_to_radian))
    mean_new_moon = (359.2242 + 29.10535608*k_th -
                     0.0000333*time_julian_2 - 0.00000347*time_julian_3)
    sun_mean_anomaly = (306.0253 + 385.81691806*k_th +
                        0.0107306*time_julian_2 + 0.00001236*time_julian_3)
    moon_mean_anomaly = (21.2964 + 390.67050646*k_th -
                         0.0016528*time_julian_2 - 0.00000239*time_julian_3)
    moon_arg_lat = ((0.1734 - 0.000393*time_julian) *
                    math.sin(mean_new_moon*degree_to_radian) +
                    0.0021*math.sin(2*degree_to_radian*mean_new_moon))
    moon_arg_lat = (moon_arg_lat -
                    0.4068*math.sin(sun_mean_anomaly*degree_to_radian)
                    + 0.0161*math.sin(degree_to_radian*2*sun_mean_anomaly))
    moon_arg_lat = (moon_arg_lat -
                    0.0004*math.sin(degree_to_radian*3*sun_mean_anomaly))
    moon_arg_lat = (moon_arg_lat +
                    0.0104*math.sin(degree_to_radian*2*moon_mean_anomaly)
                    - 0.0051 * math.sin(degree_to_radian *
                                        (mean_new_moon + sun_mean_anomaly)))
    moon_arg_lat = (moon_arg_lat -
                    0.0074*math.sin(degree_to_radian *
                                    (mean_new_moon - sun_mean_anomaly))
                    + 0.0004*math.sin(degree_to_radian *
                                      (2*moon_mean_anomaly + mean_new_moon)))
    moon_arg_lat = (moon_arg_lat - 0.0004*math.sin(degree_to_radian *
                                                   (2*moon_mean_anomaly -
                                                    mean_new_moon))
                    - 0.0006 * math.sin(degree_to_radian *
                                        (2*moon_mean_anomaly
                                         + sun_mean_anomaly)))
    moon_arg_lat = (moon_arg_lat + 0.0010*math.sin(degree_to_radian *
                                                   (2*moon_mean_anomaly -
                                                    sun_mean_anomaly))
                    + 0.0005*math.sin(degree_to_radian *
                                      (2*sun_mean_anomaly + mean_new_moon))
                    )
    if time_julian < -11:
        deltat = (0.001 + 0.000839*time_julian + 0.0002261*time_julian_2
                  - 0.00000845*time_julian_3 -
                  0.000000081*time_julian*time_julian_3)
    else:
        deltat = -0.000278 + 0.000265*time_julian + 0.000262*time_julian_2
    new_julian_day = julian_day_1 + moon_arg_lat - deltat
    return new_julian_day


def sun_longitude(jdn: float) -> float:
    """Compute the longitude of the sun at any time."""
    time_in_julian = (jdn - 2451545.0) / 36525.
    time_in_julian_2 = time_in_julian * time_in_julian
    degree_to_radian = math.pi / 180.
    mean_time = (357.52910 + 35999.05030*time_in_julian
                 - 0.0001559*time_in_julian_2 -
                 0.00000048 * time_in_julian*time_in_julian_2)
    mean_degree = (280.46645 + 36000.76983*time_in_julian +
                   0.0003032*time_in_julian_2)
    mean_long_degree = ((1.914600 - 0.004817*time_in_julian -
                         0.000014*time_in_julian_2)
                        * math.sin(degree_to_radian*mean_time))
    mean_long_degree += ((0.019993 - 0.000101*time_in_julian) *
                         math.sin(degree_to_radian*2*mean_time) +
                         0.000290*math.sin(degree_to_radian*3*mean_time))
    long_degree = mean_degree + mean_long_degree
    long_degree = long_degree * degree_to_radian
    long_degree = long_degree - math.pi*2*(int(long_degree / (math.pi*2)))
    return long_degree


def get_sun_longitude(day_number: int, time_zone: float) -> int:
    """Compute sun position at midnight of the day."""
    return int(sun_longitude(day_number - 0.5 - time_zone / 24)
               / math.pi*6)


def get_new_moon_day(k: int, time_zone: float) -> int:
    """Compute the day of the k-th new moon in the given time zone."""
    return int(new_moon(k) + 0.5 + time_zone / 24.)


def get_lunar_month_11(yy: int, time_zone: float) -> int:
    """Find the day that starts the lunar month 11 of the given year."""
    off = julian_day_from_date(31, 12, yy) - 2415021.
    k = int(off / 29.530588853)
    lunar_month = get_new_moon_day(k, time_zone)
    sun_long = get_sun_longitude(lunar_month, time_zone)
    if sun_long >= 9:
        lunar_month = get_new_moon_day(k - 1, time_zone)
    return lunar_month


def get_leap_month_offset(a11: int, time_zone: float) -> int:
    """Find the index of the leap month after the month starting on the day a11."""
    k = int((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    last = 0
    i = 1
    arc = get_sun_longitude(get_new_moon_day(k + i, time_zone), time_zone)
    while True:
        last = arc
        i += 1
        arc = get_sun_longitude(get_new_moon_day(k + i, time_zone), time_zone)
        if not (arc != last and i < 14):
            break
    return i - 1


def solar_to_lunar(solar_dd: int, solar_mm: int, solar_yy: int, time_zone: float = 7) -> list:
    """
    Convert solar date dd/mm/yyyy to the corresponding lunar date.
    Returns: [day, month, year, is_leap_month]
    """
    day_number = julian_day_from_date(solar_dd, solar_mm, solar_yy)
    k = int((day_number - 2415021.076998695) / 29.530588853)
    month_start = get_new_moon_day(k + 1, time_zone)
    if month_start > day_number:
        month_start = get_new_moon_day(k, time_zone)
    a11 = get_lunar_month_11(solar_yy, time_zone)
    b11 = a11
    if a11 >= month_start:
        lunar_year = solar_yy
        a11 = get_lunar_month_11(solar_yy - 1, time_zone)
    else:
        lunar_year = solar_yy + 1
        b11 = get_lunar_month_11(solar_yy + 1, time_zone)
    lunar_day = day_number - month_start + 1
    diff = int((month_start - a11) / 29.)
    lunar_leap = 0
    lunar_month = diff + 11
    if b11 - a11 > 365:
        leap_month_diff = get_leap_month_offset(a11, time_zone)
        if diff >= leap_month_diff:
            lunar_month = diff + 10
        if diff == leap_month_diff:
            lunar_leap = 1
    if lunar_month > 12:
        lunar_month = lunar_month - 12
    if lunar_month >= 11 and diff < 4:
        lunar_year -= 1
    return [lunar_day, lunar_month, lunar_year, lunar_leap]


def lunar_to_solar(lunar_day: int, lunar_month: int, lunar_year: int,
                   lunar_leap_month: int, time_zone: float = 7) -> list:
    """Convert a lunar date to the corresponding solar date."""
    if lunar_month < 11:
        a11 = get_lunar_month_11(lunar_year - 1, time_zone)
        b11 = get_lunar_month_11(lunar_year, time_zone)
    else:
        a11 = get_lunar_month_11(lunar_year, time_zone)
        b11 = get_lunar_month_11(lunar_year + 1, time_zone)
    k = int(0.5 + (a11 - 2415021.076998695) / 29.530588853)
    off = lunar_month - 11
    if off < 0:
        off += 12
    if b11 - a11 > 365:
        leap_off = get_leap_month_offset(a11, time_zone)
        leap_month = leap_off - 2
        if leap_month < 0:
            leap_month += 12
        if lunar_leap_month != 0 and lunar_month != leap_month:
            return [0, 0, 0]
        elif lunar_leap_month != 0 or off >= leap_off:
            off += 1
    month_start = get_new_moon_day(k + off, time_zone)
    return julian_day_to_date(month_start + lunar_day - 1)


def day_in_week(solar_dd: int, solar_mm: int, solar_yy: int, viet_language: int = 1) -> str:
    """Get day in week."""
    julian_day = julian_day_from_date(solar_dd, solar_mm, solar_yy)
    date_index = julian_day % 7
    if viet_language:
        _day_in_week = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5",
                        "Thứ 6", "Thứ 7", "Chủ nhật"]
    else:
        _day_in_week = ["Mon", "Tue", "Wed", "Thu",
                        "Fri", "Sat", "Sun"]
    return _day_in_week[date_index]


def zodiac_year(year: int) -> str:
    """Find year in CAN-CHI (zodiac) name."""
    can_index = (year + 6) % 10
    chi_index = (year + 8) % 12
    return "{} {}".format(CAN[can_index], CHI[chi_index])


def zodiac_day(solar_dd: int, solar_mm: int, solar_yy: int) -> str:
    """Find day in CAN-CHI (zodiac) name."""
    julian_day = julian_day_from_date(solar_dd, solar_mm, solar_yy)
    can_index = (julian_day + 9) % 10
    chi_index = (julian_day + 1) % 12
    return "{} {}".format(CAN[can_index], CHI[chi_index])


def zodiac_month(month: int, year: int) -> str:
    """Month in CAN-CHI name."""
    can_index = (year * 12 + month + 3) % 10
    return "{} {}".format(CAN[can_index], CHI_MONTH[month])
