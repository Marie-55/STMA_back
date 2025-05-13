# in this file, we will create a middleware that will fetch data from the database using Backend controllers

# We will first explain what we need as input for the algorithm
##  All tasks from the day the task is entered -> deadline date 
#### we have to get all tasks from to from data base
#### convert them into json format 
#### return json
##  All sessions from the day the task is entered -> deadline date (same as above)

## extracting all availabale time slots (from json -- doesn't need fetching)

# simluated annealing: 
## input: available time slots, tasks, sessions
## output: Dict [date, LIST[TASK]] -----> call controller to write the tasks into their respective dates (in week, days schedule)



#Genetic algorithm:
## input: available time slots within the day, tasks of the day, create sessions for tasks ---> needs to retrieve the day schedule from the database
## output: Dict [date, LIST[TASK]] -----> call controller to write the tasks into their respective times within the day ( days schedule, add sessions)