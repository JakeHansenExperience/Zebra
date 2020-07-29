Directions for Running:

1. Add files you wish to test to the inputFiles directory. Note that currently
that directory holds the two test files given in the assignment.

2. Re-name the output variable to whatever you would like (line 128). Currently, I have the
final schema outputting to "outputFiles/ZebraAssignmentOutput-' + str(date.today()) + '.csv'",
but obviously you can name it whatever your heart desires!

3. Make sure you have the environment set up with the dependencies listed below

4. CD into the Zebra directory from the command line

5. Run the command 'python zebraReader.py'

6. Sit back and shed a tear at how beautiful the new CSV file is!

If you would rather have just use a list files and not have a whole directory, you can
uncomment lines 140-144, 152-153, 162 and 166 and comment lines 147, 151, 154, 161, and 167.
I could see instances in your testing where you would rather just hand pick a few
test cases, in which case just listing them out would be easier than giving a whole
directory.

For my approach, I took the line in the requirements that files could be in the
tens of thousands to mean that any input > 99999 lines would be too many for a single
run. So first, I check to make sure that the input isn't too big, which would take O(n)
time where n represents the number of lines. I also check to make sure all the
input files are in '.csv' format. I guess one could argue that this isn't the
ideal approach, if 9 files are in CSV format but one is a pdf, and the company
would still want the data from the 9 files it should not just exit. However,
I reasoned that given the objective is to combine all the data, it would be better
to fail in this case, get rid of the pdf / save the pdf as a csv, and then re-run.
Wouldn't be a big change though, and would just depend on why the company wants this
data / what it will be used for if it should just always grab as much data as
possible or if it is important to have it all go at the same time.

Once the input passes the length / csv requirements, the script loops through
every file in the directory (or every file in the list given if you take that
approach). For each file, it first checks to see if the file has the required
column names for the output schema. If the file does not possess the required headers,
the getHeaderIndexes function returns a bool False and the algorithm goes on to the
next file, given none of the rows would work in that file and adds all the rows
in that file to the printed error message. If the file does have the required headers,
for each row in the file it then checks to see if the data can be fit to the output
schema, and if so adds it to the final string that is the CSV file for the output.
The indices dictionary is the "bread and butter" of this approach because it allows
for quick accessing of the necessary data fields for each row in a file.

For outputting, I wait until the end to write the output because of how expensive
writes are in terms of time / screen delays. One thing I noticed in the directions
was the line that "they always send the columns in the same order". Originally,
I had only been thinking of O(n) as n being the number of lines, but this piece
of information reminded me that there is an O(m) where m is the number of columns, that
would happen for each file being read (just once at the headers line, but still if
the file came with over a million columns, that would be a significant time constraint)
In order to combat this, I created the "DataSource" class and at the end store a
dictionary of all the 'datasource' objects referenced by the file name.
In the case where some of in input would be consisting of millions of columns, it
would be advantageous to remember the indices from the previous day so that the
computer wouldn't have to check all the headers again for a specific source. I
therefore determined that having a master dictionary of all the data sources
indices would be helpful, as well as storing an array of the datasource objects
daily as a way to "log/track" how many good / bad lines come from a data source
each day. I didn't include the necessary code for importing the pickle file at the
beginning of the loop for two reasons. First, I do know that pickle files have some
security issues, so I didn't want to risk anything with that, and second I honestly
don't know if pickle files are used in "professional" environments or not. I saved
the pickle files to show that I am comfortable using them, and in many instances in
the past I have found them to be useful. But, I have never worked in a "professional"
setting with other engineers(my previous experience I was only surrounded by SSIS
specific developers), so maybe pickle files are laughed at in professional settings.
Either way, hopefully the thought process of trying to save time is appreciated!

In terms of future steps for this project, I think it would really come down to
learning more about the companies sending the data, why The Zebra wants this data,
how The Zebra plans to use the data, as well as what the current data capabilities  
of The Zebra are. These possible extensions to the projects are what really excite
me about this potential role. Given I would be on the data team, and able to work with data
scientists / analysts / business stakeholders, there appears to me to be a lot of
potential for being creative and really contributing to meaningful projects. For example,
given part of this data is a link, we could write a web-crawler (beautifulSoup) to try
and get extra information from the companies websites, such as temporary promotions or
a missing phone number. This sort of "extra" data idea I could see being very beneficial if this was
a project for the data scientists. If this was for the data analysts, a next step
I could see would be modeling the current schema to fit with the current data warehousing
approach the company is using, allowing for current dashboards to quickly display this
data. From an engineering specific approach, adding a multi-threading approach could
help cut down on the time this job takes to run, especially if we are pulling these
data sources from multiple different sources and the companies aren't just sending us
the data because in my experience I found threading in python to be very helpful when making
external API calls. Also, instead of just putting "Error:" and then the offending row,
giving some sort of "Error: Missing X column" or "Error: Float expected, string given"
or something along those lines would make the error output more usable.

I thoroughly enjoyed building this for y'all, and I look forward to hopefully hearing back
from you! Thank you in advance for your time and consideration. Cheers.

Dependencies:

Python 3.8.1
csv
os
sys
pickle
datetime
pytest
