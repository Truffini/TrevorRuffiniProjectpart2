# TrevorRuffiniProjectpart2

This code is built off of part 1, however it is now saved too a database, and has 2 additional tests. One to check the number of data items retrieved and another to create a new 
empty database, that runs a table creation function, then saves the data to the database method to check to see that the database contains the test university that has been put 
there. Along with workflow updates, requirements.txt added as well as API_KEY.

the database has been created in such a table that it follows similar but more clear structure to part 1.
It gets the data for all universities with degrees of type 2 and 3.
With columns as followed.

school.name
school.city
2018.student.size
2017.student.size
2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line
2016.repayment.3_yr_repayment.overall

I have added sprint three, which takes in data from an excel sheet, adding the new table emp_data to our original database, it shows the following statistics(as DB row)
for each state (including territories).

the state
the occupation major title
the total employment in that field in that state
the 25th percentile salary (lets assume that most college grads earn in the lower 25%) for that field both hourly and annual

there has also been added tests to check if the method to read from the xlsx file works properly.
testing if all 50 states are included and to make sure it gets the right number of major occupational groups.
along with other tests that check to see if the old and new tables are still there and writing.

I have refactored the database to include
the school.state
the 2016.repayment.repayment_cohort.3_year_declining_balance
as well as the existing data that you are already retrieving.

I have also created a GUI so that users can interact with the project more naturally
When the program first starts up with the GUI it allows the user to choose to either
update the data
run the data visualization
When updating the data is chosen
the project lets the user choose the file name for the excel file
When data visualization is chosen
it provides the user the ability to do two forms of data analysis
The first analysis displays the data in a color coded text format as a list in ascending or descending order  chosen by user
The second renders maps to visualize the data.



