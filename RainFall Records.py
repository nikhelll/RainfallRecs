x` import pandas as pd
pd.options.mode.chained_assignment = None  #so that editRecord() works
import sys
import matplotlib

class RainFallRecord:
    def __init__(self, flag): #flag, True if task1/2. False if task3
        self.year=0
        self.cityFile=''
        self.months=[]
        if flag == True:
            self.dataFrame = pd.read_csv(self.cityFileChooser(), skiprows=2, index_col=0, header=None)
            self.dataFrameCleaner()
        
    def dataFrameCleaner(self): #clear unwanted characters from data, only cleans rainfall column. Can be easily changed to clean whole file however
        index=len(self.dataFrame.index)
        for i in range(index):
            try:
                float(self.dataFrame.iloc[i, 4])
            except:
                self.dataFrame.iloc[i, 4] = "".join(ch for ch in self.dataFrame.iloc[i, 4] if ch.isalnum())
                print("Removed special character")
        self.dataFrame.to_csv(self.cityFile)

    def cityFileChooser(self): #assigns filepath to class variable
        city = int(input("Enter which city you'd like to access data from\n1.Oxford\n2.Aberporth\n3.Armagh\n"))
        if(city == 1):
            self.cityFile='Oxford.csv'
            return 'Oxford.csv'
        elif(city==2):
            self.cityFile='Aberporth.csv'
            return 'Aberporth.csv'
        elif (city==3):
            self.cityFile='Armagh.csv'
            return 'Armagh.csv'
        else:
            print("INVALID CITY. TERMINATING PROCESS")
            sys.exit()
        
    def monthsAndYearInput(self, months,year):   #assigning year and list of months (prerequisite for findRecords())   
        self.year = year
        self.months= months
        #print(self.months)

    def findRecords(self):  #finds records with specified time criteria, returns a clean dataFrame with just specified months and rainfall data
        try:
            yearFrame = self.dataFrame.loc[str(self.year)]   
            rainarray =[]   
            for month in self.months:      
                rainarray.append(yearFrame.iloc[int(month)-1, 4])               
            print("\nAverage rainfall table for year: ", self.year, "\n")    
            returnFrame = pd.DataFrame({'AvgRainfall': rainarray}, index=self.months)    
        except:
            print("Invalid data input, file may not contain data for such time period")
            sys.exit()
        print(returnFrame)   
        return returnFrame
        
    def findAvgFromFrame(self, inFrame): #takes a cleaned dataframe from findrecords (with only rainfall data), calculates average
        avg=0.0
        #print(inFrame)
        index=len(inFrame.index) #amount of rows
        for i in range(index):           
            if float(inFrame.iloc[i]) != -1.0: #if not deleted
                avg+=float(inFrame.iloc[i])
            else: #to handle moving averages with missing data points (a+b+c+d.../k) : k=0, k+=1 foreach valid data point a-z+. if missing point k is not incremented (or in this case index is decremented)
                index-=1 
                pass
        try:
            avg=avg/index
        except:
            return None
        return avg          

    def rainfall(self, year): #rainfall takes as input a month and return the value of the rainfall in the given month of the year, and city
        self.year =year         
        month = int(input("\nEnter month you'd like to see data for: "))  
        self.months = [month]
        return(self.findRecords())
        
    def delete(self,year):
        self.year=year       
        month = int(input("\nEnter month you'd like to delete rainfall data for: "))
        self.editRecord(month, value=-1)    #exception checked    

    def insert(self,year):
        self.year=year       
        month = int(input("\nEnter month you'd like to insert rainfall data for: "))
        value = int(input("\nEnter value you would like to insert:"))
        self.editRecord(month,value)  #exception checked  
        
    def editRecord(self, month,value): #changes a a SINGLE SPECIFIED CELL per run. Can loop through this many times (next function)
        try:
            self.dataFrame.loc[self.year].iloc[int(month)-1, 4] = value
            self.dataFrame.to_csv(self.cityFile) #Inefficient?
        except:
            print("\nError editing cell. Cannot be located with data given")
            sys.exit()
        print("\nData successfully edited!")
    
    def insertQuarter(self,year): #insert function with a little bit more info needed, loops through editRecord unlike insert()
        self.year=year
        quarter = int(input("\nEnter quarter you'd like to insert rainfall for: 1/2/3/4 (Jan/Feb/Mar .... Oct/Nov/Dec"))
        values = input("\nEnter rainfall values you'd like to add for each consecutive months of specified quarter. Separated by commas.")
        values=values.split(',')
        if len(values) != 3: 
            print("Invalid amount of data added!")
            self.insertQuarter(year)#keep the program flowing
        for i in range(3):
            self.editRecord(i+(quarter*3-2), int(values[i])) ###########
    
    def selRecords(self, id):
        if id==1:
            self.dataFrame = pd.read_csv('Oxford.csv', skiprows=2, index_col=0, header=None)
            return self
        elif id==2:
            self.dataFrame = pd.read_csv('Aberporth.csv', skiprows=2, index_col=0, header=None)
            return self
        elif id==3:
            self.dataFrame= pd.read_csv('Armagh.csv', skiprows=2, index_col=0, header=None)
            return self

class Archive:
    def __init__(self):
        self.rainFallRecords = dict()

    def main(self):
        print("\nWelcome to the archive")   
        self.taskThree()

    def taskThree(self):
        task3 = int(input("\n1 for data insertion, 2 for data deletion, 3 for moving average calculator"))
        if(task3==1):
            self.insert()
        elif(task3==2):
            self.insert()
        elif(task3==3):
            self.sma()
        else:
            print("Invalid input")
            sys.exit()

    def insert(self):#error check here
        id = int(input("Which city should be inserted? 1. Oxford 2. Aberporth 3. Armagh")) #if i had csvs for many more cities i would automate this
        a = RainFallRecord(False)
        if id==1:
            self.rainFallRecords["Oxford"] = a.selRecords(id)
        elif id==2:
            self.rainFallRecords["Aberporth"] = a.selRecords(id)
        elif id ==3:
            self.rainFallRecords["Armagh"] = a.selRecords(id)
        else: 
            print("Invalid city selected")
        
        next = input("Insert another? Y/N")
        if next.capitalize() == "Y":
            self.insert()
        elif next.capitalize == "N":
            self.taskThree()
        

    def delete(self, rfr):
        try:
            self.rainFallRecords.__delitem__(rfr)
        except:
            print("Record not present in DB")

    def sma(self):  
        for i in self.rainFallRecords:
            print(i)

        city = input("Enter a city to look through (Type it in)")
        try:
            rfr = self.rainFallRecords[city]
        except:
            print("City not found! Retry \n")
            self.sma()

        year1 = int(input("Enter a start year: "))
        year2 = int(input("Enter an end year: "))
        if year1>year2:
            print("")

            ####godot
           
        ma = int(input("Enter k months as moving average chunk size: \n"))
        months = [1,2,3,4,5,6,7,8,9,10,11,12]  #need a pointer based system as a chunk may go from 11 - 2 for example
        pointer =0
        allFrames= pd.DataFrame() 
        for i in range(year2-year1):
            curyear = year1+i
            rfr.monthsAndYearInput(months,str(curyear))       
            allFrames = allFrames.append(rfr.findRecords())

        done = False
        pointer=0
        movingAvgList=[]
        while done==False:
            maChunk = allFrames.iloc[pointer:pointer+ma]  
            pointer +=1
            if pointer +ma > len(allFrames.index):
                done=True
            movingAvgList.append(rfr.findAvgFromFrame(maChunk))

        print(movingAvgList)
                  
class Driver: #in charge of running other classes
    def __init__(self):
        self.Arc = Archive()
        self.calc()
        
    def calc(self):
        task = int(input("1 for task 1, 2 for 2, 3 for 3")) 
        if (task==1):    #done and robusted
            rfr = RainFallRecord(True)      
            put = input("\nInput a year, then a comma, then all the months as a set of numbers separated by commas: ")
            yearPlusMonths = put.split(',')
            year =yearPlusMonths[0] #error check here
            yearPlusMonths.remove(year)
            months=yearPlusMonths           
            rfr.monthsAndYearInput(months, year)           
            print("AVG: ",rfr.findAvgFromFrame(rfr.findRecords()))

        elif (task==2):
            rfr = RainFallRecord(True)
            task2 = int(input("\n1 for Search, 2 for Delete, 3 for Insert, 4 for InsertQuarter \n"))           
            year = int(input("Enter year you'd like to search in\n"))            
            if(task2==1):
                rfr.rainfall(year)
            elif(task2==2):
                rfr.delete(year)
            elif(task2==3):
                rfr.insert(year)
            elif(task2==4):
                rfr.insertQuarter(year)
            else:
                print("Invalid input, no task selected")
                sys.exit()

        elif (task==3):
            self.Arc.main()
        else:
            print("Invalid input")
            sys.exit()
            

a = Driver()
a.calc()