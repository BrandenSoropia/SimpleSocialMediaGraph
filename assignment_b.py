#
# Group: c3lamann, c4soropi
#
import unittest

class ProfileNode(object):
    '''A class holding the information of someone's profile which includes,
    name, email, school(s), friend(s). '''
    
    def __init__(self: 'ProfileNode', name: str, email: str, 
                 schools: 'list of str', friends: 'list of str') -> None:
        '''Assign name, email, schools and friends of a person to their 
        node.'''
        
        self.name = name
        self.email = email
        self.schools = schools
        self.friends = friends
        
    def print_profile(self):
        return self.name, self.email, self.schools, self.friends

class SocialNetwork(object):
    '''Class holding profile information extraced from .txt files'''
    
    def __init__(self: 'SocialNetwork') -> None:
        '''Initialize a Social network'''
        self.friends_dict = {}
        self.profiles_list = []
    
    def load_from_file(self: 'SocialNetwork', file: 'file') -> 'graph':
        '''Return a connected graph based off of file.
        
        Precondition: file must be open to read
        '''
        
        name = ''
        email = ''
        schools = ''
        friends = ''
        
        # Take all lines in file, divide them into individual lines by 
        # separating at '\n' and save them.
        data = file.read()
        data = data.split(sep='\n')

        # Go through each line of file.
        for line in data[:-1]:
            # Go through each char in line.
            info = ''
            for char in line:
                # Break apart each line to extract name, profile's email, 
                # schools and friend's emails.
                if char == '<':
                    name = info
                    # Reset info to empty to separate name from email.
                    info = ''
                elif char == '>':                                     
                    email = info
                    # Reset info to empty to separate email from schools.
                    info = ''
                # Don't concatenate the '(' bracket.
                elif char == '(':
                    continue
                elif char == ')':
                    schools = info
                    # Reset info to empty to separate schools from friends.
                    info = ''
                # Don't concatenate the ':'.
                elif char == ':':
                    continue
                else:
                    # Saves each char in a variable until one of the separator 
                    # symbols are found. 
                    info = info + char
            # Once you go through the entire line, the friend email(s) are
            # not assigned to the friends var. Therefore assign them now.            
            friends = info
            
            # Assign the separeated data to create a person's Profile. 
            # Splits strings containing name(s) of friends/schools
            # into a list.
            profile = ProfileNode(name, email, schools.split(sep=','), 
                                  friends.split(sep=','))
            
            # Use email to make a key in dicitonary to store their friends
            self.friends_dict[email] = friends.split(sep=',')
            # Store all profiles in a list
            self.profiles_list.append(profile)
            
        # Makes sure that friendships are made mutual
        for email in self.friends_dict:
            maintain_mutual_friendship(self, email)
            # Update the person's profile friends list as well
            profile = self._profile_finder(email)
            profile.friends = self.friends_dict[email]
            
    def friends(self: 'SocialNetwork', person: str) -> str:
            '''Return a list of person's friends seperated by spaces in 
            alphabetical order. Return empty line if none.
            
            Pre-condition: person must be person's email
            
            >>> friends harold@alias.me
        
            >>> friends hl@imaeatchu.com
            Annie Dr. Evil
            >>> friends andy@toronto.edu
            Brian Law
            '''
            name_list = []
            friend_list = self.friends_dict[person]
            if friend_list == ['']:
                return ''
            else:
                for friend in friend_list:
                    # Takes friends emails into names
                    for profile in self.profiles_list:
                        if profile.email == friend:
                            name_list.append(profile.name)
                            
            name_list.sort()
            # Takes name_list and forms a string of its contents
            return string_maker(name_list)                     
                 
    def degree_between(self: 'SocialNetwork', person1: str, person2: str) -> int:
            '''Return the number of edges on the shortest path between person1 
            and person2. Separation to oneself is always 0 and inf if no path
            at all.
                    
            Pre-condition: person must be person's email
                    
            >>> degree liudavid@cdf.toronto.edu henry@hyde.net
            2
            >>> degree harold@alias.me andy@toronto.edu
            inf
            >>> degree harold@alias.me harold@alias.me
            0
            '''
            
            # Used to avoid counting person1 in future depth search
            people_checked = []
            depth_list = []
            # Check if person even exists in graph
            if person1 not in self.friends_dict or person2 not in \
               self.friends_dict:
                return float('inf')
            # Store friends of each person 
            person1_friends = self.friends_dict[person1]
            person2_friends = self.friends_dict[person2]                
            

            # There is no depth between the same person        
            if person1 == person2:
                return 0
            
            # If one of them doesn't have friends, then it is impossible to  
            # find a path to them
            if person1_friends == [''] or person2_friends == ['']:
                return float('inf')
            
            # Checks to see if person1 and 2 are friends (1 edge away only)
            if person2 in person1_friends:
                return 1
                    
            depth = 1
            cur_depth = [person1]
            next_depth = []
            
            while True:
                for item in cur_depth:                   
                    # See if person2 is here and item hasn't been checked yet
                    if person2 in self.friends_dict[item]:
                        return depth
                    else:
                        for person in self.friends_dict[item]:
                            if person not in people_checked:
                                next_depth.append(person)
                                # Keep track of who you've checked
                                people_checked.append(person)
                        cur_depth = next_depth
                        next_depth = []
                depth += 1
 
    def people_with_degree(self: 'SocialNetwork', person: str, deg_of_sep: int) -> str:
            '''Return a str of people in alphabetical order that are exactly
            deg_of_sep away from person.
            
            Pre-condition: person must be person's email
                    
            '''
            
            if deg_of_sep == 0:
                profile = _profile_finder(person)
                return profile.name
            
            people_within_degree = []
            
            # Go through everyone in SocialNetwork to find their degree of 
            # separation.
            for profile in self.profiles_list:
                # Returns the smallest degree of separation between the two
                deg = self.degree_between(person, profile.email)
                # If the degree is the same as given, append the name to list
                if deg == deg_of_sep:
                    people_within_degree.append(profile.nameS)
            
            # Sort list in alpabetical order.
            people_within_degree.sort()
            # Take the list and put it in alphabetical order and return as
            # a string with each name separated by a space
            return string_maker(people_within_degree)            
        
    def mutual_friends(self: 'SocialNetwork', person1: str, 
                       person2: str) -> str:
            '''Return a string of mutual friends between person1 and person 2 
            in alphabetical order.
            
            Pre-condition: person must be person's email
            
            '''
            
            mutual_friends_list = []
            #sorted_friends = ''
            
            # Go through person1's friends if not empty
            if self.friends_dict[person1] != ['']:
                for mutual_friend in self.friends_dict[person1]:                
                    # See if any of person1's friends are in person2's friend
                    # list, if person2's friends list is not empty
                    if self.friends_dict[person2] != [''] and \
                       mutual_friend in self.friends_dict[person2]:
                        # If so, append their name to the list
                        profile = self._profile_finder(mutual_friend)
                        mutual_friends_list.append(profile.name)
                        
            return string_maker(mutual_friends_list)    
            
    def likely_friends(self: 'SocialNetwork', person: str) -> str:
            '''Return the likeliest missing friend(s) of person based on who
            shares the most mutual friends with person, in alphabetical order.
            
            Pre-condition: person must be person's email
            
            '''
            
            potential_friends_dict = {}
            most_likely = []
            max_score = 0
            
            if self.friends_dict[person] != ['']:
                # Go through person's friends
                for friend in self.friends_dict[person]:     
                    # Go through all friends of friend
                    for potential_friend in self.friends_dict[friend]:
                        # Check if already friend or if friend is person
                        if potential_friend not in self.friends_dict[person] \
                           and potential_friend != person:
                            # Create a key in dict
                            if potential_friend not in potential_friends_dict:
                                potential_friends_dict[potential_friend] = 1
                            # Increase likely friend score if key exists
                            else:
                                potential_friends_dict[potential_friend] += 1
                     
            # Go through dict to find the highest likely friend score and
            # append to most_likely
            for potential_friend in potential_friends_dict:
                # If potential_friend score is higher than current max_score, 
                # change max_score to it and reassign to most_likely
                if potential_friends_dict[potential_friend] > max_score:
                    most_likely = [potential_friend]
                    max_score = potential_friends_dict[potential_friend]
                # If potential_friend score is equal to max_score, append to 
                # most_likely
                elif potential_friends_dict[potential_friend] == max_score:
                    most_likely.append(potential_friend)
            
            # Change email's into names
            for i in range(len(most_likely)):
                for profile in self.profiles_list:
                    if most_likely[i] == profile.email:
                        # Replace email with person's name
                        most_likely[i] = profile.name
                        
            # Sort alphabetically
            most_likely.sort()
            
            return string_maker(most_likely)
            
    def classmates(self: 'SocialNetwork', person: str, depth: int) -> str:
        '''Return a list of all people in the same class as person within 
        depth.
        
        Pre-condition: person is an email.
        
        '''
        
        classmates = []
        person_profile = self._profile_finder(person)
        
        # Check if person has any connections to look for classmates
        if person_profile.friends != ['']:
            # Loop over his friends to check their schools
            for friend in person_profile.friends:
                classmates = self._classmates(friend, depth, 
                                              person_profile.schools) 
        
        # If the list is empty
        if classmates == []:
            return ''        
        
        # Switch emails with their names
        for i in range(len(classmates)):
            classmates[i] = self._profile_finder(classmates[i]).name
            
        # Sort list alphabetically    
        classmates.sort()
        
        # Remove the person's name from the classmates list.
        classmates.remove(person_profile.name)
                 
        return string_maker(classmates)
        
    def _classmates(self: 'SocialNetwork', person: str, depth: int,
                    persons_schools: 'list of str') -> list:
        '''Return a list of all people in the same class as person within 
        depth.
        
        Pre-condition: person is an email.
        
        '''
                
        classmate_list = []
        cleaned_classmate_list = []
        
        # Find the person's profile
        profile_of_person = self._profile_finder(person)
        
        list_of_friends = profile_of_person.friends
        friends_schools = profile_of_person.schools
        
        # Check if person went to school
        if friends_schools == ['']:
            return []
        
        # Stop if depth when depth is reached or if the person has no friends
        if int(depth) == 0 or profile_of_person.friends == ['']:
            return classmate_list
        
        # Go through schools
        for school in friends_schools:            
            # Check if friend's schools is one of person's schools
            if school in persons_schools and person not in classmate_list:
                classmate_list.append(person)

        # recurse through friends of friends
        for friend in list_of_friends:
            recurse_function = self._classmates(friend, int(depth)-1, 
                                                persons_schools)
            classmate_list = classmate_list + recurse_function
        
        # Clean up classmante_list for multiple copies of names
        for email in classmate_list:
            if email not in cleaned_classmate_list:
                cleaned_classmate_list.append(email)

        return cleaned_classmate_list
                
    def _profile_finder(self: 'SocialNetwork', person: str) -> str: 
        '''Return person's profile.'''
        # Find person's profile.
        for profile in self.profiles_list:
            if profile.email == person:
                return profile

