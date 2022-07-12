from datetime import datetime, date
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass


from config import readJsonlocation
from config import saveJsonlocation
# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
@dataclass
class Holiday:
    name: str
    date: str
        # String output
        # Holiday output when printed.
    def __str__(self):
        return "%s (%s)" % (self.name, self.date)
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    
    def __init__(self):
       self.innerHolidays = []
    
    def __str__(self):
        return str(self.innerHolidays)
   
    def addHoliday(self, holidayObj):
        if (type(holidayObj) == Holiday):
            self.innerHolidays.append(holidayObj)
            print("Success:")
            print(f"{holidayObj} has been added to the list")
        else :
            print("Only a Holiday Object is accepted")
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday
    
    def findHoliday(self, HolidayName, Date):
        for holiday in self.innerHolidays:
            if holiday.name == HolidayName and holiday.date == Date:
                return holiday
        return False
        # Find Holiday in innerHolidays
        # Return Holiday

    def removeHoliday(self, HolidayName):
        # Find Holiday in innerHolidays by searching the name and date combination.
        for i in self.innerHolidays:
            if i.name == HolidayName:
                # remove the Holiday from innerHolidays
                self.innerHolidays.remove(i)
                # inform user you deleted the holiday
                print(f"Success: {i} has been removed from the list")
                return
            else:
                print("Sorry, that holiday does not exist.")

    def read_json(self, filelocation):
        # Read in things from json file location
        with open(filelocation, "r") as f:
            data = json.load(f)
            for i in data['holidays']:
                self.addHoliday(Holiday(i["name"], i["date"]))
        # Use addHoliday function to add holidays to inner list.

    def save_to_json(self, filelocation):
        # Write out json file to selected file.
        with open(filelocation,"w") as holidayJSON:
            tempHolidayList = []
            for i in self.innerHolidays:
                holiday = {"name":i.name, "date":i.date}
                tempHolidayList.append(holiday)
            json.dump(tempHolidayList, holidayJSON, indent = 4)
            holidayJSON.write("\n")
        # Write out json file to selected file.
        
    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        try:
            holidays = []
        
            for year in range(2020,2025):

                url = (f'https://www.timeanddate.com/holidays/us/{year}?hol=33554809')
                response = requests.get(url)
                html = response.text

                soup = BeautifulSoup(html, 'html.parser')
                table = soup.find('table', attrs={'id':'holidays-table'})
                body = table.find('tbody')
                
                for row in body.find_all('tr'):
                    HolidayDict = {}

                    date = row.find('th')
                    name = row.find('a')

                    if date is not None and name is not None:
                        date = date.text
                        date = f"{date} {year}"
                        date= datetime.strptime(date,"%b %d %Y")
                        date = date.strftime('%Y-%m-%d')

                        HolidayDict['Name'] = name.text
                        HolidayDict['Date'] = date
                    holidays.append(HolidayDict)

                    while {} in holidays:
                        holidays.remove({}) 
                    holidays = [dict(t) for t in {tuple(d.items()) for d in holidays}]
            
            for i in holidays:
                hol = (Holiday(i['Name'], i['Date']))
                if hol not in self.innerHolidays:
                    self.innerHolidays.append(hol)
        
        except Exception as e:
                print(e)



    def numHolidays(self):
        return (len(self.innerHolidays))
        # Return the total number of holidays in innerHolidays
    
    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        holidays = list(filter(lambda x: datetime.strptime(x.date, '%Y-%m-%d').isocalendar()[0] == int(year) and datetime.strptime(x.date, '%Y-%m-%d').isocalendar()[1] == int(week_number), self.innerHolidays))
        # Week number is part of the the Datetime object
        return holidays
        # Cast filter results as list
        # return your holidays

    def displayHolidaysInWeek(self, holidayList):
        for i in holidayList:
            print(str(i))
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

    #def getWeather(weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        thisWeek = datetime.today().isocalendar().week
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        self.displayHolidaysInWeek(self.filter_holidays_by_week(datetime.today().year, thisWeek))
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results



def main():
    global readJsonlocation
    global saveJsonlocation
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    initList = HolidayList()
    
    # 2. Load JSON file via HolidayList read_json function
    initList.read_json(readJsonlocation)
    
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    initList.scrapeHolidays()
    
    # 3. Create while loop for user to keep adding or working with the Calender
    menu = True
    savedChoices = False

    print("\nHoliday Management")
    print("===================")
    print(f"There are {initList.numHolidays()} holidays stored in the system")


    while menu:
 # 4. Display User Menu (Print the menu)
        print("\nHoliday Menu")
        print("===================")
        print("1. Add a Holiday")
        print("2. Remove a Holiday")
        print("3. Save Holiday List")
        print("4. View Holidays")
        print("5. Exit")

        menuChoice = int(input("Please enter which option you would like to use: "))
        if menuChoice == 1:
            print("Add a Holiday")
            print("===============")
            holidayChoice = str(input("Holiday: "))
            dateChoice = input("Date (YYYY-MM-DD): ")
            initList.addHoliday(Holiday(holidayChoice, dateChoice))
        
        elif menuChoice == 2:
            print("Remove a Holiday")
            print("==================")
            holidayNamechoice = str(input("Holiday Name: "))
            initList.removeHoliday(holidayNamechoice)

        elif menuChoice == 3:
            print("Saving Holiday List")
            print("======================")
            saveList = str(input("Would you like to save your changes? (Y/N): "))
            if saveList == "N":
                print("Canceled:")
                print("Holiday list file save was canceled")
            else:
                initList.save_to_json(saveJsonlocation)
                print("Success:")
                print("Your changes have been saved")
                savedChoices = True

        elif menuChoice == 4:
            print("View Holidays")
            print("===============")
            chooseYear = input("Which year?: ")
            chooseWeek = input("Which week? [1-52, leave blank for the current week]: ")
            if chooseWeek == "":
                initList.viewCurrentWeek()
            else:
                print(f"These are the holidays for {chooseYear} week #{chooseWeek}:")
                initList.displayHolidaysInWeek(initList.filter_holidays_by_week(chooseYear, chooseWeek))

        elif menuChoice == 5:
            if savedChoices == True:
                chooseExit = input("Are you sure you want to exit? (Y/N): ")
                if chooseExit == "Y":
                    print("Goodbye!")
                    break
                elif chooseExit == "N":
                    continue
            elif savedChoices == False:
                unsavedExit = input("Are you sure you want to exit? Your changes will be lost. (Y/N)")
                if unsavedExit == "Y":
                    print("Goodbye!")
                    break
                elif unsavedExit == "N":
                    continue

   
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 


if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





