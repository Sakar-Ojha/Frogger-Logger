"""
File:        frogger.py
Author:      Sakar Ojha
Date:        11/19/2024
Section:     71
E-mail:      o66@umbc.edu
Description: A game of frogger without the logs part
Secret Word: Pusillanimous
"""
import os

root, directories, files = next(os.walk('.'))

#----------------------------------------------------------------------------------------
def update_frog_position(move_command, frog_position, len_col):
      '''
      Function updates the new frog position based on the users input of WASD
      Parameters: 
      move_command takes in 'w' , 'a', 's', 'd' any one of those
      frog_position takes the position of frog in array [row, col]
      len_col is the length of the column
      Returns: updated frog_position variable
      '''
      if move_command == "W":
            if frog_position[0] == -1:
                  print('Not a valid move at this position.')
            else:
                  frog_position[0] -= 1

      elif move_command == "S":
            frog_position[0] += 1

      elif move_command == "A":
            if frog_position[1] <= 0:
                  print('Out of bounds on the left.')
            else:
                  frog_position[1] -= 1

      elif move_command == "D":
            if frog_position[1] == len_col-1:
                  print('Out of bounds on the left.')
            else:
                  frog_position[1] += 1

      return frog_position
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
def rotate_all_lanes(highway, speed):
      '''
      Function will rotate any matrix given into it, it is linked
        with the lane_rotation function to do the rotation task
      Parameters:
      highway is the old rotated list of lists that will be passed onto it.
      speed is also a list consisting of speed respective to each row in ascending order.
      Example: speed = [1,3,2] speed 1 is associated with row 1, speed 3 is row 2....
      Returns: the rotated matrix
      '''
      updated_highway = []
      for i in range(len(highway)):
           rotated_lane = rotate_one_lane(highway[i], speed[i])
           updated_highway.append(rotated_lane)

      return updated_highway
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
def rotate_one_lane(lane, rotation_speed):
      '''
      Function rotates any row passed, with appropriate speed
      Parameters : lane, rotation_speed
      lane is a list containing elements of a certain row
      rotation_speed takes in the speed of the rotation
      Returns: rotated lane after applying the lane speed
      '''
      rotated_lane = lane[len(lane)-rotation_speed:] +  lane[:len(lane)-rotation_speed]

      return rotated_lane
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
def jump(user_input, frog_position, available_jumps, num_columns):
      '''
      Function checks if the jump the user wants to make is valid.      
      Parameter:
      Function takes in the users_input, the previous position of the frog 
      before the jump, and available jumps left as well as the num_colmns. 
      Returns: the new position of the frog based on the jump.   
      '''
      if available_jumps == 0:
            print('There is no jumps left.')
            return frog_position, available_jumps

      # Splitting user input into every character parts. for ex[j,2,4]
      list_parts = user_input.split()

      user_input_row = int(list_parts[1]) # First index = row
      user_input_col = int(list_parts[2]) # Second Index = column

      #Checking the bounds of the input to validate it
      if (user_input_row-1 > (frog_position[0] + 1)) or (user_input_row-1 < (frog_position[0] - 1)):
            print('You can only jump one row at a time!')
            return frog_position, available_jumps
      elif (user_input_col > num_columns) or (user_input_col < 1):
           print('Column is out of range!')
           return frog_position, available_jumps
      elif (user_input_row < 0):
           print('Cannot go upwards!')
           return frog_position, available_jumps
      else:
           new_frog_position = [user_input_row-1, user_input_col-1]
           return new_frog_position, available_jumps-1 #available jumps is subtracted once
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
def printing_board(frog_position, frog_symbol, highway):
      '''
      Function is going to print the frog at its designated place.
      Parameters: 
      Frog position takes in frogs position in a list with the first
      index being row and second column.
      highway is the original list copy and later on will be rotated as it is sent
      Returns: None
      '''
      if (frog_position[0] == -1):
            for i in range(frog_position[1]):
                  print(' ',end='')
            print(frog_symbol)

      for row in range(len(highway)):
            for column in range(len(highway[0])):
                  if ((row == frog_position[0] and column == frog_position[1])\
                      and (frog_position[0] != -1)):
                        print(frog_symbol, end='')
                  else:
                        print(highway[row][column], end='')
            print()
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
def get_game_data(game_file):
      '''
      Gets all the games data like the amount of jumps available, the speed of each lanes
       and the highway
      Parameters: game_file which is the name of the selected game file
      Returns: available_jumps, lanes_speed, highway
      '''
      file_contents = open(game_file, 'r') #opens the file in read mode
      
      # strip off the last \n character and make it into a list split by whitespace
      first_line  = ((file_contents.readline()).strip()).split()
      second_line = ((file_contents.readline()).strip()).split()

      available_jumps = int(first_line[2])

      lanes_speed = []
      # Looping through the elements, changing them to integers, and appending them to lanes_speed
      for speed in second_line:
            lanes_speed.append(int(speed))

      highway = []
      # Append to the list highway, by looping row times
      for i in range(int(first_line[0])):
           line = ((file_contents.readline()).strip())
           highway.append(line)

      return available_jumps, lanes_speed, highway
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
def frogger_game(game_file):
      '''
      Runs the game
      Parameter: 
      game_file which is name of the game file selected
      Returns:None
      '''
      frog_symbol = '\U0001F438'
      dead_frog_symbol = '\U0001F480'
      available_jumps, lanes_speed, highway = get_game_data(game_file)

      len_column = len(highway[0])

      frog_y_initial = -1     # This means the frog has not entered the highway yet
      frog_position  = [frog_y_initial, len_column // 2]
      
      game = 'on'

      while game != 'over':
            # Calling funciton printing_board to print the frog position and the board
            printing_board(frog_position, frog_symbol, highway)

            move_command = input('WASD: ').upper()    
            valid_inputs = 'WASD'

            while (move_command not in valid_inputs) and ('J' not in move_command):
                  print('Not a valid input, Try again: ', end = " ")
                  move_command = input().upper()

            if 'J' in move_command: # If jump is chosen
                  frog_position, available_jumps = jump(move_command, frog_position, available_jumps, len_column)

            else: #WASD input
                  frog_position = update_frog_position(move_command, frog_position, len_column)

            # Calling function to rotate the matrix and assigning it to variable rotated_matrix
            highway = rotate_all_lanes(highway, lanes_speed)

            # Assigning the output of the frog_position function into row and column variables
            frog_row, frog_column = frog_position

            if (frog_row > len(highway)-1): #Meaning we reached the end of the row
                  printing_board(frog_position, frog_symbol, highway)
                  for i in range (frog_position[1]):
                        print(' ', end = '')
                  print(frog_symbol)
                  print('Frog lives to cross another day.')
                  
                  game = 'over'

            #-----------Frogger Only---------------
            elif (frog_row != frog_y_initial) and (highway[frog_row][frog_column] != '_'):
                  game = 'over'
                  printing_board(frog_position, dead_frog_symbol, highway)
                  print('Got Killed')

            #-----------Logger Only---------------
            # elif (frog_row != frog_y_initial) and (highway[frog_row][frog_column] == '_'):
            #       game = 'over'
            #       printing_board(frog_position, dead_frog_symbol, highway)
            #       print('Got Killed')

            #--------Logger and Frogger---------
            # logger = True
            # if (not logger):
            #       if (frog_row != frog_y_initial) and (highway[frog_row][frog_column] != '_'):
            #             game = 'over'
            #             printing_board(frog_position, dead_frog_symbol, highway)
            #             print('Got Killed')
            # else:
            #       if (frog_row != frog_y_initial) and (highway[frog_row][frog_column] == '_'):
            #             game = 'over'
            #             printing_board(frog_position, dead_frog_symbol, highway)
            #             print('Got Killed')

#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
def select_game_file():
      '''
      Shows all the files in the current directory
      No Parameters
      Returns the file selected by the user
      '''
      # Remove .py file from "files" so that all the files in the directory is displayed...
      # ...except frogger.py
      for file in files:
            if ".py" in file:
                  files.remove(file) 

      # Carefully prints out all the files elements without raising index errors
      for i in range(1, len(files) + 1):
            print(f'[{i}] {files[i-1]}')
      
      file_option = int(input('Enter an option: '))
      while (file_option > len(files)) or (file_option <= 0): # Checks for userinputs validity
            file_option = int(input('Invalid option, Enter again: '))

      selected_game_file = files[file_option - 1] # game file is the file_option index - 1

      return selected_game_file
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
if __name__ == '__main__':
      selected_game_file = select_game_file()
      frogger_game(selected_game_file)