# Helper Functions
def maintain_mutual_friendship(graph: 'SocialNetwork', person: str) -> None:
    '''Check friends of person to see if person is included in their
    own friends list and add them if not there.
    
    Pre-condition: person should be a person's email.'''
    
    # Check if they even have friends
    if graph.friends_dict[person] != ['']:
        # Go through all of person's friends
        for friend in graph.friends_dict[person]:
            # Check if person is in their friend's friend list
            if person not in graph.friends_dict[friend]:
                # If the person didn't have any friends before hand, replace
                # empty list with friend
                if graph.friends_dict[friend] == ['']:
                    graph.friends_dict[friend] = [person]
                # Otherwise, append to list
                else:
                    graph.friends_dict[friend].append(person)
                    
                    
def string_maker(list: list) -> str:
    '''Return a string containing all the items in list separated by spaces
    
    Pre-condition: list is sorted.
    
    '''
    
    sorted_friends = ''
    
    for item in list:
            # If string is empty, concatenate without space
            if sorted_friends == '':
                sorted_friends = sorted_friends + item 
            # If string is not empty, concatenate with a space between 
            # existing str and the new name
            else:
                sorted_friends = sorted_friends + ' ' + item
    
    return sorted_friends

# GRAPHS FOR ALL TEST CASES #

