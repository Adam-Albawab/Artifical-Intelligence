Name: Adam Albawab  ID#1001572887  CSE4380-002
------------------------------------------------------------
This program was written for Python 3.9.0. 
------------------------------------------------------------
The code is structured by dividing the five tasks that need
to be done into five methods. The methods are as follows:

1) uniformedParsing - a method to parse all of the necessary
   information from the city file for the uninformed searching 
   algorithm.
2) informedParsing -  a method to parse all of the necessary
   information from the heuristic file as well as the city file.
3) UCS - a method that essentially uses the parsed information
   from the previous methods to perform the Uniform Cost Search
   upon the graph before returning the number of nodes popped and
   generated as well as the total distance and the route taken.
4) aStar - a method that essentially uses the parsed information
   from the first two methods to perform the A* graph search
   upon the graph before returning the number of nodes popped and
   generated as well as the total distance and the route taken.
5) displayInfo -  a method to neatly display the information that
   is created through the searches.

Lastly there is a chunk of code at the bottom to parse the command-line
arguments and call the methods.
------------------------------------------------------------------------
In order to run this program you should have Python 3.9.0 and you should
enter the following command into the command terminal:

python find_route.py input_filename origin_city destination_city heuristic_filename 

If you do not enter a 5th argument then it will run the UCS search.