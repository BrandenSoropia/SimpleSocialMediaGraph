# SimpleSocialMediaGraph
DISCLAIMER: assignment_b_driver source code given by professor, none of it was my work. 

Instructions:
  1) Put all .py files and formatted txt files in same folder
  2) Run assignment_b_driver.py
  3) Input command as follows:
    >>>command_name param_1 (param_2) 

Graph based social media simulator implemented in Python 3. 
Populates graph from specially formatted given txt file. Each profile has their information stored on their own line (new lines separate profiles) with the following format:

  NAME\<email\>(educational institutes):friend's_email
  
  ex: 
    Dr. Evil\<dr@evil.net\>(Queen's University,University of Waterloo,Evil Medical School):hl@imaeatchu.com
    Hannibal Lecter\<hl@imaeatchu.com\>(Evil Medical School,School of Hard Knocks):dr@evil.net
    
  Note: it is possible for a person to be friends with someone but that friend is not friends them back
  
This program can:
  1) List a person's friends
  2) Find the degree between profiles (or infinite if to self)
    - however can't work when searching for a path that doesn't exist
  3) List all people exactly "n" people away
  4) List mutual friends between 2 people (empty if no mutual friends)
  5) Make friend suggestions based on mutal friends
  6) List people with similar educational institutions with "n" depth
    - however doesn't work with depth 1
  
