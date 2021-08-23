# Async Library
import asyncio

# Json Library
import json

# System Library
import sys

# System Library
import os

# Json Builder Source
import src.json_builder

# Elo Builder Source
import src.elo_builder

if __name__ == '__main__':

  # Root of the script
  root = os.path.dirname(__file__)

  # Output directory of the script
  out = os.path.join(root, 'out')

  # Create the async event loop
  loop = asyncio.get_event_loop()

  # List of files to calculate elo for
  files = []

  # If there are any arguments
  if len(sys.argv) > 1:

    # Get all entries after the first
    files = sys.argv[1:]

    # Loop over the files
    for path in files:

      # Extract the filename from the path
      filename = os.path.basename(path)

      # Get name, extension from the filename
      name, ext = os.path.splitext(filename)

      # Generate the output file name
      outname_json = name + '.json'

      # Generate outfile name in out directory
      outfile_json = os.path.join(out, outname_json)

      # Get the content from the file
      lines = open(path).readlines()

      # Run the async event loop for the file
      loop.run_until_complete(src.json_builder.build_json(loop, lines, outfile_json))

      # If the file was created successfully
      if os.path.exists(outfile_json):

        # Open the json output file
        with open(outfile_json, 'r') as file:

          # Read the json data from the file
          data = json.load(file)

          # Build the elo ladder from the file
          ladder = src.elo_builder.build_json(data)

          # Create the elo outfile name
          outname_elo = name + '.elo'

          # Create the elo outfile full path
          outfile_elo = os.path.join(out, outname_elo)

          # Open the output elo json file
          with open(outfile_elo, 'w+') as elo:

            # Write the elo json to the output file
            json.dump(ladder, elo, indent = 2)

          # Create the txt outfile name
          outname_txt = name + '.txt'

          # Create the txt outfile full path
          outfile_txt = os.path.join(out, outname_txt)

          # Open the output elo text file
          with open(outfile_txt, 'w+') as txt:

            # Write the elo ladder to the output file
            txt.write(src.elo_builder.build_txt(ladder))

      else: # File failed to be created

        print("Failed to create file '" + outfile_json + "'! Please verify the results!")

  else: # No arguments

    # Prompt the user to provide a filename
    print("json_builder.py [filename] e.g. json_builder.py tournaments.txt")
    print("Input file (tournaments.txt) format:")
    print("One link per line, e.g. 'https://challonge.com/ddpultspt1'")