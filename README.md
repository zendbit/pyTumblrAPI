# pyTumblrAPI (Version 1.0.0)
python wrapper for simplify tumblr rest API (I code using Python v3.4, if it's not working on older python release you can modify this code and commit to this repository :-))

Using newer tumblr api v2 and oauth v1.0

This software is GPLV3
You can modify and redistribute free of charge :-)
This is python code to simplify access using tumblr REST API https://www.tumblr.com/docs/en/api/v2
Implementation using oauth and browser callback for authentication grant access

*Note : you should pass base_hostname in all paramter, it's not mandatory but most of tumblr api need base_hostname parameter. In this case I use xyzmind.tumblr.com as my base_hostname

How to use this tumblrAPI?

#A. authentication process
<pre>
# example using python tumblr API
#
# for testing only, in your case you need to handle callback url and grab oauth_token and oauth_verifier
# for get access token
#
# for authentication grant access
# will return authentication url for grant access

from tumblrAPI import TumblrAPI

# create object
# TumblrAPI('CONSUMER SECRET', 'CONSUMER KEY')

t_api = TumblrAPI('rUJ8MepSitKOYoSmaIJS', '49BcA9HPSaD')

# request token
# need callback parameter
# callback is must same with your application callback in twitter apps

request_token = t_api.request_token('http://127.0.0.1:8888/p/authenticate/tumblr')

# return token will give dictionary output if operation success
# example output in my case {'oauth_callback_confirmed': 'true', 'oauth_token': 'ITL82qNEmWkh3Uze', 'oauth_token_secret': 'M1XwCvmMffnTD'}
# we will use oauth_token and oauth_token_secret for next step when we request access token

# then use oauth_token for get authentication url
# request authentication url
# use oauth_token as parameter

print(t_api.request_authenticate_url(request_token.get('oauth_token')))

# in my case will give output
# http://www.tumblr.com/oauth/authorize?oauth_token=ITL82qNEmWkh3Uze
# this token only available for 300 second after that you need to regenerate new one

# will give you output grant access url
# open on the browser, in my case output will be like this
# http://www.tumblr.com/oauth/authorize?oauth_token=ITL82qNEmWkh3Uze
# open on the browser and grant access to application
</pre>

#B. grant access to the application and get access token
After open link in browser in my case i use http://www.tumblr.com/oauth/authorize?oauth_token=ITL82qNEmWkh3Uze
After granting access it will be redirect to your callback url in my case i use http://127.0.0.1:8888/p/authenticate/tumblr
If valid it will automatically redirect to your callback url with oauth_token, oauth_token_secret (from previous step) and oauth_verifier, in my case it will be redirect to http://127.0.0.1:8888/p/authenticate/tumblr?oauth_token=b0BbomV1nZzFqr8Oc&oauth_verifier=QTLTHWAF52trN07q1#_=_

*NOTE: skip and remove #_=_ appended character from the callback result, it should be handle by your callback url code, so we just care with this one http://127.0.0.1:8888/p/authenticate/tumblr?oauth_token=b0BbomV1nZzFqr8Oc&oauth_verifier=QTLTHWAF52trN07q1

then use oauth_token, oauth_token_secret (from previous step) and oauth_verifier to get access token
<pre>
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
</pre>

#C. request api with token and token secret
in my case I use my token and token secret
if i want call request to http://api.tumblr.com/v2/blog/:base_hostname/post twitter REST API
just use this code:
<pre>
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

# output will be in json format except when request avatar url it will give url string location of avatar image
</pre>

#D. API Type and Parameter
All url request already encapsulated in my code you only need call the name of url type, for parameter when request you need refer to tumblr REST API https://www.tumblr.com/docs/en/api/v2

here the list of mapping REST api url:
<pre>
{'api_oauth_request_token':('http://www.tumblr.com/oauth/request_token', 'POST'),
'api_oauth_authorize':('http://www.tumblr.com/oauth/authorize', 'GET'),
'api_oauth_access_token':('http://www.tumblr.com/oauth/access_token', 'POST'),
'api_blog_info':('http://api.tumblr.com/v2/blog/:base_hostname/info', 'GET'),
'api_blog_avatar':('http://api.tumblr.com/v2/blog/:base_hostname/avatar', 'GET'),
'api_blog_likes':('http://api.tumblr.com/v2/blog/:base_hostname/likes', 'GET'),
'api_blog_followers':('http://api.tumblr.com/v2/blog/:base_hostname/followers', 'GET'),
'api_blog_posts_text':('http://api.tumblr.com/v2/blog/:base_hostname/posts/text', 'GET'),
'api_blog_posts_photo':('http://api.tumblr.com/v2/blog/:base_hostname/posts/photo', 'GET'),
'api_blog_posts':('http://api.tumblr.com/v2/blog/:base_hostname/posts', 'GET'),
'api_blog_posts_quote':('http://api.tumblr.com/v2/blog/:base_hostname/posts/quote', 'GET'),
'api_blog_posts_link':('http://api.tumblr.com/v2/blog/:base_hostname/posts/link', 'GET'),
'api_blog_posts_chat':('http://api.tumblr.com/v2/blog/:base_hostname/posts/chat', 'GET'),
'api_blog_posts_audio':('http://api.tumblr.com/v2/blog/:base_hostname/posts/audio', 'GET'),
'api_blog_posts_video':('http://api.tumblr.com/v2/blog/:base_hostname/posts/video', 'GET'),
'api_blog_posts_queue':('http://api.tumblr.com/v2/blog/:base_hostname/posts/queue', 'GET'),
'api_blog_posts_draft':('http://api.tumblr.com/v2/blog/:base_hostname/posts/draft', 'GET'),
'api_blog_posts_submission':('http://api.tumblr.com/v2/blog/:base_hostname/posts/submission', 'GET'),
'api_blog_post':('http://api.tumblr.com/v2/blog/:base_hostname/post', 'POST'),
'api_blog_post_edit':('http://api.tumblr.com/v2/blog/:base_hostname/post/edit', 'POST'),
'api_blog_post_reblog':('http://api.tumblr.com/v2/blog/:base_hostname/post/reblog', 'POST'),
'api_blog_post_delete':('http://api.tumblr.com/v2/blog/:base_hostname/post/delete', 'POST'),
'api_user_info':('http://api.tumblr.com/v2/user/info', 'GET'),
'api_user_likes':('http://api.tumblr.com/v2/user/likes', 'GET'),
'api_user_following':('http://api.tumblr.com/v2/user/following', 'GET'),
'api_user_follow':('http://api.tumblr.com/v2/user/follow', 'POST'),
'api_user_unfollow':('http://api.tumblr.com/v2/user/unfollow', 'POST'),
'api_user_like':('http://api.tumblr.com/v2/user/like', 'POST'),
'api_user_unlike':('http://api.tumblr.com/v2/user/unlike', 'POST'),
'api_tagged':('http://api.tumblr.com/v2/tagged', 'GET')}
</pre>

<pre>
api_type='api_blog_avatar' or api_type='api_blog_info' etc.

ex:
params = {'base_hostname':'xyzmind.tumblr.com', 'size':'64'}
print(t_api.request_api('299-2cim9m4d630UKb', 'VN8gw5ESX8eBExLzS8pp', 'api_blog_avatar', params))

params should be refer to tumblr REST API,
</pre>