# Graph with a single node (no friends) only and no schools 
schooless_single_node_graph = SocialNetwork()
schooless_single_node_graph.friends_dict = {'totoro@ghibli.jp': ['']}
schooless_single_node_graph.profiles_list = [ProfileNode('Totoro', 'totoro@ghibli.jp', [''],[''])]  

# Graph with 2 nodes Connected
graph_with_2_nodes = SocialNetwork()
graph_with_2_nodes.friends_dict = {'totoro@ghibli.jp': ['mae.kusakasbe@ghibli.jp'], 'mae.kusakasbe@ghibli.jp': ['totoro@ghibli.jp']}
mae_kusakabe = ProfileNode('Mae Kusakabe', 'mae.kusakasbe@ghibli.jp', ['SomeSchool'], ['totoro@ghibli.jp'])
totoro = ProfileNode('Totoro', 'totoro@ghibli.jp', ['UofT'], ['mae.kusakasbe@ghibli.jp'])
graph_with_2_nodes.profiles_list = [totoro, mae_kusakabe]

# Graph with 2 nodes that are unconnected, multi schools
unconnected_pair_graph = SocialNetwork()
unconnected_pair_graph.friends_dict = {'totoro@ghibli.jp': [''], 'mae.kusakasbe@ghibli.jp': ['']}
mae_kusakabe = ProfileNode('Mae Kusakabe', 'mae.kusakasbe@ghibli.jp', ['SomeSchool'], [''])
totoro = ProfileNode('Totoro', 'totoro@ghibli.jp', ['UofT'], [''])
graph_with_2_nodes.profiles_list = [totoro, mae_kusakabe]

