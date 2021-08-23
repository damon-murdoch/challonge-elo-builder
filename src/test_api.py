# Async IO Library
import asyncio

# Challonge API Library
import challonge

# Config file
import config

# Application Main Function
async def main(loop):

  try:

    print("Retrieving user '" + config.name + "' ...")

    # Get the challonge user using the challonge api
    user = await challonge.get_user(config.name, config.key)

    print("User retrieved successfully! Retrieving Tournaments ...")

    # Get the tournaments from the user
    tournaments = await user.get_tournaments()

    print("Tournaments retrieved successfully. Displaying tournaments ...")

    # Loop over the tournaments
    for t in tournaments:

      # Print the tournament name, url
      print("Tournament Name:", t.name, "\nTournament Url:", t.full_challonge_url)

    print("Tournaments listed. Test complete.")

  except Exception as e:

    print("Challonge API Fail:",e)

if __name__ == '__main__':

  # Create the async event loop
  loop = asyncio.get_event_loop()

  # Run the async event loop
  loop.run_until_complete(main(loop))