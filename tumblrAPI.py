# TumblrAPI
#
# this document is GPLV3
# you can changes or modify and redistribute for free
# author : amru rosyada
# email : amru.rosyada@gmail.com
# twitter : @_mru_
# skype : amru.rosyada
# tumblr api V2
# oauth v1.0
import time
from base64 import b64encode
from urllib.parse import quote, parse_qs
from urllib.request import Request, urlopen
from hmac import new as hmac
from hashlib import sha1

class TumblrAPI():
    
    # constructor init parameter is consumer secret and consumer key
    def __init__(self, consumer_secret, consumer_key):
        self.consumer_secret = consumer_secret
        self.consumer_key = consumer_key
        
        # list of dictionary of twitter rest api url
        # access via dicionary get will return url of rest api
        self.rest_api = {'api_oauth_request_token':('http://www.tumblr.com/oauth/request_token', 'POST'),
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

    # parameter
    # url_request : api url for request ex https://api.twitter.com/oauth/request_token
    # oauth_token : access token for accessing api this step should be after request granting from user to application
    # oauth_token_secret : access token will concate with consumer secret for generating signing key
    # oauth_callback : required if request oauth token and oauth token sercret, this callback should be same with application callback on api provider
    # request_method can be POST/GET
    # use_headers_auth False/True, depend on provider restriction
    # if use_headers_auth True headers will send with Authorization payload
    # additional_params should be pair key and val as dictionary and will put on payload request
    def do_request(self, url_request='', request_method='GET',
        oauth_token='', oauth_token_secret='',
        oauth_callback='', use_headers_auth=False, additional_params={}):

        oauth_nonce = str(time.time()).replace('.', '')
        oauth_timestamp = str(int(time.time()))

        params = {'oauth_consumer_key':self.consumer_key,
            'oauth_nonce':oauth_nonce,
            'oauth_signature_method':'HMAC-SHA1',
            'oauth_timestamp':oauth_timestamp,
            'oauth_version':'1.0'}

        # if validate callback
        # and request token and token secret
        if(oauth_callback != ''):
            params['oauth_callback'] = oauth_callback

        # if request with token
        if(oauth_token != ''):
            params['oauth_token'] = oauth_token
            
        # if additional parameter exist
        # append to parameter
        for k in additional_params:
            params[k] = additional_params.get(k)

        # tumblr need api_key in parameter
        # we need consumer key as api_key
        params['api_key'] = self.consumer_key

        # create signing key
        # generate oauth_signature
        # key structure oauth standard is [POST/GET]&url_request&parameter_in_alphabetical_order
        params_str = '&'.join(['%s=%s' % (self.percent_quote(k), self.percent_quote(params[k])) for k in sorted(params)])
        message = '&'.join([request_method, self.percent_quote(url_request), self.percent_quote(params_str)])

        # Create a HMAC-SHA1 signature of the message.
        # Concat consumer secret with oauth token secret if token secret available
        # if token secret not available it's mean request token and token secret
        key = '%s&%s' % (self.percent_quote(self.consumer_secret), self.percent_quote(oauth_token_secret)) # Note compulsory "&".
        signature = hmac(key.encode('UTF-8'), message.encode('UTF-8'), sha1)
        digest_base64 = b64encode(signature.digest()).decode('UTF-8')
        params["oauth_signature"] = digest_base64

        # if use_headers_auth
        headers_payload = {}
        if use_headers_auth:
            headers_str_payload = 'OAuth ' + ', '.join(['%s="%s"' % (self.percent_quote(k), self.percent_quote(params[k])) for k in sorted(params)])
            headers_payload['Authorization'] = headers_str_payload

            # if POST method add urlencoded
            if request_method == 'POST':
                headers_payload['Content-Type'] = 'application/x-www-form-urlencoded'
                
            headers_payload['User-Agent'] = 'HTTP Client'
            
        # generate param to be passed into url
        params_str = '&'.join(['%s=%s' % (k, self.percent_quote(params[k])) for k in sorted(params)])

        # if method GET append parameter to url_request with ? params_request_str
        # and set params_request_str to None
        # if using get method
        # all parameter should be exposed into get parameter in alphabetical order
        if request_method == 'GET':
            url_request += '?' + params_str
            params_str = None
            
        # if method POST encode data to standard iso
        # post using header based method
        elif request_method == 'POST':
            # encode to standard iso for post method
            params_str = params_str.encode('ISO-8859-1')

        #print(url_request)
        # request to provider with
        # return result
        try:
            req = Request(url_request, data=params_str, headers=headers_payload, method=request_method)
            res = urlopen(req)

            # if avatar request url contain avatar
            # return value should be avatar url location
            # don'3 read image result
            # just return the url
            if url_request.find('/avatar') != -1:
                return res.url.encode('UTF-8')

            # default return value
            return res.readall()

        except Exception as e:
            print(e)
            return None

    # parse query string into dictionary
    # parameter is query string key=valuy&key2=value2
    def qs_to_dict(self, qs_string):
        res = parse_qs(qs_string)
        data_out = {}
        for k in res:
            data_out[k] = res[k][0]
        
        return data_out
        
    # simplify request token
    # get request token
    # required oauth_callback
    def request_token(self, oauth_callback):
        url, method = self.rest_api.get('api_oauth_request_token')
        
        res = self.do_request(url_request=url,
            request_method=method,
            oauth_callback=oauth_callback,
            use_headers_auth=True)

        # mapping to dictionary
        # return result as dictioanary
        if res:
            return self.qs_to_dict(res.decode('UTF-8'))
            

        # default return is None
        return None

    # request authentication url
    # requred parameter is oauth_token
    # will return request_auth_url for granting permission
    def request_authenticate_url(self, oauth_token):
        url, method = self.rest_api.get('api_oauth_authorize')
        
        if oauth_token:
            return '?'.join((url, '='.join(('oauth_token', self.percent_quote(oauth_token)))))
            
        # default value is None
        return None
        
    # request access token
    # parameter oauth_verifier and oauth_token is required 
    def request_access_token(self, oauth_token, oauth_token_secret, oauth_verifier):
        url, method = self.rest_api.get('api_oauth_access_token')
        
        if oauth_token and oauth_verifier:
            res = self.do_request(url_request=url,
                request_method=method,
                oauth_token=oauth_token,
                oauth_token_secret=oauth_token_secret,
                oauth_callback='',
                use_headers_auth=True,
                additional_params={'oauth_verifier':oauth_verifier})
                
            # mapping to dictionary
            # return result as dictioanary
            if res:
                return self.qs_to_dict(res.decode('UTF-8'))
                
        # default return none
        return None
        
    # call request api
    # ex: params = {'base_hostname':'yourdomain.tumblr.com|yourcustomdomain.com', 'other_optional_param':'value'}
    # api_type is key of api will called
    # ex: api_type='api_blog_info'
    def request_api(self, oauth_token, oauth_token_secret, api_type, params={}):
        url, method = self.rest_api.get(api_type)

        # replace :base_hostname in url with param base_hostname
        # pop base_hostname to remove it from parameter
        # dont pass base_hostname into querystring
        if url.find(':base_hostname') != -1:
            url = url.replace(':base_hostname', params.pop('base_hostname'))

        # if request avatar and give params size
        # then append size to end of url
        # ex size available is 16, 24, 30, 40, 48, 64, 96, 128, 512
        if url.find('/avatar') != -1 and params.get('size'):
            url = '/'.join((url, params.get('size')))

        res = self.do_request(url_request=url,
                request_method=method,
                oauth_token=oauth_token,
                oauth_token_secret=oauth_token_secret,
                oauth_callback='',
                use_headers_auth=True,
                additional_params=params)

        if res:
            return res.decode('UTF-8')

        # default return value
        return None

    # percent_quote
    # quote url as percent quote
    def percent_quote(self, text):
        return quote(text, '~')
        