# Graph containing a connected pair and a lone node, multi schools 
pair_and_loner_graph = SocialNetwork()
pair_and_loner_graph.friends_dict = {'totoro@ghibli.jp': ['mae.kusakasbe@ghibli.jp'], 'mae.kusakasbe@ghibli.jp': ['totoro@ghibli.jp'], 'kanta@ghibli.jp': ['']}
mae_kusakabe = ProfileNode('Mae Kusakabe', 'mae.kusakasbe@ghibli.jp', ['SomeSchool'], [''])
totoro = ProfileNode('Totoro', 'totoro@ghibli.jp', ['UofT'], [''])  
kanta = ProfileNode('Kanta Okagi', 'kanta@ghibli.jp', ['SomeSchool'], [''])
graph_with_2_nodes.profiles_list = [totoro, mae_kusakabe, kanta]

# Jonathan's Graph from the assignment B handout updated to make friendships
# friendships mutual

anya = ProfileNode('Anya Tafliovich', 'anya@cdf.toronto.edu', ['University of Toronto'], ['sengels@cdf.toronto.edu', 'liudavid@cdf.toronto.edu', 'henry@hyde.net'])
engels = ProfileNode('Steve Engels', 'sengels@cdf.toronto.edu', ['Urban Technical School', 'University of Waterloo'], ['liudavid@cdf.toronto.edu', 'lungj@cdf.toronto.edu', 'anya@cdf.toronto.edu'])
liu = ProfileNode('David Liu', 'liudavid@cdf.toronto.edu', ["Queen's University", 'University of Toronto', 'Urban Technical School'], ['anya@cdf.toronto.edu', 'sengels@cdf.toronto.edu', 'blaw@cdf.toronto.edu', 'lungj@cdf.toronto.edu'])
mr_fancy_pants = ProfileNode('Jonathan Lung', 'lungj@cdf.toronto.edu', ['Urban Technical School', 'University of Toronto'], ['sengels@cdf.toronto.edu', 'liudavid@cdf.toronto.edu', 'blaw@cdf.toronto.edu'])
finch = ProfileNode('Harold Finch', 'harold@alias.me', [''], [''])
blaw = ProfileNode('Brian Law', 'blaw@cdf.toronto.edu', ['Urban Technical School', 'University of Waterloo', 'University of Toronto'], ['andy@toronto.edu', 'lungj@cdf.toronto.edu', 'liudavid@cdf.toronto.edu', 'dr@evil.net'])
evil = ProfileNode('Dr. Evil', 'dr@evil.net', ["Queen's University", 'University of Waterloo', 'Evil Medical School'], ['blaw@cdf.toronto.edu', 'henry@hyde.net', 'hl@imaeatchu.com'])
annie = ProfileNode('Annie', 'annie@mgo.org', ['School of Hard Knocks'], ['henry@hyde.net', 'hl@imaeatchu.com'])
jekyll = ProfileNode('Henry Jekyll', 'henry@hyde.net', ['Evil Medical School'], ['annie@mgo.org', 'dr@evil.net', 'anya@cdf.toronto.edu'])
hannibal = ProfileNode('Hannibal Lecter', 'hl@imaeatchu.com', ['Evil Medical School', 'School of Hard Knocks'], ['annie@mgo.org', 'dr@evil.net'])
andy = ProfileNode('Andy Hwang', 'andy@toronto.edu', ['University of Toronto', 'University of Waterloo'], ['blaw@cdf.toronto.edu'])
dfinn = ProfileNode('Dewey Finn', 'dfinn2003@gmail.com', ['School of Rock'], ['principal@gppr.edu'])
mullins = ProfileNode('Rosalie Mullins', 'principal@gppr.edu', ['School of Rock'], ['dfinn2003@gmail.com'])    

