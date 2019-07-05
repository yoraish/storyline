#!/usr/bin/env python
print( "Content-type: text/html\n")
import cgitb
import cgi
import datetime
import sqlite3
import datetime
import json
# # code that is responsible to return the most recent line from the story and also handle the insertion of a new line

# cgitb.enable()

#command below takes the arguements from the get request and puts them in some sort of a dictionary
# There are two options for this script.
# * Get last line:
#       Simply return the last line from the json
# * Update story and return last line
#       Put in the new line at the end of the json string (\n), also as the last line in the json
#       Return the last line (the one just added)


def get_last_line():
    # load the json file
    with open("last_and_story.json") as jsonfile:
        data = json.load(jsonfile)
        last_line = data["last"]
        story = data["story"] # This loads the whole story to memory, which is kinda meh. But let's assume for nw that that's fine.
        return last_line

def add_line(new_line):
    # Adds the new line to the story and sets it in the last line place in the json file.
    # Do not forget to add a new line break at the end of the story.
    with open("last_and_story.json") as jsonfile:
        # Get the contents of the file.
        data = json.load(jsonfile)
        story = data["story"] # This loads the whole story to memory, which is kinda meh. But let's assume for nw that that's fine.
        # Modify new line to be updated
        last_line = new_line
        # Add it to story, anding the line afterwards
        story+= new_line+"\n"
        new_data = {"last":last_line, "story":story}
    # Wrtie back to json
    with open("last_and_story.json", 'w') as jsonfile:
        json.dump(new_data, jsonfile)

def create_json():
    sample_json = {"last": "This is the most most recent line",
                    "story": "Old line\nOlder line.\nOldest line.\n"}
    with open("last_and_story.json", 'w') as jsonfile:
        json.dump(sample_json, jsonfile)    


def handle_request(request):
    """ The expected fields of request are:
    > command -> "get" || "add"
    > line    -> "line_text_string". Empty if in in "get" command.
    """
    command = request["command"].value

    if command == "get":
        # Print out the most recent line
        last_line = get_last_line()
        print(last_line)

        pass
    if command == "add":
        pass
    print(command)



if __name__ == "__main__":
    # create_json()
    # get_last_line()
    # add_line("TSUPERline")
    # get_last_line()


    # Get the request.
    inDataDict = cgi.FieldStorage()
    # Pass the dictionary to the function that deals with it.
    handle_request(inDataDict)


# #ask that the info will bi in the form of asdfgefs/dataHandler.py?status='alive' OR 'filming'
# if 'status' in inDataDict:
#     # modify the txt file
#     with open('status.txt', 'w') as f:
#         # re-write the file with the current data we got:
#         month_dict = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep',10:'Oct', 11:'Nov', 12:'Dec'}
#         now = datetime.datetime.now()
#         year = now.year
#         day = now.day 
#         date = month_dict[now.month] +' '+ str(day)+' ' + str(year)
        
#         hour = ('0'+ str(now.hour))[-2:] + ':' +('0'+ str(now.minute))[-2:] +':'+ ('0'+ str(now.second))[-2:]



#         new_data_string = 'Status is ~~' +  inDataDict.getvalue('status') + '~~ at '+hour+' '+ date + ' Boston Time'
#         f.write(new_data_string)

# # now, whether or not we modified the file, we will print the file out, since this is the most recent update

# with open ('status.txt', 'r') as f:
#     data = f.read()
#     print(data)


