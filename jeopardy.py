import pandas as pd
from datetime import datetime
import random

pd.set_option('display.max_colwidth', -1)

jeopardy_df = pd.read_csv("C:\\Users\\Ghisl\\New folder\\jeopardy.csv")

jeopardy_df.columns = ['show_num', 'date', 'round', 'category', 'value', 'question', 'answer']
jeopardy_df['value'] = jeopardy_df.value.str.lstrip('$')
jeopardy_df['value'] = jeopardy_df.value.str.replace(',','')
jeopardy_df['value'] = jeopardy_df.value.str.replace('None','0')
jeopardy_df['value'] = pd.to_numeric(jeopardy_df.value)


day = lambda x:datetime.strptime(x, "%Y-%m-%d")
jeopardy_df['date'] = jeopardy_df.date.apply(day)

jeopardy_df['decade']= ((pd.DatetimeIndex(jeopardy_df['date']).year)//10)*10


#Write a function that filters the dataset for questions that contains all of the words in a list of words. 
#For example, when the list ["King", "England"] was passed to our function, Every row had the strings "King" and "England" somewhere in its " Question".
# Step 1 : concatenate string to create a regex
def concat(liste):
    new_string = ''
    for i in liste:
        new_string += '(?=.*'+i+')'
    return new_string

#Step 2 : filter
def filter_func(liste, df):
    mots = concat(liste)
    new_df = df[df.question.str.contains(mots, case = False, regex=True)]
    return new_df


#what is the average value of questions that contain the word "King"?
filtered_df = filter_func(['king'], jeopardy_df)
average = filtered_df.value.mean()
#print(average)

#Write a function that returns the count of the unique answers to all of the questions in a dataset. 
# For example, after filtering the entire dataset to only questions containing the word "King", we could then find all of the unique answers to those questions. 
# The answer “Henry VIII” appeared 3 times and was the most common answer.
result = filtered_df.groupby('answer').show_num.count()
print(result)


#Investigate the ways in which questions change over time by filtering by the date. 
#How many questions from the 90s use the word "Computer" compared to questions from the 2000s?

filtered_df_2 = filter_func(['computer'], jeopardy_df)
result_2 = filtered_df_2.groupby('decade').show_num.count()
#print(result_2)


#Build a system to quiz yourself. Grab random questions, and use the input function to get a response from the user. Check to see if that response was right or wrong.
def random_question(df):
    yes_or_no = 'yes'
    correct = 0
    incorrect = 0
    while (yes_or_no == 'yes'):
        random_index = random.randint(1, len(df))
        print(df.question[random_index])
        x = input()
        if (x.lower() == df.answer[random_index].lower()):
            correct +=1
            print('Correct ! You have '+ str(correct) + ' correct answers and ' + str(incorrect) + ' incorrect answers')
        else:
            incorrect +=1
            print('Incorrect ! the right answer is '+ df.answer[random_index].lower())
            print('You have '+ str(correct) + ' correct answers and ' + str(incorrect) + ' incorrect answers')
        print('Do you want to answer another question ?')
        y = input()
        if (y.lower()=='yes'):
            yes_or_no = 'yes'
        else:
            yes_or_no = 'no'

random_question(jeopardy_df)