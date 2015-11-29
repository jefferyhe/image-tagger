#!/usr/bin/env python

#	Copyright 2013 AlchemyAPI
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from __future__ import print_function

import requests

try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
    from urllib.parse import urlencode
except ImportError:
    from urlparse import urlparse
    from urllib2 import urlopen
    from urllib import urlencode

try:
    import json
except ImportError:
    # Older versions of Python (i.e. 2.4) require simplejson instead of json
    import simplejson as json


if __name__ == '__main__':
    """
    Writes the API key to api_key.txt file. It will create the file if it doesn't exist.
    This function is intended to be called from the Python command line using: python alchemyapi YOUR_API_KEY
    If you don't have an API key yet, register for one at: http://www.alchemyapi.com/api/register.html

    INPUT:
    argv[1] -> Your API key from AlchemyAPI. Should be 40 hex characters

    OUTPUT:
    none
    """

    import sys
    if len(sys.argv) == 2 and sys.argv[1]:
        if len(sys.argv[1]) == 40:
            # write the key to the file
            f = open('api_key.txt', 'w')
            f.write(sys.argv[1])
            f.close()
            print('Key: ' + sys.argv[1] + ' was written to api_key.txt')
            print(
                'You are now ready to start using AlchemyAPI. For an example, run: python example.py')
        else:
            print(
                'The key appears to invalid. Please make sure to use the 40 character key assigned by AlchemyAPI')


