import os
import pandas
import praw
from prawcore.exceptions import ResponseException
from keep_alive import keep_alive

reddit=praw.Reddit(                                             #Auhtorization information deleted for security
  user_agent= "<UWBot1.0>" 
)


try:                                                            #Checks authorization details and connects to the Reddit API
    print("Authenticated as {}".format(reddit.user.me())) 
except ResponseException:
    print("Something went wrong during authentication")

subreddit= reddit.subreddit("enghacksinfo")


df= pandas.read_csv('Merged.csv')                               #Read's the UWaterloo CSV file for course information


courses=[]                                                      #Creates arrays to store different values from the CSV file
courseCode=[]
courseDesc={}
commentID=[]

                                                                #Adding infomation into the different arrays from CSV file
for course in df["subjectCode"]:
   courses.append(course)
for course in df["catalogNumber"]:
   courseCode.append(course)

for i in range(len(courses)):
  courses[i]= courses[i]+" "+courseCode[i]


count=0
for course in df["description"]:
   
   if count<=1153:
    courseDesc[courses[count]]=course
    count += 1
    
   else:
     break

for comment in subreddit.stream.comments(skip_existing=True):  #Loops through a reddit comment looking for information

  result = ""                                                  #Normalizes the comment to a recognizable format
  alpha = ""
  num = ""

  for letter in comment.body:
    if letter.isalpha():
      alpha=alpha+letter
    elif letter.isnumeric():
      num = num + letter
  
  result = alpha + " " + num
  result = result.upper()

  TmpCourse = ""
  print(commentID)                                            #prints different results for testing *can be removed*
  print(result)
  print(len(result))
  IsThere = False
  for course in courses: 
    if course == result:
      IsThere = True
      TmpCourse = course
      break
  if comment.id not in commentID and not comment.author == reddit.user.me():
    if (IsThere == True):
      comment.reply(courseDesc[TmpCourse])
      commentID.append(comment.id)
      print("I have replied")
    elif (IsThere == False):
      comment.reply("Course not found, for information on the courses offered at UWaterloo, use this: ecampusontario.ca/?itemTypes=1&itemTypes=2&itemTypes=3&sourceWebsiteTypes=2&institutions=426&sortCol")
      commentID.append(comment.id)
  keep_alive()
