## See readme

from flask import Flask
from threading import Thread
import time, json, pickle, os
from datetime import datetime
import praw

app = Flask(__name__)

## RedditParser
tracked = []

class RedditParser:
    reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'],
                         client_secret=os.environ['REDDIT_CLIENT_SECRET'],
                         password=os.environ['REDDIT_PASSWORD'],
                         username=os.environ['REDDIT_USERNAME'],
                         user_agent = 'python')
    keys = ['id', 'score', 'upvote_ratio', 'num_comments', 'title', 'is_self', 'selftext','created_utc']

    @classmethod
    def get_data(self, subreddit, mode='top', limit=1000):
        data = [] #pd.DataFrame([],columns=keys)
        if mode == 'top':
            fun = self.reddit.subreddit(subreddit).top
        else:
            fun = self.reddit.subreddit(subreddit).new
        for identifier in fun(limit=100000):
            print(identifier)
            data.append(self.get_submission(identifier))
        pickle.dump(data,open(f'{subreddit}{mode}1000.p','wb'))
        return data

    @classmethod
    def get_submission(self, identifier):
        s=self.reddit.submission(id=identifier)
        dex = {k:getattr(s,k) for k in self.keys}
        dex['retrieval_timestamp'] = str(datetime.now())
        dex['N_comments'] = len(s.comments.list())
        return dex

## views ############
@app.route('/track_submission=<identifier>')
def track_submission(identifier):
    if identifier in tracked:
        return {'status': 'already running'}
    else:
        tracked.append(identifier)
        Thread(target=tracker, args=[identifier]).start()
        app.logger.info(f'tracking submission {identifier}')
        return {'status': 'success', 'time': str(datetime.now()), 'submission': identifier}

@app.route('/output_submission=<identifier>')
def output_submission(identifier):
    filename = f'{identifier}.json'
    if os.path.exists(filename):
        return {'status': 'success', 'data': json.load(open(filename,'r'))}
    else:
        return {'status': 'file not found'}

@app.route('/status')
def status():
    if tracked:
        return {'status': 'running', 'tracking': tracked}
    else:
        return {'status': 'idle'}

## tasks #############

def tracker(identifier):
    data = []
    start = datetime.now()
    while True:
        data.append(RedditParser.get_submission(identifier))
        json.dump(data,open(f'{identifier}.json','w'))
        time.sleep(60*5)
        if (datetime.now() - start).days > 1:
            tracked.remove(identifier)
            return 0

########## RUN MAIN ##############
if __name__ == '__main__':
    print('/status')
    print('/track_submission=<identifier> starts tracking')
    print('/output_submission=<identifier> outputs data')
    app.run(host= '0.0.0.0')
