# chat-bot.
Author: Loc Duc Minh Khong

# Introduction
At the school level, students learn basic concepts of many different subjects to develop
a better understanding of the issues and problems around them. However, not all subjects are easy to learn and understand. Many students hate chemistry because it has a lot of information to memorize. One of the first things that students have to learn in chemistry is the periodic table, which is categorized and organized to provide the similarities and properties of the elements. Nevertheless, it requires a lot of time and effort to understand and remember the periodic table. Therefore, for this project, I want to create a chatbot that can answer questions about the periodic table of elements. With the chatbot, they can conveniently recall the information of elements and immediately get an answer to their questions. As a chatbot is like a friend who is always ready to help them, it can make learning not only be more enjoyable but also be more effective.

# Technical Overview
  This project was implemented in Python 3 (ver 3.8.5). It didn't use any APIs and external libraries.
  
# Features

  
# Input Handling
  I used the CYKParse parse the user input and created a tree from the words. I also made the grammar rules and lexicons for some common inputs which I predicted that the user will chat or ask my bot.
  If the input is not in any grammar rules or lexicons, the chatbot will send a message to the user.
  
# Internal Representations and Data Sources
  The data of the periodic table rarely changes and is stable over time, so I do not need to
access any network-available database in real-time. Instead, I will use the data of the periodic table that I have found on the internet. The data has already been written, formatted, and saved in a JSON file (​https://github.com/Bowserinator/Periodic-Table-JSON​ ). As JSON is the string representation of the data, I will convert it to a python dictionary to read the data by using the loads() function of the JSON module.

# Example
 ![Screen Shot 2021-08-23 at 7 29 14 PM](https://user-images.githubusercontent.com/48174888/130546349-75ba46cf-fb63-4194-9d20-7960eb14ebb3.png)
 ![Screen Shot 2021-08-23 at 7 30 53 PM](https://user-images.githubusercontent.com/48174888/130546459-86978cc0-7ec9-47bf-af91-62a4e64c5727.png)






  
 
