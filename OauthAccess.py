import twitter
from oauthtwitter import OAuthApi
 
class OauthAccess():
 
    CONSUMER_KEY = "atG3B3lZ6fOKshfiUr5FAMDER"
    CONSUMER_SECRET = "zJ52dNaHe3CHDHZahmBC7JwciUS93rFhf5pPzk79CqKZN37R1z"
    ACCESS_TOKEN_URL = 'https://twitter.com/oauth/access_token'
 
    mPin = ""
    mOauthRequestToken = ""
    mOauthAccessToken = ""
    mUser = twitter.User
    mTwitterApi = ""
 
    def __init__(self, pOauthRequestToken, pPin):
        self.mOauthRequestToken = pOauthRequestToken
        self.mPin = pPin
 
    def getOauthAccess(self):
        self.mTwitterApi = OAuthApi(self.CONSUMER_KEY, self.CONSUMER_SECRET, self.mOauthRequestToken)
        self.mOauthAccessToken = self.mTwitterApi.getAccessToken(self.mPin)
        self.mAuthenticatedTwitterInstance = OAuthApi(self.CONSUMER_KEY, self.CONSUMER_SECRET, self.mOauthAccessToken)
        self.mUser = self.mAuthenticatedTwitterInstance.GetUserInfo()