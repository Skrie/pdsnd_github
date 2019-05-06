import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
DAYS = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

def line_seperator():
    """
    Prints a line of semi-colons as a seperation line in the termonal output.
    """
    print('-'*40)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Enter a city name, we have data for Chicago, New York City and Washington: ')
        if city.lower() not in CITY_DATA.keys():
            print('Sorry please enter a valid city. Either Chicago, New York City or Washington')
            continue
        else:
            print('You selected {}'.format(city))
            break    

    # get user input for the month (all, january, february, ... , june)
    while True:
        month = input('Enter a month, you can select any month between January and June. Enter All to select all months: ')
        if month.lower() not in MONTHS:
            print('Sorry please enter a valid month.')
            continue
        else:
            print('You selected {}'.format(month))
            break
    
    # get user input for the day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Enter a day, you can select any day between Monday and Sunday. Enter All to select all days: ')
        if day.lower() not in DAYS:
            print('Sorry please enter a valid day.')
            continue
        else:
            print('You selected {}'.format(day))
            break

    line_seperator()
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day_Of_Week'] = df['Start Time'].dt.weekday_name

    # filter by the month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month.lower())

        # filter by the month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day_Of_Week'] == day.title()]
    return df.interpolate(method='linear', axis=0)


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['Month'].value_counts().index[0]
    print('The most common month of travel is {}.'.format(MONTHS[common_month].title()))    

    # display the most common day of week
    common_week_day = df['Day_Of_Week'].value_counts().index[0]
    print('The most common day of travel is {}.'.format(common_week_day))

    # display the most common start hour
    common_start_hour = df['Start Time'].dt.hour.value_counts().index[0]
    print('The most common hour of travel is {}:00.'.format(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    line_seperator()


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts()
    print('The most commonly used start station is {} with {} starts.'.format(start_station.index[0], start_station[0]))

    # display most commonly used end station
    end_station = df['End Station'].value_counts()
    print('The most commonly used end station is {} with {} endings.'.format(end_station.index[0], end_station[0]))

    # display most frequent combination of start station and end station trip
    start_end_station = (df['Start Station'] + ' and ' + df['End Station']).value_counts()
    print('The most frequent combination of start and end station is {} with {} beginnings and endings'.format(start_end_station.index[0], start_end_station[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    line_seperator()


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Time Spent'] = (df['End Time'] - df['Start Time'])
    print('The total time travelled is {}'.format(df['Time Spent'].sum()))

    # display mean travel time
    print('The mean time travelled is {}'.format(df['Time Spent'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    line_seperator()


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print('The counts of user types in the data are')
    print(user_type_counts)

    # Display counts of gender
    try:
        gender_type_counts = df['Gender'].value_counts()
        print('The counts of gender types in the data are: {}'.format(gender_type_counts))
    except KeyError as e:
        print('{} does not exist in this dataset and hence no analysis has been done.'.format(e))
        
    # Display earliest, most recent, and most common year of birth
    try:
        print('The earliest birth year is {}.'.format(int(df['Birth Year'].min())))
        print('The most recent birth year is {}.'.format(int(df['Birth Year'].max())))
        common_birth_year_count = int(df['Birth Year'].value_counts().index[0])
        print('The most common birth year is {}.'.format(common_birth_year_count))
    except KeyError as e:
        print('{} does not exist in this dataset and hence no analysis has been done.'.format(e))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    line_seperator()

def user_raw_output(df):
    """Displays statistics on the total and average trip duration."""

    """
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    b = 0
    while True:
        user_input = input('Would you like to see 5 lines of raw data?: ')
        if user_input.lower() == 'yes':
            for _ in range(5):
                print(df.iloc[b])
                b += 1
            continue
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        user_raw_output(df)
        station_stats(df)
        user_raw_output(df)
        trip_duration_stats(df)
        user_raw_output(df)
        user_stats(df)
        user_raw_output(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
