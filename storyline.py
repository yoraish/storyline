#!/usr/bin/env python
print ("Access-Control-Allow-Origin: *\r\nContent-type: text/html\r\n")
import cgitb
import cgi
import datetime
import sqlite3
import datetime
import json
import smtplib
from secret import email as email_addr
from secret import password

# # code that is responsible to return the most recent line from the story and also handle the insertion of a new line

cgitb.enable()

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
        return last_line

def add_line(new_line):
    # Adds the new line to the story and sets it in the last line place in the json file.
    # Do not forget to add a new line break at the end of the story.
    with open("last_and_story.json") as jsonfile:
        # Get the contents of the file.
        data = json.load(jsonfile)
        story = data["story"] # This loads the whole story to memory, which is kinda meh. But let's assume for now that that's fine.
        authors = data["authors"]
        # Modify new line to be updated
        last_line = new_line
        # Add it to story, anding the line afterwards
        story+= new_line+"\n"
        new_data = {"last":last_line, "story":story, "authors": authors}
    # Wrtie back to json
    with open("last_and_story.json", 'w') as jsonfile:
        json.dump(new_data, jsonfile)
    return new_line

def email_out(name_of_updater = "default_yorai", added_line = "default_line"):
    # Get the authors to email map from json file
    """
    TODO - GET THE NAME OF THE AUTHOR FROM THE HTTP REQUEST
    Till then, email everyone.
    """
    with open("last_and_story.json") as jsonfile:
        # Get the authors of the file.
        data = json.load(jsonfile)
        authors_to_emails = data["authors"]

    gmail_user = email_addr
    sent_from = email_addr
    gmail_password = password
    subject = "Storyline Update!"

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(email_addr, password)

    for name, to in authors_to_emails.items():
        body = "Hello "+name+  " the Hooman!\n\nThe author " + str(name_of_updater) + " has posted an update to your shared story!\n"
        body += "Check it out:\n\n"
        body += added_line + "\n"
        body+= "\n\nMay you be forgiven for your sins,\nThe Storyline team."
    
        email_text = ""
        email_text += 'From: %s\n' % gmail_user
        email_text += 'To: %s\n' % ','.join([to])
        email_text += 'Subject: %s\n\n' % subject
        email_text += body
        
        server.sendmail(sent_from, to, email_text)

    server.close()
    

def print_story():
    # Converts the story to html (linebreaks) and prints it.
    # Get story from json.
    with open("last_and_story.json") as jsonfile:
        # Get the contents of the file.
        data = json.load(jsonfile)
        story = data["story"]
        story_as_list = story.split("\n")
        for line in story_as_list:
            print("<p>"+line+"</p>")
        
        authors = data["authors"]
        print("<br>The authors are: ")
        print("<p>")
        for author,email in authors.items():
            print("<br>")
            print(str(author), ": ", str(email))
        print("</p>")
    


# def create_json():
#     sample_json = {"last": "This is the most most recent line",
#                     "story": "Old line\nOlder line.\nOldest line.\n",
#                     "authors":{"yorai":"yorai@mit.edu", "elise":"emcc1016@mit.edu"}}
#     with open("last_and_story.json", 'w') as jsonfile:
#         json.dump(sample_json, jsonfile)    


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

    if command == "add":
        # Get new added line string
        new_line = request["line"].value
        res = add_line(new_line)
        print(res)
        # Email out
        email_out("yorai the strong")


    if command == "show":
        print_story()




if __name__ == "__main__":
    # create_json()
    # get_last_line()
    # add_line("TSUPERline")
    # get_last_line()


    # Get the request.
    inDataDict = cgi.FieldStorage()
    # Pass the dictionary to the function that deals with it.
    handle_request(inDataDict)