class AlchemyAPI:
    # Setup the endpoints
    ENDPOINTS = {}
    ENDPOINTS['sentiment'] = {}
    ENDPOINTS['sentiment']['url'] = '/url/URLGetTextSentiment'
    ENDPOINTS['sentiment']['text'] = '/text/TextGetTextSentiment'
    ENDPOINTS['sentiment']['html'] = '/html/HTMLGetTextSentiment'
    ENDPOINTS['sentiment_targeted'] = {}
    ENDPOINTS['sentiment_targeted']['url'] = '/url/URLGetTargetedSentiment'
    ENDPOINTS['sentiment_targeted']['text'] = '/text/TextGetTargetedSentiment'
    ENDPOINTS['sentiment_targeted']['html'] = '/html/HTMLGetTargetedSentiment'
    ENDPOINTS['author'] = {}
    ENDPOINTS['author']['url'] = '/url/URLGetAuthor'
    ENDPOINTS['author']['html'] = '/html/HTMLGetAuthor'
    ENDPOINTS['keywords'] = {}
    ENDPOINTS['keywords']['url'] = '/url/URLGetRankedKeywords'
    ENDPOINTS['keywords']['text'] = '/text/TextGetRankedKeywords'
    ENDPOINTS['keywords']['html'] = '/html/HTMLGetRankedKeywords'
    ENDPOINTS['concepts'] = {}
    ENDPOINTS['concepts']['url'] = '/url/URLGetRankedConcepts'
    ENDPOINTS['concepts']['text'] = '/text/TextGetRankedConcepts'
    ENDPOINTS['concepts']['html'] = '/html/HTMLGetRankedConcepts'
    ENDPOINTS['entities'] = {}
    ENDPOINTS['entities']['url'] = '/url/URLGetRankedNamedEntities'
    ENDPOINTS['entities']['text'] = '/text/TextGetRankedNamedEntities'
    ENDPOINTS['entities']['html'] = '/html/HTMLGetRankedNamedEntities'
    ENDPOINTS['category'] = {}
    ENDPOINTS['category']['url'] = '/url/URLGetCategory'
    ENDPOINTS['category']['text'] = '/text/TextGetCategory'
    ENDPOINTS['category']['html'] = '/html/HTMLGetCategory'
    ENDPOINTS['relations'] = {}
    ENDPOINTS['relations']['url'] = '/url/URLGetRelations'
    ENDPOINTS['relations']['text'] = '/text/TextGetRelations'
    ENDPOINTS['relations']['html'] = '/html/HTMLGetRelations'
    ENDPOINTS['language'] = {}
    ENDPOINTS['language']['url'] = '/url/URLGetLanguage'
    ENDPOINTS['language']['text'] = '/text/TextGetLanguage'
    ENDPOINTS['language']['html'] = '/html/HTMLGetLanguage'
    ENDPOINTS['text'] = {}
    ENDPOINTS['text']['url'] = '/url/URLGetText'
    ENDPOINTS['text']['html'] = '/html/HTMLGetText'
    ENDPOINTS['text_raw'] = {}
    ENDPOINTS['text_raw']['url'] = '/url/URLGetRawText'
    ENDPOINTS['text_raw']['html'] = '/html/HTMLGetRawText'
    ENDPOINTS['title'] = {}
    ENDPOINTS['title']['url'] = '/url/URLGetTitle'
    ENDPOINTS['title']['html'] = '/html/HTMLGetTitle'
    ENDPOINTS['feeds'] = {}
    ENDPOINTS['feeds']['url'] = '/url/URLGetFeedLinks'
    ENDPOINTS['feeds']['html'] = '/html/HTMLGetFeedLinks'
    ENDPOINTS['microformats'] = {}
    ENDPOINTS['microformats']['url'] = '/url/URLGetMicroformatData'
    ENDPOINTS['microformats']['html'] = '/html/HTMLGetMicroformatData'
    ENDPOINTS['combined'] = {}
    ENDPOINTS['combined']['url'] = '/url/URLGetCombinedData'
    ENDPOINTS['combined']['text'] = '/text/TextGetCombinedData'
    ENDPOINTS['image'] = {}
    ENDPOINTS['image']['url'] = '/url/URLGetImage'
    ENDPOINTS['imagetagging'] = {}
    ENDPOINTS['imagetagging']['url'] = '/url/URLGetRankedImageKeywords'
    ENDPOINTS['imagetagging']['image'] = '/image/ImageGetRankedImageKeywords'
    ENDPOINTS['facetagging'] = {}
    ENDPOINTS['facetagging']['url'] = '/url/URLGetRankedImageFaceTags'
    ENDPOINTS['facetagging']['image'] = '/image/ImageGetRankedImageFaceTags'    
    ENDPOINTS['taxonomy'] = {}
    ENDPOINTS['taxonomy']['url'] = '/url/URLGetRankedTaxonomy'
    ENDPOINTS['taxonomy']['html'] = '/html/HTMLGetRankedTaxonomy'
    ENDPOINTS['taxonomy']['text'] = '/text/TextGetRankedTaxonomy'

    # The base URL for all endpoints
    BASE_URL = 'http://access.alchemyapi.com/calls'

    s = requests.Session()

    def __init__(self):
        """	
        Initializes the SDK so it can send requests to AlchemyAPI for analysis.
        It loads the API key from api_key.txt and configures the endpoints.
        """

        import sys
        try:
            # Open the key file and read the key
            f = open("api_key.txt", "r")
            key = f.read().strip()

            if key == '':
                # The key file should't be blank
                print(
                    'The api_key.txt file appears to be blank, please run: python alchemyapi.py YOUR_KEY_HERE')
                print(
                    'If you do not have an API Key from AlchemyAPI, please register for one at: http://www.alchemyapi.com/api/register.html')
                sys.exit(0)
            elif len(key) != 40:
                # Keys should be exactly 40 characters long
                print(
                    'It appears that the key in api_key.txt is invalid. Please make sure the file only includes the API key, and it is the correct one.')
                sys.exit(0)
            else:
                # setup the key
                self.apikey = key

            # Close file
            f.close()
        except IOError:
            # The file doesn't exist, so show the message and create the file.
            print(
                'API Key not found! Please run: python alchemyapi.py YOUR_KEY_HERE')
            print(
                'If you do not have an API Key from AlchemyAPI, please register for one at: http://www.alchemyapi.com/api/register.html')

            # create a blank key file
            open('api_key.txt', 'a').close()
            sys.exit(0)
        except Exception as e:
            print(e)


    def imageTagging(self, flavor, data, options={}):
        """

        INPUT:
        flavor -> which version of the call only url or image.
        data -> the data to analyze, either the the url or path to image.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.
        """
        if flavor not in AlchemyAPI.ENDPOINTS['imagetagging']:
            return {'status': 'ERROR', 'statusInfo': 'imagetagging for ' + flavor + ' not available'}
        elif 'image' == flavor:
            image = open(data, 'rb').read()
            options['imagePostMode'] = 'raw'
            return self.__analyze(AlchemyAPI.ENDPOINTS['imagetagging'][flavor], options, image)

        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['imagetagging'][flavor], {}, options)
    
    def __analyze(self, endpoint, params, post_data=bytearray()):
        """
        HTTP Request wrapper that is called by the endpoint functions. This function is not intended to be called through an external interface. 
        It makes the call, then converts the returned JSON string into a Python object. 

        INPUT:
        url -> the full URI encoded url

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Add the API Key and set the output mode to JSON
        params['apikey'] = self.apikey
        params['outputMode'] = 'json'

        # additonal params
        params['forceShowAll'] = 1
        params['knowledgeGraph'] = 1
        # Insert the base url

        post_url = ""
        try:
            post_url = AlchemyAPI.BASE_URL + endpoint + \
                '?' + urlencode(params).encode('utf-8')
        except TypeError:
            post_url = AlchemyAPI.BASE_URL + endpoint + '?' + urlencode(params)

        results = ""
        try:
            results = self.s.post(url=post_url, data=post_data)
        except Exception as e:
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'network-error'}
        try:
            return results.json()
        except Exception as e:
            if results != "":
                print(results)
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'parse-error'}