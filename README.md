# Assessment for Neuroflow

- first commit includes (got ahead of myself!!)

Create a web REST application with a '/mood' endpoint, which when POSTed to persists the
submitted mood value.
Add the ability for users to login.
Update the '/mood' endpoint with a GET method, so it only returns values submitted by the
logged-in user.

- second commit is .gitignore

- third commit: Add to the body of the response for the ‘/mood’ endpoint the length of their current "streak".

- fourth commit: fix the [Update the '/mood' endpoint with a GET method...] step, results were not serialized into json

- fifth commit: Calculate the user's streak's percentile and return >= 50

- sixth commit: Dockerize + notes

## Directions:
	1. Run run.py in order to create appropriate db/tables
	2. Use Insomnia, cURL, or another client to test API endpoints @ http://0.0.0.0:1337 (user/password auth on resource endpoints):
		/mood [GET] - returns mood entries from authenticated user, percentile if max streak >= 50%
		/mood [POST] -  Creates new mood entry. If streak is valid, it is aggregated, else defaults to 1
		/api/users [POST] - Creates new user. Requires username/password as application/json 

### Notes:

	If this were a production application, I would certainly add tests (via pytest) in order to prevent unintended consequences in a CI/CD environment. I would also move the app.config to environment variables for safe keeping. Another security enhancement would be to further validate/sanitize the json inputs from the api to ensure there are no attempts at SQL injection. For cleanliness, the DB models could probably be moved to separate files.

	In order to scale the application, I would definitely replace SQLite with Postgres or another SQL flavor of your choice. The port would be relatively trivial with SQLAlchemy in place. For usability/security, I would definitely alter the API endpoints to serve JWT to authenticated users. Unfortunately, I do not have experience with Flask at scale, however, I am sure there are some performance tweaks that could be configured.
