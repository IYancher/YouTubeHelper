from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showerror
from openai_api import *
from tkinter.scrolledtext import ScrolledText
import os, openai


TITLE_REQUEST_PREFIX = "Write title for YouTube video about "
DESCRIPTION_REQUEST_PREFIX = "Write description for YouTube video about "
KEYWORD_REQUEST_PREFIX = "Write at least 35 comma separated keywords or keyphrases for YouTube video about "



main_window = Tk()

LABEL_FONT = ("Calibri", 14)
WIDGET_FONT = ("Calibri", 12)

openai.api_key = OPENAI_API_KEY

title_area = None
description_area = None
keywords_area = None



def output(title, description, keywords):
    
    global title_area
    global description_area
    global keywords_area
    
    output_frame = Frame()
    output_frame.pack(side=LEFT, pady=40)

    
    title_lable = Label(output_frame, text="Title:", font=LABEL_FONT)
    title_lable.pack(anchor=W, padx=30)
    
    title_area = ScrolledText(output_frame, font=WIDGET_FONT, wrap="word", height=2)
    title_area.pack(anchor=W, padx=30)
    title_area.insert("1.0", title)
    
    
    
    Label(output_frame).pack(pady=5) # just spacer
    description_lable = Label(output_frame, text="Description:", font=LABEL_FONT)
    description_lable.pack(anchor=W, padx=30)
    
    description_area = ScrolledText(output_frame, font=WIDGET_FONT, wrap="word", height=5)
    description_area.pack(anchor=W, padx=30)
    description_area.insert("1.0", description)
        
        
    
    Label(output_frame).pack(pady=5) # just spacer
    keywords_lable = Label(output_frame, text="Keywords:", font=LABEL_FONT)
    keywords_lable.pack(anchor=W, padx=30)
    
    keywords_area = ScrolledText(output_frame, font=WIDGET_FONT, wrap="word", height=10)
    keywords_area.pack(anchor=W, padx=30)  
    keywords_area.insert("1.0", keywords)
        
    button_frame = Frame()
    button_frame.pack(side=RIGHT)

    
    Button(button_frame, text="Save data", command=save_data, font=WIDGET_FONT).pack(padx=20, pady=15, ipadx=25, ipady=5,anchor=E)
    Button(button_frame, text="Reset all", command=reset_all, font=WIDGET_FONT).pack(padx=20, pady=15, ipadx=25, ipady=5, anchor=E)

    pass


def send():
    
    user_description = input_user_description.get()
    title_request = TITLE_REQUEST_PREFIX + user_description
    description_request = DESCRIPTION_REQUEST_PREFIX + user_description
    keywords_request = KEYWORD_REQUEST_PREFIX + user_description
    if user_description == "":
        showerror(title="Error", message="Your request is empty")
        return
    try:
        title_response = openai.Completion.create(model="text-davinci-003", prompt=title_request, max_tokens=200)
        title = title_response.choices[0].text.strip()
        
        description_response = openai.Completion.create(model="text-davinci-003", prompt=description_request, max_tokens=1000)
        description = description_response.choices[0].text.strip()
        
        keywords_response = openai.Completion.create(model="text-davinci-003", prompt=keywords_request, max_tokens=3000)
        keywords = keywords_response.choices[0].text.strip()
        
                
    except openai.error.RateLimitError:
        showerror(title="Error", message="You've reached the requests limit")
    except openai.error.AuthenticationError:
        showerror(title="Error", message="Incorrect API key provided")
    except:
        showerror(title="Error", message="Unknown error")
        
    else:
        if len(title) != 0 or len(description) != 0 or len(keywords) != 0:
            output(title, description, keywords)
        else:
            showerror(title="Error", message="Unknown error. Data doesn't exist")


def clear():
    input_user_description.delete(0, END)
    
    
def save_data():
    
    title = title_area.get("1.0", END)
    description = description_area.get("1.0", END)
    keywords = keywords_area.get("1.0", END)
    
    data_for_save = f"Title:\n{title}\n\nDescription:\n{description}\n\nKeywords:\n{keywords}"
    
    filepath = filedialog.asksaveasfilename(defaultextension="txt")
    if filepath != "":
        with open(filepath, "w") as file:
            file.write(data_for_save)
            
            

def reset_all():
    clear()
    title_area.replace("1.0", END, "")
    keywords_area.replace("1.0", END, "")
    description_area.replace("1.0", END, "")
    main_window.update()
    pass


main_window.geometry("900x700+0+0")
main_window.resizable(False, False)
icon_path = os.path.join(os.path.dirname(__file__), "favicon.ico")
main_window.iconbitmap(default= icon_path)
main_window.title("YouTube Helper 1.0")

user_frame = Frame()
user_frame.pack(fill=BOTH)

user_frame_top = Frame(user_frame)
user_frame_top.pack(fill=BOTH, side=TOP)
user_frame_bottom = Frame(user_frame)
user_frame_bottom.pack(side=BOTTOM)

input_user_description_label = Label(user_frame_top, text="What is your video about?", font=LABEL_FONT)
input_user_description_label.pack(anchor=W, pady=20, padx=30)

input_user_description = Entry(user_frame_top, font=WIDGET_FONT)
input_user_description.pack(anchor=NW, padx=30, ipadx=30, ipady=5, fill="x")


Button(user_frame_bottom, text="Send", command=send, font=WIDGET_FONT).pack(padx=20, pady=15, ipadx=25, ipady=5, side=LEFT)
Button(user_frame_bottom, text="Clear", command=clear, font=WIDGET_FONT).pack(padx=20, pady=15, ipadx=25, ipady=5, side=LEFT)


   

main_window.mainloop()