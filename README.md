# Periodic table - Chatbot.
Author: Loc Duc Minh Khong

# Introduction
At the school level, students learn basic concepts of many different subjects to develop a better understanding of the issues and problems around them. However, not all subjects are easy to learn and understand. Many students hate chemistry because it has a lot of information to memorize. One of the first things that students have to learn in chemistry is the periodic table, which is categorized and organized to provide the similarities and properties of the elements. Nevertheless, it requires a lot of time and effort to understand and remember the periodic table. Therefore, for this project, I want to create a chatbot that can answer questions about the periodic table of elements. With the chatbot, they can conveniently recall the information of elements and immediately get an answer to their questions. As a chatbot is like a friend who is always ready to help them, it can make learning not only be more enjoyable but also be more effective.

# Technical Overview
This project was implemented in Python 3 (ver 3.8.5). I didn't use any APIs and external libraries.
  
# Features of the Chatbot
  * Reply to common greeting, thanks and goodbye sentences in many different ways.
  
  * Respond to unexpected replies/inputs.
  
  * Answer question about the periodic table (Ex: How many rows/ columns? - What is the periodic table?)
  
  * Answer to questions about some characteristics of elements.
       * Who discovered the element.
       * Symbol or name of the elements. (if given name, or name if given symbol)
       * Atomic number or atomic mass.
       * Metal or nonmetal.
       * Gas or solid at room temperature.
       * Electrons and protons number.
       * Position of elements in the periodic table.
     
  * For Comparison questions, my chat bot can compare (more or less) - reactive, metallic and nonmetallic of 2 or more elements.
  
  * For Y/N questions, it is able to check the symbol or number of electrons and protons, atomic number, molar mass of an element. Moreover, it also can verify the comparison of reactivity, metal and nonmetal of 2 elements. For example: “Is Cl more reactive than F?”
  
  * Remember the element and information from the lastest question, so my chatbot can respond to “its/ it” and “what about/ how about” questions. For example: How many electrons does K have? And if in the next question, the user can ask “How about/ what about Na?” 

  * It can handle some variety of input questions and have from 2 -5 different ways to respond.

# Input Handling
I used the CYKParse to parse the user input, then split the input into single word and put them in a binary tree (leaves are the words and parents are part-of-speech tags, such as N: noun, V: Verb. 

I also made the grammar rules and lexicons for some common inputs which I predicted that the user will chat or ask my bot.

If the input is not in any grammar rules or lexicons, the chatbot will send a message to the user.
  
# Internal Representations and Data Sources
The data of the periodic table rarely changes and is stable over time, so I do not need to access any network-available database in real-time. Instead, I will use the data of the periodic table that I have found on the internet. The data has already been written, formatted, and saved in a JSON file [By Bowserinator](https://github.com/Bowserinator/Periodic-Table-JSON). As JSON is the string representation of the data, I will convert it to a python dictionary to read the data by using the loads() function of the JSON module.

# Output Handling
First, I use the getSentenceParse(T) to get the parse tree corresponding to the complete sentence. To avoid crashing due to the function max() in getSentenceParse(), return None if the tree created CYKParse has no key start with S/0 (the sentence does not follow the grammar rules) before passing it to the max() function.
  
Second, I modify the requestInfo dictionary and updateRequestInfo(Tr) to pull out the information that I need for my bot to reply. In updateRequestInfo(), if it finds unknown words, the function will stop immediately.
  
Third, I create getInformation() functions to update the requestInfo.
  
Finally, I implement the reply function depending on the requestInfo.
* repWhatQuestion() : handle what/where/who/ How about/ What about.
* repReactive(): handle Which is [more/less] [reactive/metallic/nonmetallic].
* YesNo() : handle question starts with Is/Does.
* repHowManyQuestion(): handle question starts with ”How many”.
* resetInfo(): reset requestInfo{}.
* checkSymbol(), getinfo(), checkMetal(): get information of elements from datas.

If the chatbot is not capable of answering a user’s question, it will print out a message to notify the user. I hardcoded lists of different ways to respond for greetings, farewells and unexpected input, then use function randint() to randomly reply to the user.

# Example - 1
  ![Screen Shot 2021-08-24 at 10 08 52 PM](https://user-images.githubusercontent.com/48174888/130730115-f2c624df-8c40-4b57-84f3-e7f9e6aa36f1.png)  
    
# Example - 2
 ![Screen Shot 2021-08-23 at 7 29 14 PM](https://user-images.githubusercontent.com/48174888/130546349-75ba46cf-fb63-4194-9d20-7960eb14ebb3.png)
 ![Screen Shot 2021-08-23 at 7 30 53 PM](https://user-images.githubusercontent.com/48174888/130546459-86978cc0-7ec9-47bf-af91-62a4e64c5727.png)

# How to run it?
  On terminal: python3 Proj.py
