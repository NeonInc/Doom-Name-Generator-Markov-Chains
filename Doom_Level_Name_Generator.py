from tkinter import *
from tkinter.font import Font
from tkinter import scrolledtext
import numpy as np


# *****************************************************************************
# Window and Canvas values 
# *****************************************************************************

master = Tk()
master.title('Doom Level Name Generator') 
master.minsize(1024, 768) 
master.configure(background='#696969')
canvas_height=300
canvas_width=600

# *****************************************************************************
# Create the word and the next word association.
# *****************************************************************************

def make_word_pairs(corpus):
    for i in range(len(corpus)-1):

        # If the next word is 'The', skip to the word after that  
        if corpus[i+1] == '.the':
          yield (corpus[i], corpus[i+2])
        else:
          yield (corpus[i], corpus[i+1])


# *****************************************************************************
# Create the end words list. 
# *****************************************************************************
         
def make_end_words_list(corpus,end_words_list):
    for i in range(len(corpus)):
      if corpus[i].find(',') != -1:
          end_words_list.append(corpus[i].replace(",", ""))
          corpus[i]=corpus[i].replace(",", "")

# *****************************************************************************
# Called when Generate is clicked. 
# *****************************************************************************

def generate_level_names():

    # Clear previously generated level name list
    scrolled_text.config(state=NORMAL)
    scrolled_text.delete('1.0', END)
    
    # Choose the respective name file depending on the radio button selection
    if v.get() == 1:
        level_name_data = open('.\Level_Names-SciFi_Theme.txt', encoding="latin-1").read()
        no_of_words = 3
    elif v.get() == 2:
        level_name_data = open('.\Level_Names-Hellish_Theme.txt', encoding="latin-1").read()
        no_of_words = 4

    # Split the read data into individual words and convert to lower case
    corpus = level_name_data.lower().split()

    # Initiate and call function to create end words list
    end_words = []
    make_end_words_list(corpus,end_words)

    # Create word pairs
    word_pairs = make_word_pairs(corpus)
    
    # Create a dictionary to hold word and next word
    word_dict = {}

    # Add word and next word to dictionary
    for word_1, word_2 in word_pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]    

    # No of iterations to run the name generator loop
    no_of_iterations=1000

    # No of generated level names
    no_of_level_names=10

    # Generated level names list
    generated_names=[]

    # Start generator loop
    for i in range(no_of_iterations):
    
        # Choose random word from file
        first_word = np.random.choice(corpus)

        # Add the first word to chain 
        chain = [first_word]
        
        # Run loop as long as chain is less than the desired length
        while len(chain)<no_of_words:
            
            # Randomly choose next word from dictionary by feeding in last word of chain
            chosen_word=np.random.choice(word_dict[chain[-1]])
            
            # If the chosen word is already in chain
            if chosen_word in chain:
                
                # Randomly choose next word from dictionary by feeding in last chosen word
                # Append to chain
                new_chosen_word=np.random.choice(word_dict[chosen_word])
                chain.append(new_chosen_word)

            # Append chosen word to chain if not already in chain     
            elif not(chosen_word in chain):
                chain.append(chosen_word)
            
            # Break current iteration if chain doesn't contain unique words
            if len(set(chain)) != len(chain):
                break
            
            # Add generated name to list, if chain length greater than or equal to 
            # desired chain length and last word in chain in end words list
            if len(chain) >= no_of_words and chain[-1] in end_words:

                # Clean and format chain
                level_name=' '.join(chain)
                level_name=level_name.replace(".the", "the").capitalize()
                level_name=level_name.replace(",", "")

                # Display generated if it is unique
                if not(level_name in generated_names):
                    scrolled_text.insert(INSERT,level_name+'\n')
                    scrolled_text.update()

                # Add generated name to list
                generated_names.append(level_name)
                
                break

        # Break out of current function if desired no of level names have been generated   
        if len(set(generated_names)) == no_of_level_names: 
            break

    scrolled_text.config(state=DISABLED)
    
# Draw canvas and display image  
w = Canvas(master, width=canvas_width, height=canvas_height,bg='#696969',highlightthickness=0) 
w.pack() 
doom_logo = PhotoImage(file=".\Doom_Logo.png")    
w.create_image(0,0, anchor=NW, image=doom_logo) 

# Main instruction label
main_instructions=Label(master, text="Select the theme of the genrated level name and click Generate. ",fg = "#000000",bg='#696969',font = "Times 18 bold").pack()

# Radio button variable to hold value
v = IntVar()

#Radio buttons to choose theme
scifi_theme_radio_button=Radiobutton(master,font="Times 15 bold",text="Sci-Fi Theme", variable=v, value=1,bg='#696969',activebackground='#696969',activeforeground='#7f0000',selectcolor='#800080').pack(anchor=CENTER)
hellish_theme_radio_button=Radiobutton(master,font="Times 15 bold",text="Hellish Theme", variable=v, value=2,bg='#696969',activebackground='#696969',activeforeground='#7f0000',selectcolor='#800080').pack(anchor=CENTER)

# Click button to genrate level names
generate_button = Button(master,font="Times 15 bold",text="Generate", bg='#800080',activebackground='#7f0000',command=generate_level_names).pack(pady=10)

# Scrolled text widget to hold genrated level names
scrolled_text = scrolledtext.ScrolledText(master,width=40,height=12,font="Times 15 bold",fg = '#000000',bg='#696969')
scrolled_text.pack(pady=30)

#Main loop of program
mainloop()




