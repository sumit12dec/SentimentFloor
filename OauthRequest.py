from oauthtwitter import OAuthApi
 
class OauthRequest():
    CONSUMER_KEY = "atG3B3lZ6fOKshfiUr5FAMDER"
    CONSUMER_SECRET = "zJ52dNaHe3CHDHZahmBC7JwciUS93rFhf5pPzk79CqKZN37R1z"
    AUTHORIZATION_URL = 'http://twitter.com/oauth/authorize'
    REQUEST_TOKEN_URL = 'https://twitter.com/oauth/request_token'
 
    def GetRequest(self):
        vOauthApi = OAuthApi(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        self.mOauthRequestToken = vOauthApi.getRequestToken(self.REQUEST_TOKEN_URL)
        self.mOauthRequestUrl = vOauthApi.getAuthorizationURL(self.mOauthRequestToken)