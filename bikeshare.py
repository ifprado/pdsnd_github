import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def display_raw_data(df, currentFunction, listOfColumns):
    usrInput = input('Would you like to see 5 lines of raw data from {}? yes/no\n'.format(currentFunction)).lower()
    if usrInput != 'no':
        print(df[listOfColumns].sample(frac=1).head())

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please enter in one of these three cities - Chicago, New York City, Washington:\n").title()
    cities = ["Chicago", "New York City", "Washington"]
    while city not in cities:
        city = input("Sorry, please enter one of these three cities - Chicago, New York City, Washington:\n").title()
    city = city.lower().replace(" ","_")
    print(city)


    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Please enter a month or 'all' - January, February, ..., May, June or 'all':\n").title()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    while month not in months:
        month = input("Sorry, please enter a month - January, February, ..., May, June or 'all':\n").title()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please enter a day of the week - Monday, ..., Sunday or 'all' :\n") .title()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
            'Sunday', 'All']
    while day not in days:
        day = input("Sorry, please enter a day of the week - Monday, ..., Sunday or 'all':\n").title()

    print('-'*40)
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

    df = pd.read_csv(city + ".csv")
    df.columns = [c.replace(' ', '_') for c in df.columns]

    df['Start_Time'] = pd.to_datetime(df['Start_Time'])
    df['End_Time'] = pd.to_datetime(df['End_Time'])

    months = ['January', 'February', 'March', 'April', 'May', 'June']

    if month in months:
        df = df[df['Start_Time'].dt.month == (months.index(month) + 1)]



    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
            'Sunday']

    if month in months:
        df = df[df['Start_Time'].dt.day == (days.index(day) + 1)]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months = ['January', 'February', 'March', 'April', 'May', 'June']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
            'Sunday']

    # TO DO: display the most common month
    mostCommonMonth = months[df['Start_Time'].dt.month.mode()[0]-1]
    print("Most common month is {}".format(mostCommonMonth))

    # TO DO: display the most common day of week
    convert_Date_To_DayOfWeek_List = [0,0,0,0,0,0,0]
    for dateValue in df['Start_Time']:
        D = dateValue.year % 100
        forumlaConverterValue = dateValue.day + + int((13*dateValue.month-1)/5) + D + int(D/4) - 35
        forumlaConverterValueIndex = forumlaConverterValue % 7
        convert_Date_To_DayOfWeek_List[forumlaConverterValueIndex] += 1
    mostCommonDay = days[convert_Date_To_DayOfWeek_List.index(max(convert_Date_To_DayOfWeek_List))]    
    
    #mostCommonDay = days[df['Start_Time'].dt.day.mode()[0]-1]
    print("Most common day is {}".format(mostCommonDay))

    # TO DO: display the most common start hour
    mostCommonHour = df['Start_Time'].dt.hour.mode()[0]
    print("Most common hour is {} military time".format(mostCommonHour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    display_raw_data(df, 'time_stats', ['Start_Time','End_Time'])


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    mostCommonStartStation = df['Start_Station'].mode()[0]
    print("Most common start station is {}".format(mostCommonStartStation))

    # TO DO: display most commonly used end station
    mostCommonEndStation = df['End_Station'].mode()[0]
    print("Most common end station is {}".format(mostCommonEndStation))


    # TO DO: display most frequent combination of start station and end station trip
    mostCommonStartAndEndStation = (df['Start_Station'] + ', ' + df['End_Station']).mode()[0]
    print("Most common start and end station is {}".format(mostCommonStartAndEndStation))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    display_raw_data(df, 'station_stats', ['Start_Station','End_Station'])


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    totalTravelTime = df['Trip_Duration'].sum()
    print('Total travel time was {}'.format(totalTravelTime))

    # TO DO: display mean travel time
    avgTravelTime = round(df['Trip_Duration'].mean(),2)
    print('Mean travel time was {}'.format(avgTravelTime))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    display_raw_data(df, 'trip_duration_stats', ['Trip_Duration'])


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    numOfSubscribers = df[df['User_Type'] == 'Subscriber'].User_Type.count()
    numOfCustomers = df[df['User_Type'] == 'Customer'].User_Type.count()

    print('The number of subscribers were {}\nThe number of customers were {}'.format(numOfSubscribers,numOfCustomers))

    lisOfUserColumns = ['User_Type']

    # TO DO: Display counts of gender
    if city != 'washington':
        numOfMen = df[df['Gender'] == 'Male'].Gender.count()
        numOfWomen = df[df['Gender'] == 'Female'].Gender.count()

        print('The number of men were {}\nThe number of women were {}'.format(numOfMen,numOfWomen))

        lisOfUserColumns.append('Gender')

    # TO DO: Display earliest, most recent, and most common year of birth
        earliestBirth = int(df.Birth_Year.min())
        mostRecentBirth = int(df.Birth_Year.max())
        mostCommonBirth = int(df.Birth_Year.mode()[0])
        print('The earilest birth year was {}\nThe most recent birth year was {}\nThe most common birth year was {}'.format(earliestBirth,mostRecentBirth,mostCommonBirth))

        lisOfUserColumns.append('Birth_Year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    display_raw_data(df, 'user_stats', lisOfUserColumns)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
