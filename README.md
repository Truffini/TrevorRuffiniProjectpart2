# TrevorRuffiniProjectpart2

This code is built off of part 1, however it is now saved too a database, and has 2 additional tests. One to check the number of data items retrieved and another to create a new 
empty database, that runs a table creation function, then saves the data to the database method to check to see that the database contains the test university that has been put 
there. Along with workflow updates.

the database has been created in such a table that it follows similar but more clear structure to part 1.
It gets the data for all universities with degrees of type 2 and 3.
With columns as followed.

school.name
school.city
2018.student.size
2017.student.size
2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line
2016.repayment.3_yr_repayment.overall

The only issues faced with the code was when test were being applied I began to get a key error on 'metadata' I suspect there may have been an API issue.
I also have put this in a seperate repository because in part one I made a mistake discussed in office hours while creating the repository and could not push although now fixed 
in this repository.
