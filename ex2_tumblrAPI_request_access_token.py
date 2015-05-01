# import tumblr api

from tumblrAPI import TumblrAPI

# create object
# input your oauth_token, oauth_token_secret (from previous step) and oauth_verifier from callback url to request access token

t_api = TumblrAPI('rUJ8MepSitKOYoSmaIJS', '49BcA9HPSaD')

# request_access_token('oauth_token', 'oauth_token_secret', 'oauth_verifier')

print(t_api.request_access_token('ITL82qNEmWkh3Uze', 'M1XwCvmMffnTD', 'QTLTHWAF52trN07q1'))

# in my case it will give an output
# {'oauth_token_secret': 'VN8gw5ESX8eBExLzS8pp', oauth_token': '299-2cim9m4d630UKb'}
# save it and store it in text file or database, because we can use oauth_token_secret and oauth_token for request an api
# no need step step 1 and step 2 if you already have oauth_token and oauth_token_secret