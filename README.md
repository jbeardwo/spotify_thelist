# thelist-spotify

This is a simple program that uses the Spotify API to get a users followed artists
and reference [The List](http://www.foopee.com/punk/the-list/)
to see if there are any shows in the Bay Area for those artists.

## Requirements

- Python 3.12+
- A Spotify account
- A Spotify Developer App (to get your `CLIENT_ID` and `CLIENT_SECRET`)

## Instructions

- git clone <https://github.com/jbeardwo/spotify_thelist>
- cd spotify_thelist
- make your own .env file using .env.example as a template
- uv sync
- uv run main.py
- You will have to login to your Spotify account and authorize the application.
- You will authenticate automatically for a while after that.

### Final Thoughts

- I may expand on this later but it does what I want for now.
- I will likely host this eventually.
