import datetime

from lunar_birthday_ical.lunar import get_future_lunar_equivalent_date


def test_first_day_of_gregorian_year():
    # Test case 1: First day of the Gregorian year
    solar_date = datetime.datetime(2020, 1, 1)
    age = 1
    expected_date = datetime.datetime(2021, 1, 19)
    assert get_future_lunar_equivalent_date(solar_date, age) == expected_date


def test_last_day_of_gregorian_year():
    # Test case 2: Last day of the Gregorian year
    solar_date = datetime.datetime(2020, 12, 31)
    age = 1
    expected_date = datetime.datetime(2021, 12, 20)
    assert get_future_lunar_equivalent_date(solar_date, age) == expected_date


def test_lunar_new_year_to_next_lunar_new_year():
    # Test case 3: From Lunar New Year's Day 2020 to Lunar New Year's Day 2021
    solar_date = datetime.datetime(2020, 1, 25)
    age = 1
    expected_date = datetime.datetime(2021, 2, 12)
    assert get_future_lunar_equivalent_date(solar_date, age) == expected_date


def test_last_day_of_lunar_year_to_next_last_day_of_lunar_year():
    # Test case 4: From the last day of the Lunar year 2020 to the last day of the Lunar year 2021
    solar_date = datetime.datetime(2021, 2, 11)
    age = 1
    expected_date = datetime.datetime(2022, 1, 31)
    assert get_future_lunar_equivalent_date(solar_date, age) == expected_date


def test_leap_month_to_next_leap_month():
    # Test case 5: From the first day of the leap fourth month 2020 to the first day of the fourth month 2021
    solar_date = datetime.datetime(2020, 5, 23)
    age = 1
    expected_date = datetime.datetime(2021, 5, 12)
    assert get_future_lunar_equivalent_date(solar_date, age) == expected_date


def test_utc_timezone():
    # Test case 6: UTC timezone
    solar_date = datetime.datetime(2020, 1, 25, 15, 30, tzinfo=datetime.timezone.utc)
    age = 1
    expected_date = datetime.datetime(2021, 2, 12, 15, 30, tzinfo=datetime.timezone.utc)
    assert get_future_lunar_equivalent_date(solar_date, age) == expected_date


def test_different_timezone():
    # Test case 7: Different timezone
    solar_date = datetime.datetime(
        2020, 1, 25, 15, 30, tzinfo=datetime.timezone(datetime.timedelta(hours=8))
    )
    age = 1
    expected_date = datetime.datetime(
        2021, 2, 12, 15, 30, tzinfo=datetime.timezone(datetime.timedelta(hours=8))
    )
    assert get_future_lunar_equivalent_date(solar_date, age) == expected_date


def test_large_age_increment():
    # Test case 8: Large age increment
    solar_date = datetime.datetime(2000, 1, 1)
    age = 20
    expected_date = datetime.datetime(2019, 12, 20)
    assert get_future_lunar_equivalent_date(solar_date, age) == expected_date


def test_negative_age_increment():
    # Test case 9: Negative age increment
    solar_date = datetime.datetime(2020, 1, 25)
    age = -1
    expected_date = datetime.datetime(2019, 2, 5)
    assert get_future_lunar_equivalent_date(solar_date, age) == expected_date