jono_graph = SocialNetwork()
jono_graph.friends_dict = {'liudavid@cdf.toronto.edu': ['anya@cdf.toronto.edu', 'sengels@cdf.toronto.edu', 'blaw@cdf.toronto.edu', 'lungj@cdf.toronto.edu'], 'dr@evil.net': ['henry@hyde.net', 'hl@imaeatchu.com', 'blaw@cdf.toronto.edu'], 'harold@alias.me': [''], 'henry@hyde.net': ['annie@mgo.org', 'dr@evil.net', 'anya@cdf.toronto.edu'], 'dfinn2003@gmail.com': ['principal@gppr.edu'], 'andy@toronto.edu': ['blaw@cdf.toronto.edu'], 'lungj@cdf.toronto.edu': ['sengels@cdf.toronto.edu', 'liudavid@cdf.toronto.edu', 'blaw@cdf.toronto.edu'], 'principal@gppr.edu': ['dfinn2003@gmail.com'], 'hl@imaeatchu.com': ['annie@mgo.org', 'dr@evil.net'], 'annie@mgo.org': ['henry@hyde.net', 'hl@imaeatchu.com'], 'sengels@cdf.toronto.edu': ['liudavid@cdf.toronto.edu', 'lungj@cdf.toronto.edu', 'anya@cdf.toronto.edu'], 'anya@cdf.toronto.edu': ['sengels@cdf.toronto.edu', 'liudavid@cdf.toronto.edu', 'henry@hyde.net'], 'blaw@cdf.toronto.edu': ['andy@toronto.edu', 'lungj@cdf.toronto.edu', 'liudavid@cdf.toronto.edu', 'dr@evil.net']}
jono_graph.profiles_list = [anya, engels, liu, mr_fancy_pants, finch, blaw, evil, annie, jekyll, hannibal, andy, dfinn, mullins]

# Graph of 3 nodes, all connected n a straigh line as follow: 
# NodeA <-> NodeB <-> NodeC

linear_node_graph = SocialNetwork()
linear_node_graph.friends_dict = {'anya@cdf.toronto.edu': ['liudavid@cdf.toronto.edu'], 'liudavid@cdf.toronto.edu': ['anya@cdf.toronto.edu', 'blaw@cdf.toronto.edu'], 'blaw@cdf.toronto.edu': ['liudavid@cdf.toronto.edu']}
anya2 = ProfileNode('Anya Tafliovich', 'anya@cdf.toronto.edu', ['University of Toronto'], ['liudavid@cdf.toronto.edu'])
liu2 = ProfileNode('David Liu', 'liudavid@cdf.toronto.edu', ['University of Toronto'], ['anya@cdf.toronto.edu', 'blaw@cdf.toronto.edu'])
blaw2 = ProfileNode('Brian Law', 'blaw@cdf.toronto.edu', ['University of Toronto'], ['liudavid@cdf.toronto.edu'])
linear_node_graph.profiles_list = [anya2, liu2, blaw2]    
 
# Graph of 3 nodes all connected to form a triangle
 
