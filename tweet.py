from flask import Flask, request, redirect, url_for, session, flash, g, \
     render_template,request
from flask_oauth import OAuth
import twitter as TWEET
SECRET_KEY = 'development key'
DEBUG = True

# setup flask
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()
CONSUMER_KEY = 'atG3B3lZ6fOKshfiUr5FAMDER'
CONSUMER_SECRET = 'zJ52dNaHe3CHDHZahmBC7JwciUS93rFhf5pPzk79CqKZN37R1z'

# Use Twitter as example remote application
twitter = oauth.remote_app('twitter',
    # unless absolute urls are used to make requests, this will be added
    # before all URLs.  This is also true for request_token_url and others.
    base_url='https://api.twitter.com/1/',
    # where flask should look for new request tokens
    request_token_url='https://api.twitter.com/oauth/request_token',
    # where flask should exchange the token with the remote application
    access_token_url='https://api.twitter.com/oauth/access_token',
    # twitter knows two authorizatiom URLs.  /authorize and /authenticate.
    # they mostly work the same, but for sign on /authenticate is
    # expected because this will give the user a slightly different
    # user interface on the twitter side.
    authorize_url='https://api.twitter.com/oauth/authenticate',
    # the consumer keys from the twitter application registry.
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET
)



@app.before_request
def before_request():
    g.user_id = None
    print session
    if 'user_id' in session:
        g.user_id = session['user_id']
        print g.user_id,"$$$$$$$$$$$$$$$$$$$$$$"
        print session,"&&&&&&&&&&&&&&&&&&&&&&&&&&&&"


@app.after_request
def after_request(response):
    return response


@twitter.tokengetter
def get_twitter_token():
    """This is used by the API to look for the auth token and secret
    it should use for API calls.  During the authorization handshake
    a temporary set of token and secret is used, but afterwards this
    function has to return the token and secret.  If you don't want
    to store this in the database, consider putting it into the
    session instead.
    """
    user = g.user_id
    if user is not None:
        return session['oauth_token'], session['oauth_secret']


@app.route('/')
def index():
    tweets = None
    if g.user_id is not None:

        ACCESS_TOKEN =  session['oauth_token']
        ACCESS_TOKEN_SECRET = session['oauth_secret']
        api = TWEET.Api(consumer_key=CONSUMER_KEY,consumer_secret=CONSUMER_SECRET,
         access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)
        tweets =    api.GetSearch(term='football',count=100)
        print tweets,'\n\n'
        if len(tweets)>0:
            tweets = tweets
        else:
            flash('Unable to load tweets from Twitter. Maybe out of '
                      'API calls or Twitter is overloaded.')
    return render_template('index.html', tweets=tweets)


@app.route('/tweet', methods=['POST'])
def tweet():
    """Calls the remote twitter API to create a new status update."""
    if g.user_id is None:
        return redirect(url_for('login', next=request.url))
    status = request.form['tweet']
    if not status:
        return redirect(url_for('index'))
    ACCESS_TOKEN =  session['oauth_token']
    ACCESS_TOKEN_SECRET = session['oauth_secret']
    api = TWEET.Api(consumer_key=CONSUMER_KEY,consumer_secret=CONSUMER_SECRET,
     access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

    
    try:
        resp = api.PostUpdate(status)
        print resp
        if len(resp.text)>0:
            flash('Successfully tweeted your tweet (: #%s)' % resp.text)
    except:
        flash('some error occured')
    return redirect(url_for('index'))


@app.route('/login')
def login():
    """Calling into authorize will cause the OpenID auth machinery to kick
    in.  When all worked out as expected, the remote application will
    redirect back to the callback URL provided.
    """
    return twitter.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next') or request.referrer or None))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('index'))


@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    """Called after authorization.  After this function finished handling,
    the OAuth information is removed from the session again.  When this
    happened, the tokengetter from above is used to retrieve the oauth
    token and secret.

    Because the remote application could have re-authorized the application
    it is necessary to update the values in the database.

    If the application redirected back after denying, the response passed
    to the function will be `None`.  Otherwise a dictionary with the values
    the application submitted.  Note that Twitter itself does not really
    redirect back unless the user clicks on the application name.
    """
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)


    # in any case we update the authenciation token in the db
    # In case the user temporarily revoked access we will have
    # new tokens here.
    print resp,'^^^^^^^^^^^^^^^^^^^'

    oauth_token = resp['oauth_token']
    oauth_secret = resp['oauth_token_secret']
    user = resp['screen_name']
    session['user_id'] = resp['screen_name']
    session['oauth_token'] = oauth_token
    session['oauth_secret'] = oauth_secret
    print session,"::::::::::::::::::;;"
    flash('You were signed in')
    return redirect(next_url)


if __name__ == '__main__':
    app.run()
