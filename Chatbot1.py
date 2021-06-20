# importing all libraries
import os
import dialogflow
from google.api_core.exceptions import InvalidArgument
from tkinter import *
import random
import csv

# creating the main chatbot window
main = Tk()
main.geometry("500x650")
main.title("IHG Clarity Chatbot")

# Adding IHG Logo at top
img = PhotoImage(file="ihg.png.png")
image = Label(main, image=img)
image.pack(pady=10)


# creating ask_bot function
def ask_bot():
    query = textbox.get()
    text_to_be_analyzed = query

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    if response.query_result.intent.display_name == 'ProjectRename':
        file_name = filename(response.query_result.intent.display_name)

    write_bot(query, response.query_result.fulfillment_text, response.query_result.intent.display_name)
    # write_csv(file_name,query)

    # # writing to csv
    # dictionary = {'User': str(query), 'Bot': str(response.query_result.fulfillment_text)}
    # with open('clarity.csv', 'a+', newline='') as file:
    #     writer = csv.writer(file)
    #     for key, value in dictionary.items():
    #         writer.writerow([key, value])

    # with open('proj_rename.csv', 'a+', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(write_csv)


def filename(name):
    if name == 'ProjectRename':
        filename = 'proj_rename.csv'
    return filename


def write_bot(query, response, intent):
    if query.lower() == "thanks" or query.lower() == "quit" or query.lower() == "exit":
        msgs.insert(END, "ChatBot : " + response + "\n" + "\n")
        main.after(3000, main.destroy)
        file = open('proj_rename.csv', 'a+', newline="")
        with file:
            header=['CurrentProjectID','NewProjectName','Email']
            writer=csv.writer(file)

            # writer.writeheader()
            writer.writerow(write_csv)

    elif intent == 'CurrentProjectID' or intent == 'NewProjectName' or intent == 'Email':
        msgs.insert(END, "You : " + query + "\n" + "\n")
        msgs.insert(END, "ChatBot : " + response + "\n" + "\n")
        textbox.delete(0, END)
        msgs.yview(END)

        # dictionary[intent] = query
        # with open('proj_rename.csv', 'a+') as file:
        #     dictionary[intent] = query
        #     print(dictionary)

        if intent=='CurrentProjectID':
            write_csv[0] = query
        elif intent=='NewProjectName':
            write_csv[1] = query
        elif intent=='Email':
            write_csv[2] = query
        else:
            pass

    else:
        msgs.insert(END, "You : " + query + "\n" + "\n")
        msgs.insert(END, "ChatBot : " + response + "\n" + "\n")
        textbox.delete(0, END)
        msgs.yview(END)


# Creating the frame inside the main window
frame = Frame(main)
scroll = Scrollbar(frame)
msgs = Text(frame, width=80, height=25, yscrollcommand=scroll.set, wrap=WORD)
scroll.pack(side=RIGHT, fill=Y)
msgs.pack(side=LEFT, fill=BOTH, pady=10, padx=5)
frame.pack()

# Creating text box for query
textbox = Entry(main, font=("Verdana", 16))
# textbox.pack(fill=X, pady=10, padx=5)
textbox.place(x=5, y=560, height=70, width=370)

# Creating the button
button = Button(main, text="Send", font=("Verdana", 20), command=ask_bot)
# button.pack()
button.place(x=400, y=560, height=70, width=80)


# Creating a function to revoke button through Enter key
def enter_function(event):
    button.invoke()


# Binding main window with Enter key
main.bind('<Return>', enter_function)

# Random number generator for session ID
n = random.randint(11, 220)
# print(n)

# Dialogflow Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'
DIALOGFLOW_PROJECT_ID = 'chatbot1-projectid'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = str(n)
write_csv = ['CurrentProjectID', 'NewProjectName', 'Email', 'Pending']
dictionary = {'CurrentProjectID': 'a', 'NewProjectName': 'b', 'Email': 'c'}

# def write_csv(filename, query):
#     write_csv.append(query)
#     with open(filename, 'a+', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(write_csv)

main.mainloop()
