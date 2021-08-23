# Async IO Library
import asyncio

# Challonge API Library
import challonge

# config File
import config

# JSON Library
import json

# System Library
import sys

# Process the match data 
# for a tournament
async def get_matches(tour):

  # List that will be returned
  history = []

  # Get a list of all of the participants
  participants = await tour.get_participants()

  # Participants hashtable
  table = {}

  # Create a hashtable of the participants
  for p in participants:

    # Assign the id to the table entry 
    table[p.id] = p

  # Get all of the tournament matches
  matches = await tour.get_matches()

  # Loop over all of the matches
  for match in matches:

    # Add the match round, winner, loser to the list
    history.append((match.round, table[match.winner_id].name, table[match.loser_id].name))

  # Return the list to the calling process
  return history


# Build an elo ladder for a 
# single (or list of) tournaments
async def build_json(loop, lines, file):

  # List of all recorded matches
  matches = []

  # Get the challonge user using the challonge api
  user = await challonge.get_user(config.name, config.key)

  # Loop over the tournaments provided
  for line in lines:

    # Split the row in the csv on the comma

    # [0]: yj78qn73

    rows = line.split(',')

    # Get the info about the tournament
    tour = await user.get_tournament(url = rows[0])

    # Get all of the match outcomes from the tournament (ordered)
    result = await get_matches(tour)

    # Add the new matches to the list
    matches = (result + matches)

  # Open the given filename
  with open(file, 'w') as f:

    # Dump the json content to the file
    json.dump(matches, f, indent = 2)

if __name__ == '__main__':

  # Create the async event loop
  loop = asyncio.get_event_loop()

  # List of files to calculate elo for
  files = []

  # If there are any arguments
  if len(sys.argv) > 1:

    # Get all entries after the first
    files = sys.argv[1:]

    # Loop over the files
    for filename in files:

      # Get the content from the file
      lines = open(filename).readlines()

      # Split the filename on the '.', and add .out to the name
      f = filename.replace(".csv",".json")

      # Run the async event loop for the file
      loop.run_until_complete(build_json(loop, lines, f))

  else: # No arguments

    # Prompt the user to provide a filename
    print("json_builder.py [filename] e.g. json_builder.py tournaments.txt")
    print("Input file (tournaments.txt) format:")
    print("One link per line, e.g. 'https://challonge.com/ddpultspt1'")