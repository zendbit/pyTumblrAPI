# call REST API
# call request api
# read tumblr rest api for more params optional
# ex: params = {'param':'value', 'param':'value'}
# api_type is key of api will called
# ex: api_type='api_blog_post'
# def request_api(self, oauth_token, oauth_token_secret, api_type, params={}):

from tumblrAPI import TumblrAPI
t_api = TumblrAPI('rUJ8MepSitKOYoSmaIJS', '49BcA9HPSaD')

# use api_type='api_blog_post' for request http://api.tumblr.com/v2/blog/:base_hostname/post
# request_api(oauth_token, oauth_token_secret, api_type, params={})
# params in dictionary
# all parameter should be in string format
# in my case I will use this information from previous step {'oauth_token_secret': 'VN8gw5ESX8eBExLzS8pp', 'oauth_token': '299-2cim9m4d630UKb'\}

params={'base_hostname':'xyzmind.tumblr.com', 'type':'text', 'title':'test from client', 'body':'yeah cool'}
print(t_api.request_api('299-2cim9m4d630UKb', 'VN8gw5ESX8eBExLzS8pp', 'api_blog_post', params))

# output will be in json format