tri_graph = SocialNetwork()
tri_graph.friends_dict = {'anya@cdf.toronto.edu': ['sengels@cdf.toronto.edu', 'liudavid@cdf.toronto.edu'], 'sengels@cdf.toronto.edu': ['liudavid@cdf.toronto.edu', 'anya@cdf.toronto.edu'], 'liudavid@cdf.toronto.edu': ['anya@cdf.toronto.edu', 'sengels@cdf.toronto.edu']}
anya3 = ProfileNode('Anya Tafliovich', 'anya@cdf.toronto.edu', ['University of Toronto'], ['sengels@cdf.toronto.edu', 'liudavid@cdf.toronto.edu'])
engels2 = ProfileNode('Steve Engels', 'sengels@cdf.toronto.edu', ['University of Toronto'], ['anya@cdf.toronto.edu', 'liudavid@cdf.toronto.edu'])
liu3 = ProfileNode('David Liu', 'liudavid@cdf.toronto.edu', ['University of Toronto'], ['anya@cdf.toronto.edu', 'sengels@cdf.toronto.edu'])
tri_graph.profiles_list = [anya3, engels2, liu3]

class TestDegreeBetween(unittest.TestCase):
    '''Test the degree_between metoh of SocialNetwork.'''
    
    def test_degree_between_single_node_self_target(self):
        '''Test degree_between on a graph with a single node looking starting at
        person1 looking for person1.'''
    
        self.assertEqual(schooless_single_node_graph.degree_between('totoro@ghibli.jp', 'totoro@ghibli.jp'), 0)
        
    def test_degree_between_single_node_unexisting_target(self):
        '''Test degree_between on a graph with a single node looking for an 
        non-existing person2.'''
        
        self.assertEqual(schooless_single_node_graph.degree_between('totoro@ghibli.jp', 'dr@evil.net'), float('inf'))
        
    def test_degree_between_connected_pair(self):
        '''Test degree_between on a graph with a 2 connected nodes looking for 
        a person2 with friends starting at person1 with friends'''
        
        self.assertEqual(graph_with_2_nodes.degree_between('totoro@ghibli.jp', 'mae.kusakasbe@ghibli.jp'), 1)
        
    def test_degree_between_unconnected_pair(self):
        '''Test degree_between on graph with 2 unconnected nodes looking for 
        person2 (no friends) starting at a person1 (no friends).'''
        
        self.assertEqual(unconnected_pair_graph.degree_between('totoro@ghibli.jp', 'mae.kusakasbe@ghibli.jp'), float('inf'))
        
    def test_degree_between_connected_pair_and_loner_node_no_path(self):
        '''Test degree_between on graph with 2 unconnected nodes and a 
        lone node with person1 haveing friends and person having none.'''
        
        self.assertEqual(pair_and_loner_graph.degree_between('totoro@ghibli.jp', 'kanta@ghibli.jp'), float('inf'))
        
        
    def test_degree_between_connected_pair_and_loner_node_connected_path(self):
        '''Test degree_between on graph with 2 unconnected nodes and a lone node 
        looking for other member of the connected pair starting at a connected 
        node.'''  
        
        self.assertEqual(pair_and_loner_graph.degree_between('totoro@ghibli.jp', 'mae.kusakasbe@ghibli.jp'), 1)
        
    def test_linear_1(self):
            ''' Test to find the degree between two people in a linear graph.
            Both people have friends.'''
           
            self.assertEqual(linear_node_graph.degree_between('anya@cdf.toronto.edu', 'blaw@cdf.toronto.edu'), 2)
    
    def test_triconnected(self):
        ''' Test to find the degree between two people in a triangular
        connected graph. All friends are friends with each other. '''
       
        self.assertEqual(tri_graph.degree_between('anya@cdf.toronto.edu', 'liudavid@cdf.toronto.edu'), 1)
   
    def test_linear_2(self):
        ''' Test to find the degree between two people in a linear graph.
        Both people have friends.'''
       
        self.assertEqual(linear_node_graph.degree_between('anya@cdf.toronto.edu', 'liudavid@cdf.toronto.edu'), 1)
   
    def test_jono_graph(self):
        ''' Test to find the degree between two people in a large graph.
        Both people have friends.'''
       
        self.assertEqual(jono_graph.degree_between('liudavid@cdf.toronto.edu', 'lungj@cdf.toronto.edu'), 1)  
         
    
if __name__ == '__main__':
    unittest.main()