# JSON Library
import json

# Math Library
import math

# System Library
import sys

# config Library
import config

# Calculate probability for 'a' to beat 'b'
def prob(a,b):

  # Returns probability of 'a' beating 'b'
  return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (a - b) / 400))

# Calculate rating change 'a' vs 'b'
def rating(Rw, Rl, K):

  # Probability of winner 'w' beating loser 'l'
  Pw = prob(Rl, Rw)

  # Probability of loser 'l' beating winner 'w'
  Pl = prob(Rw, Rl)

  # Increase winner "w"'s rating
  Rw = Rw + K * (1 - Pw)

  # Decrease loser "l"'s rating
  Rl = Rl + K * (0 - Pl)

  # Return winner, loser
  return (Rw, Rl)

def build_json(content):

  # Top-Sorted List of Users, Ratings
  # Index 1: User Name
  # Index 2: User Rating

  ratings = {}

  # Loop over all of the matches in the tournament
  for match in content:

    # Split the index into elements

    # Round, Winner, Loser
    rnd, winner, loser = match

    # If winner not in ratings
    if winner not in ratings.keys():

      # Create the default
      # ranking for the user
      ratings[winner] = {
        'name': winner, 
        'rating': config.default
      }

    # Get the winner's rating
    Rw = ratings[winner]['rating']

    # If loser not in ratings  
    if loser not in ratings.keys():

      # Create the default
      # ranking for the user
      ratings[loser] = {
        'name': loser, 
        'rating': config.default
      }

    # Get the loser's rating
    Rl = ratings[loser]['rating']

    # Get the updated winner and loser rankings
    Rw, Rl = rating(Rw, Rl, config.constant)

    # Update the winner and loser rankings in the table
    ratings[winner]['rating'] = Rw
    ratings[loser]['rating'] = Rl

  # Return the sorted ratings
  return ratings

def build_txt(ladder):

  # List of elements
  li = []

  # Loop over all the keys in the list
  for key in ladder.keys():

    value = ladder[key]

    # Add the row to the list
    li.append((value['name'], value['rating']))

  # Sort the list in descending order, on the elo rating
  li_sorted = sorted(li, key=lambda x:x[1],reverse=True)

  # Lines we will write to the file
  # Once all lines have been added, 
  # we will join the array with '\n'
  # characters.

  lines = []

  # Loop over all of the items in the ladder
  for i in range(len(li_sorted)):

    # Add the line to the list of lines
    # Example: 1: Damon Murdoch, 1301.220
    lines.append(str(i + 1) + ": " + str(li_sorted[i][1]) + ", " + str(li_sorted[i][0]))

  # Return the array joined on newline characters
  return "\n".join(lines)

if __name__ == '__main__':

  # List of files to calculate elo for
  files = []

  # If there are any arguments
  if len(sys.argv) > 1:

    # Get all entries after the first
    files = sys.argv[1:]

    # Loop over the files
    for filename in files:

      # Open the file
      with open(filename, 'r') as f:

        # Read the json data from the file
        data = json.load(f)

        # Build the elo ladder for the file
        ladder = build_json(data)

        # Open the output file for writing the elo json contents
        with open(filename.replace(".json",".elo"), 'w') as out:

          # Write the elo json to the output file
          json.dump(ladder, out, indent = 2)

        # Open the output file for writing the elo ladder contents
        with open(filename.replace(".json",".elo"), 'w') as out:

          # Generate a text formatted ladder from the ladder
          txt = build_txt(ladder)

          # Write the text to the output file
          out.write(txt)

  else: # No arguments

    # Prompt the user to provide a filename
    print("elo_builder.py [filename] e.g. elo_builder.py tournaments.txt")
    print("Input file (tournaments.json) format:")
    print("One file per line, e.g. 'tournaments.json'")