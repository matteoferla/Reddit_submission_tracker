# Reddit_submission_tracker
A small API app that tracks a reddit submission for 24 hours.

## Raison d'être
Reddit does not tell you when you got voted. I am curious to see the progression of a given post.

## Setup
Run on a machine that will be shut down. Don't expose it to the world as a flask internal server should not go to prod. Keep it within your network.

Requires Python 3.7 (has f strings).

In order to use the reddit API some variables are env required: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_PASSWORD and REDDIT_USERNAME.
These are obtained by registering for using Reddit API.

  REDDIT_CLIENT_ID='∗∗∗∗∗∗∗∗∗∗∗∗∗∗' REDDIT_CLIENT_SECRET="∗∗∗∗∗∗∗∗∗∗∗∗∗-∗_∗∗∗∗∗∗∗∗∗∗∗" REDDIT_PASSWORD='∗∗∗∗∗∗∗∗∗∗∗' REDDIT_USERNAME='∗∗∗∗∗∗∗∗∗∗∗' python3 app.py > log.txt &

## Cmds
Runs an API that can track a given Reddit submission for a day every 5 minutes, logging the votes and comments.

    curl http://127.0.0.1:5000/track_submission=cblzix

Data can be retrieved via

    curl http://127.0.0.1:5000/output_submission=cblzix

Status can be queries

    curl http://127.0.0.1:5000/status

"""
