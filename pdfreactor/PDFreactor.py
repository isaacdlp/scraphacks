# RealObjects PDFreactor Python Wrapper version 4
# http://www.pdfreactor.com
# 
# Released under the following license:
# 
# The MIT License (MIT)
# 
# Copyright (c) 2015-2017 RealObjects GmbH
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import sys
class PDFreactor:
    @property
    def headers(self):
        return self.__headers
    @property
    def cookies(self):
        return self.__cookies
    @property
    def apiKey(self):
        return self.__apiKey
    @apiKey.setter
    def apiKey(self, apiKey):
        self.__apiKey = apiKey
    url = ""
    def __init__(self,url="http://localhost:9423/service/rest"):
        """Constructor"""
        self.url = url
        if (url is None):
            self.url = "http://localhost:9423/service/rest"
        self.__headers = {}
        self.__cookies = {}
        self.__apiKey = None
        self.stickyMap = {}
    def convert(self,config):
        if (config != None):
            config['clientName'] = "PYTHON"
            config['clientVersion'] = PDFreactor.VERSION;

        url = self.url + "/convert.json"
        if (self.apiKey != None):
            url += '?apiKey=' + self.apiKey
        result = ""
        if len(self.__headers.keys()) == False:
            headers = self.__headers
        else :
            headers = {}
            for (key, value) in self.__headers.items():
                lcKey = key.lower()
                if lcKey != "content-type" and lcKey != "range" and lcKey != "user-agent":
                    headers[key] = value
        headers['Content-Type'] = 'application/json'
        headers['Cookie'] = '; '.join(['%s=%s' % (key, value) for (key, value) in self.__cookies.items()])
        headers['User-Agent'] = 'PDFreactor Python API v4'
        headers['X-RO-User-Agent'] = 'PDFreactor Python API v4'
        req = None
        if sys.version_info[0] == 2:
            from urllib2 import HTTPError
        else:
            from urllib.error import HTTPError
        try:
            if sys.version_info[0] == 2:
                import Cookie
                from Cookie import SimpleCookie
                import urllib2
                from urllib2 import URLError
                options = json.dumps(config)
                req = urllib2.Request(url, options, headers)
                response = urllib2.urlopen(req)
            else:
                import http.cookies
                from http.cookies import SimpleCookie
                import urllib.request
                options = json.dumps(config)
                req = urllib.request.Request(url, options.encode(), headers)
                response = urllib.request.urlopen(req)
            result = response.read()
        except HTTPError as e:
            if (e.code == 422):
                raise Exception(json.loads(e.read())['error'])
            elif (e.code == 400):
                raise Exception('Invalid client data. ' + json.loads(e.read())['error'])
            elif (e.code == 404):
                raise Exception('Error connecting to PDFreactor Web Service at ' + self.url + '. Please make sure the PDFreactor Web Service is installed and running ' + json.loads(e.read())['error'])
            elif (e.code == 403):
                raise Exception('Request rejected. ' + json.loads(e.read())['error'])
            elif (e.code == 401):
                raise Exception('Unauthorized. ' + json.loads(e.read())['error'])
            elif (e.code == 413):
                raise Exception('The configuration is too large to process.')
            elif (e.code == 500):
                raise Exception(json.loads(e.read())['error'])
            elif (e.code == 503):
                raise Exception('PDFreactor Web Service is unavailable.')
            elif (e.code > 400):
                raise Exception('PDFreactor Web Service error (status: ' + str(e.code) + ').')
        except Exception as e:
            raise Exception('Error connecting to PDFreactor Web Service at ' + self.url + '. Please make sure the PDFreactor Web Service is installed and running (Error: ' + str(e.reason) + ')')
        return json.loads(result)
    def convertAsBinary(self,config,stream = None):
        if (config != None):
            config['clientName'] = "PYTHON"
            config['clientVersion'] = PDFreactor.VERSION;

        url = self.url + "/convert.bin"
        if (self.apiKey != None):
            url += '?apiKey=' + self.apiKey
        result = ""
        if len(self.__headers.keys()) == False:
            headers = self.__headers
        else :
            headers = {}
            for (key, value) in self.__headers.items():
                lcKey = key.lower()
                if lcKey != "content-type" and lcKey != "range" and lcKey != "user-agent":
                    headers[key] = value
        headers['Content-Type'] = 'application/json'
        headers['Cookie'] = '; '.join(['%s=%s' % (key, value) for (key, value) in self.__cookies.items()])
        headers['User-Agent'] = 'PDFreactor Python API v4'
        headers['X-RO-User-Agent'] = 'PDFreactor Python API v4'
        req = None
        if sys.version_info[0] == 2:
            from urllib2 import HTTPError
        else:
            from urllib.error import HTTPError
        try:
            if sys.version_info[0] == 2:
                import Cookie
                from Cookie import SimpleCookie
                import urllib2
                from urllib2 import URLError
                options = json.dumps(config)
                req = urllib2.Request(url, options, headers)
                response = urllib2.urlopen(req)
            else:
                import http.cookies
                from http.cookies import SimpleCookie
                import urllib.request
                options = json.dumps(config)
                req = urllib.request.Request(url, options.encode(), headers)
                response = urllib.request.urlopen(req)
            if stream:
                CHUNK = 2 * 1024
                while True:
                    chunk = response.read(CHUNK)
                    if not chunk:
                        break
                    stream.write(chunk)
                result = None
            else:
                result = response.read()
        except HTTPError as e:
            if (e.code == 422):
                raise Exception(e.read())
            elif (e.code == 400):
                raise Exception('Invalid client data. ' + e.read())
            elif (e.code == 404):
                raise Exception('Error connecting to PDFreactor Web Service at ' + self.url + '. Please make sure the PDFreactor Web Service is installed and running ' + e.read())
            elif (e.code == 403):
                raise Exception('Request rejected. ' + e.read())
            elif (e.code == 401):
                raise Exception('Unauthorized. ' + e.read())
            elif (e.code == 413):
                raise Exception('The configuration is too large to process.')
            elif (e.code == 500):
                raise Exception(e.read())
            elif (e.code == 503):
                raise Exception('PDFreactor Web Service is unavailable.')
            elif (e.code > 400):
                raise Exception('PDFreactor Web Service error (status: ' + str(e.code) + ').')
        except Exception as e:
            raise Exception('Error connecting to PDFreactor Web Service at ' + self.url + '. Please make sure the PDFreactor Web Service is installed and running (Error: ' + str(e.reason) + ')')
        return result
    def convertAsync(self,config):
        if (config != None):
            config['clientName'] = "PYTHON"
            config['clientVersion'] = PDFreactor.VERSION;

        url = self.url + "/convert/async.json"
        if (self.apiKey != None):
            url += '?apiKey=' + self.apiKey
        result = ""
        if len(self.__headers.keys()) == False:
            headers = self.__headers
        else :
            headers = {}
            for (key, value) in self.__headers.items():
                lcKey = key.lower()
                if lcKey != "content-type" and lcKey != "range" and lcKey != "user-agent":
                    headers[key] = value
        headers['Content-Type'] = 'application/json'
        headers['Cookie'] = '; '.join(['%s=%s' % (key, value) for (key, value) in self.__cookies.items()])
        headers['User-Agent'] = 'PDFreactor Python API v4'
        headers['X-RO-User-Agent'] = 'PDFreactor Python API v4'
        req = None
        if sys.version_info[0] == 2:
            from urllib2 import HTTPError
        else:
            from urllib.error import HTTPError
        try:
            if sys.version_info[0] == 2:
                import Cookie
                from Cookie import SimpleCookie
                import urllib2
                from urllib2 import URLError
                options = json.dumps(config)
                req = urllib2.Request(url, options, headers)
                response = urllib2.urlopen(req)
            else:
                import http.cookies
                from http.cookies import SimpleCookie
                import urllib.request
                options = json.dumps(config)
                req = urllib.request.Request(url, options.encode(), headers)
                response = urllib.request.urlopen(req)
        except HTTPError as e:
            if (e.code == 422):
                raise Exception(json.loads(e.read())['error'])
            elif (e.code == 400):
                raise Exception('Invalid client data. ' + json.loads(e.read())['error'])
            elif (e.code == 404):
                raise Exception('Error connecting to PDFreactor Web Service at ' + self.url + '. Please make sure the PDFreactor Web Service is installed and running ' + json.loads(e.read())['error'])
            elif (e.code == 403):
                raise Exception('Request rejected. ' + json.loads(e.read())['error'])
            elif (e.code == 401):
                raise Exception('Unauthorized. ' + json.loads(e.read())['error'])
            elif (e.code == 413):
                raise Exception('The configuration is too large to process.')
            elif (e.code == 500):
                raise Exception(json.loads(e.read())['error'])
            elif (e.code == 503):
                raise Exception('Asynchronous conversions are unavailable.')
            elif (e.code > 400):
                raise Exception('PDFreactor Web Service error (status: ' + str(e.code) + ').')
        except Exception as e:
            raise Exception('Error connecting to PDFreactor Web Service at ' + self.url + '. Please make sure the PDFreactor Web Service is installed and running (Error: ' + str(e.reason) + ')')
        documentId = None;
        if (response != None and response.info() != None):
            location = response.info().getheader("Location")
            if (location != None):
                documentId = location[location.rfind("/")+1:len(location)]
            cookieHeader = response.info().getheader("Set-Cookie")
            if (cookieHeader != None):
                self.stickyMap[documentId] = {'cookies': {}, 'keepDocument': config['keepDocument'] if ('keepDocument' in config) else False}
                cookies = SimpleCookie()
                cookies.load(cookieHeader)
                for name in cookies:
                    self.stickyMap[documentId]['cookies'][name] = cookies[name].value
        return documentId
    def getProgress(self,documentId):
        url = self.url + "/progress/" + documentId + ".json"
        if (self.apiKey != None):
            url += '?apiKey=' + self.apiKey
        result = ""
        if len(self.__headers.keys()) == False:
            headers = self.__headers
        else :
            headers = {}
            for (key, value) in self.__headers.items():
                lcKey = key.lower()
                if lcKey != "content-type" and lcKey != "range" and lcKey != "user-agent":
                    headers[key] = value
        headers['Content-Type'] = 'application/json'
        headers['Cookie'] = '; '.join(['%s=%s' % (key, value) for (key, value) in self.__cookies.items()])
        headers['User-Agent'] = 'PDFreactor Python API v4'
        headers['X-RO-User-Agent'] = 'PDFreactor Python API v4'
        if (documentId in self.stickyMap):
            if (self.__cookies):
                headers['Cookie'] += '; '
            headers['Cookie'] += '; '.join(['%s=%s' % (key, value) for (key, value) in self.stickyMap[documentId]['cookies'].items()])
        req = None
        if sys.version_info[0] == 2:
            from urllib2 import HTTPError
        else:
            from urllib.error import HTTPError
        try:
            if sys.version_info[0] == 2:
                import urllib2
                from urllib2 import URLError
                req = urllib2.Request(url, None, headers)
                response = urllib2.urlopen(req)
                req.get_method = lambda: "get"
            else:
                import urllib.request
                req = urllib.request.Request(url, None, headers)
                response = urllib.request.urlopen(req)
                req.get_method = lambda: "get"
            result = response.read()
        except HTTPError as e:
            if (e.code == 422):
                raise Exception(json.loads(e.read())['error'])
            elif (e.code == 400):
                raise Exception('Invalid client data. ' + json.loads(e.read())['error'])
            elif (e.code == 404):
                raise Exception('Document with the given ID was not found. ' + json.loads(e.read())['error'])
            elif (e.code == 403):
                raise Exception('Request rejected. ' + json.loads(e.read())['error'])
            elif (e.code == 401):
                raise Exception('Unauthorized. ' + json.loads(e.read())['error'])
            elif (e.code == 413):
                raise Exception('The configuration is too large to process.')
            elif (e.code == 500):
                raise Exception(json.loads(e.read())['error'])
            elif (e.code == 503):
                raise Exception('PDFreactor Web Service is unavailable.')
            elif (e.code > 400):
                raise Exception('PDFreactor Web Service error (status: ' + str(e.code) + ').')
        except Exception as e:
            raise Exception('Error connecting to PDFreactor Web Service at ' + self.url + '. Please make sure the PDFreactor Web Service is installed and running (Error: ' + str(e.reason) + ')')
        return json.loads(result)
    def getDocument(self,documentId):
        url = self.url + "/document/" + documentId + ".json"
        if (self.apiKey != None):
            url += '?apiKey=' + self.apiKey
        result = ""
        if len(self.__headers.keys()) == False:
            headers = self.__headers
        else :
            headers = {}
            for (key, value) in self.__headers.items():
                lcKey = key.lower()
                if lcKey != "content-type" and lcKey != "range" and lcKey != "user-agent":
                    headers[key] = value
        headers['Content-Type'] = 'application/json'
        headers['Cookie'] = '; '.join(['%s=%s' % (key, value) for (key, value) in self.__cookies.items()])
        headers['User-Agent'] = 'PDFreactor Python API v4'
        headers['X-RO-User-Agent'] = 'PDFreactor Python API v4'
        if (documentId in self.stickyMap):
            if (self.__cookies):
                headers['Cookie'] += '; '
            headers['Cookie'] += '; '.join(['%s=%s' % (key, value) for (key, value) in self.stickyMap[documentId]['cookies'].items()])
        if documentId in self.stickyMap and self.stickyMap[documentId]['keepDocument'] != True:
            del self.stickyMap[documentId]
        req = None
        if sys.version_info[0] == 2:
            from urllib2 import HTTPError
        else:
            from urllib.error import HTTPError
        try:
            if sys.version_info[0] == 2:
                import urllib2
                from urllib2 import URLError
                req = urllib2.Request(url, None, headers)
                response = urllib2.urlopen(req)
                req.get_method = lambda: "get"
            else:
                import urllib.request
                req = urllib.request.Request(url, None, headers)
                response = urllib.request.urlopen(req)
                req.get_method = lambda: "get"
            result = response.read()
        except HTTPError as e:
            if (e.code == 422):
                raise Exception(json.loads(e.read())['error'])
            elif (e.code == 400):
                raise Exception('Invalid client data. ' + json.loads(e.read())['error'])
            elif (e.code == 404):
                raise Exception('Document with the given ID was not found. ' + json.loads(e.read())['error'])
            elif (e.code == 403):
                raise Exception('Request rejected. ' + json.loads(e.read())['error'])
            elif (e.code == 401):
                raise Exception('Unauthorized. ' + json.loads(e.read())['error'])
            elif (e.code == 413):
                raise Exception('The configuration is too large to process.')
            elif (e.code == 500):
                raise Exception(json.loads(e.read())['error'])
            elif (e.code == 503):
                raise Exception('PDFreactor Web Service is unavailable.')
            elif (e.code > 400):
                raise Exception('PDFreactor Web Service error (status: ' + str(e.code) + ').')
        except Exception as e:
            raise Exception('Error connecting to PDFreactor Web Service at ' + self.url + '. Please make sure the PDFreactor Web Service is installed and running (Error: ' + str(e.reason) + ')')
        return json.loads(result)
    def getDocumentAsBinary(self,documentId,stream = None):
        url = self.url + "/document/" + documentId + ".bin"
        if (self.apiKey != None):
            url += '?apiKey=' + self.apiKey
        result = ""
        if len(self.__headers.keys()) == False:
            headers = self.__headers
        else :
            headers = {}
            for (key, value) in self.__headers.items():
                lcKey = key.lower()
                if lcKey != "content-type" and lcKey != "range" and lcKey != "user-agent":
                    headers[key] = value
        headers['Content-Type'] = 'application/json'
        headers['Cookie'] = '; '.join(['%s=%s' % (key, value) for (key, value) in self.__cookies.items()])
        headers['User-Agent'] = 'PDFreactor Python API v4'
        headers['X-RO-User-Agent'] = 'PDFreactor Python API v4'
        if (documentId in self.stickyMap):
            if (self.__cookies):
                headers['Cookie'] += '; '
            headers['Cookie'] += '; '.join(['%s=%s' % (key, value) for (key, value) in self.stickyMap[documentId]['cookies'].items()])
        if documentId in self.stickyMap and self.stickyMap[documentId]['keepDocument'] != True:
            del self.stickyMap[documentId]
        req = None
        if sys.version_info[0] == 2:
            from urllib2 import HTTPError
        else:
            from urllib.error import HTTPError
        try:
            if sys.version_info[0] == 2:
                import urllib2
                from urllib2 import URLError
                req = urllib2.Request(url, None, headers)
                response = urllib2.urlopen(req)
                req.get_method = lambda: "get"
            else:
                import urllib.request
                req = urllib.request.Request(url, None, headers)
                response = urllib.request.urlopen(req)
                req.get_method = lambda: "get"
            if stream:
                CHUNK = 2 * 1024
                while True:
                    chunk = response.read(CHUNK)
                    if not chunk:
                        break
                    stream.write(chunk)
                result = None
            else:
                result = response.read()
        except HTTPError as e:
            if (e.code == 422):
                raise Exception(e.read())
            elif (e.code == 400):
                raise Exception('Invalid client data. ' + e.read())
            elif (e.code == 404):
                raise Exception('Document with the given ID was not found. ' + e.read())
            elif (e.code == 403):
                raise Exception('Request rejected. ' + e.read())
            elif (e.code == 401):
                raise Exception('Unauthorized. ' + e.read())
            elif (e.code == 413):
                raise Exception('The configuration is too large to process.')
            elif (e.code == 500):
                raise Exception(e.read())
            elif (e.code == 503):
                raise Exception('PDFreactor Web Service is unavailable.')
            elif (e.code > 400):
                raise Exception('PDFreactor Web Service error (status: ' + str(e.code) + ').')
        except Exception as e:
            raise Exception('Error connecting to PDFreactor Web Service at ' + self.url + '. Please make sure the PDFreactor Web Service is installed and running (Error: ' + str(e.reason) + ')')
        return result
    def deleteDocument(self,documentId):
        url = self.url + "/document/" + documentId + ".json"
        if (self.apiKey != None):
            url += '?apiKey=' + self.apiKey
        result = ""
        if len(self.__headers.keys()) == False:
            headers = self.__headers
        else :
            headers = {}
            for (key, value) in self.__headers.items():
                lcKey = key.lower()
                if lcKey != "content-type" and lcKey != "range" and lcKey != "user-agent":
                    headers[key] = value
        headers['Content-Type'] = 'application/json'
        headers['Cookie'] = '; '.join(['%s=%s' % (key, value) for (key, value) in self.__cookies.items()])
        headers['User-Agent'] = 'PDFreactor Python API v4'
        headers['X-RO-User-Agent'] = 'PDFreactor Python API v4'
        if (documentId in self.stickyMap):
            if (self.__cookies):
                headers['Cookie'] += '; '
            headers['Cookie'] += '; '.join(['%s=%s' % (key, value) for (key, value) in self.stickyMap[documentId]['cookies'].items()])
        if documentId in self.stickyMap:
            del self.stickyMap[documentId]
        req = None
        if sys.version_info[0] == 2:
            from urllib2 import HTTPError
        else:
            from urllib.error import HTTPError
        try:
            if sys.version_info[0] == 2:
                import urllib2
                from urllib2 import URLError
                req = urllib2.Request(url, None, headers)
                response = urllib2.urlopen(req)
                req.get_method = lambda: "delete"
            else:
                import urllib.request
                req = urllib.request.Request(url, None, headers)
                response = urllib.request.urlopen(req)
                req.get_method = lambda: "delete"
            result = response.read()
        except HTTPError as e:
            if (e.code == 422):
                raise Exception(json.loads(e.read())['error'])
            elif (e.code == 400):
                raise Exception('Invalid client data. ' + json.loads(e.read())['error'])
            elif (e.code == 404):
                raise Exception('Document with the given ID was not found. ' + json.loads(e.read())['error'])
            elif (e.code == 403):
                raise Exception('Request rejected. ' + json.loads(e.read())['error'])
            elif (e.code == 401):
                raise Exception('Unauthorized. ' + json.loads(e.read())['error'])
            elif (e.code == 413):
                raise Exception('The configuration is too large to process.')
            elif (e.code == 500):
                raise Exception(json.loads(e.read())['error'])
            elif (e.code == 503):
                raise Exception('PDFreactor Web Service is unavailable.')
            elif (e.code > 400):
                raise Exception('PDFreactor Web Service error (status: ' + str(e.code) + ').')
        except Exception as e:
            raise Exception('Error connecting to PDFreactor Web Service at ' + self.url + '. Please make sure the PDFreactor Web Service is installed and running (Error: ' + str(e.reason) + ')')
    def getVersion(self):
        url = self.url + "/version.json"
        if (self.apiKey != None):
            url += '?apiKey=' + self.apiKey
        result = ""
        if len(self.__headers.keys()) == False:
            headers = self.__headers
        else :
            headers = {}
            for (key, value) in self.__headers.items():
                lcKey = key.lower()
                if lcKey != "content-type" and lcKey != "range" and lcKey != "user-agent":
                    headers[key] = value
        headers['Content-Type'] = 'application/json'
        headers['Cookie'] = '; '.join(['%s=%s' % (key, value) for (key, value) in self.__cookies.items()])
        headers['User-Agent'] = 'PDFreactor Python API v4'
        headers['X-RO-User-Agent'] = 'PDFreactor Python API v4'
        req = None
        if sys.version_info[0] == 2:
            from urllib2 import HTTPError
        else:
            from urllib.error import HTTPError
        try:
            if sys.version_info[0] == 2:
                import urllib2
                from urllib2 import URLError
                req = urllib2.Request(url, None, headers)
                response = urllib2.urlopen(req)
                req.get_method = lambda: "get"
            else:
                import urllib.request
                req = urllib.request.Request(url, None, headers)
                response = urllib.request.urlopen(req)
                req.get_method = lambda: "get"
            result = response.read()
        except HTTPError as e:
            if (e.code == 422):
                raise Exception(json.loads(e.read())['error'])
            elif (e.code == 400):
                raise Exception('Invalid client data. ' + json.loads(e.read())['error'])
            elif (e.code == 404):
                raise Exception('Document with the given ID was not found. ' + json.loads(e.read())['error'])
            elif (e.code == 403):
                raise Exception('Request rejected. ' + json.loads(e.read())['error'])
            elif (e.code == 401):
                raise Exception('Unauthorized. ' + json.loads(e.read())['error'])
            elif (e.code == 413):
                raise Exception('The configuration is too large to process.')
            elif (e.code == 500):
                raise Exception(json.loads(e.read())['error'])
            elif (e.code == 503):
                raise Exception('PDFreactor Web Service is unavailable.')
            elif (e.code > 400):
                raise Exception('PDFreactor Web Service error (status: ' + str(e.code) + ').')
        except Exception as e:
            raise Exception('Error connecting to PDFreactor Web Service at ' + self.url + '. Please make sure the PDFreactor Web Service is installed and running (Error: ' + str(e.reason) + ')')
        return json.loads(result)
    def getStatus(self):
        url = self.url + "/status"
        if (self.apiKey != None):
            url += '?apiKey=' + self.apiKey
        result = ""
        if len(self.__headers.keys()) == False:
            headers = self.__headers
        else :
            headers = {}
            for (key, value) in self.__headers.items():
                lcKey = key.lower()
                if lcKey != "content-type" and lcKey != "range" and lcKey != "user-agent":
                    headers[key] = value
        headers['Content-Type'] = 'application/json'
        headers['Cookie'] = '; '.join(['%s=%s' % (key, value) for (key, value) in self.__cookies.items()])
        headers['User-Agent'] = 'PDFreactor Python API v4'
        headers['X-RO-User-Agent'] = 'PDFreactor Python API v4'
        req = None
        if sys.version_info[0] == 2:
            from urllib2 import HTTPError
        else:
            from urllib.error import HTTPError
        try:
            if sys.version_info[0] == 2:
                import urllib2
                from urllib2 import URLError
                req = urllib2.Request(url, None, headers)
                response = urllib2.urlopen(req)
                req.get_method = lambda: "get"
            else:
                import urllib.request
                req = urllib.request.Request(url, None, headers)
                response = urllib.request.urlopen(req)
                req.get_method = lambda: "get"
            result = response.read()
        except HTTPError as e:
            if (e.code == 422):
                raise Exception(json.loads(e.read())['error'])
            elif (e.code == 400):
                raise Exception('Invalid client data. ' + json.loads(e.read())['error'])
            elif (e.code == 404):
                raise Exception('Document with the given ID was not found. ' + json.loads(e.read())['error'])
            elif (e.code == 403):
                raise Exception('Request rejected. ' + json.loads(e.read())['error'])
            elif (e.code == 401):
                raise Exception('Unauthorized. ' + json.loads(e.read())['error'])
            elif (e.code == 413):
                raise Exception('The configuration is too large to process.')
            elif (e.code == 500):
                raise Exception(json.loads(e.read())['error'])
            elif (e.code == 503):
                raise Exception('PDFreactor Web Service is unavailable.')
            elif (e.code > 400):
                raise Exception('PDFreactor Web Service error (status: ' + str(e.code) + ').')
        except Exception as e:
            raise Exception('Error connecting to PDFreactor Web Service at ' + self.url + '. Please make sure the PDFreactor Web Service is installed and running (Error: ' + str(e.reason) + ')')
    def getDocumentUrl(self,documentId):
        return self.url + "/document/" + documentId
    def getProgressUrl(self,documentId):
        return self.url + "/progress/" + documentId
    VERSION = 4
    class CallbackType:
        FINISH = "FINISH"
        PROGRESS = "PROGRESS"
        START = "START"
    class Cleanup:
        CYBERNEKO = "CYBERNEKO"
        JTIDY = "JTIDY"
        NONE = "NONE"
        TAGSOUP = "TAGSOUP"
    class ColorSpace:
        CMYK = "CMYK"
        RGB = "RGB"
    class Conformance:
        PDF = "PDF"
        PDFA1A = "PDFA1A"
        PDFA1A_PDFUA1 = "PDFA1A_PDFUA1"
        PDFA1B = "PDFA1B"
        PDFA2A = "PDFA2A"
        PDFA2A_PDFUA1 = "PDFA2A_PDFUA1"
        PDFA2B = "PDFA2B"
        PDFA2U = "PDFA2U"
        PDFA3A = "PDFA3A"
        PDFA3A_PDFUA1 = "PDFA3A_PDFUA1"
        PDFA3B = "PDFA3B"
        PDFA3U = "PDFA3U"
        PDFUA1 = "PDFUA1"
        PDFX1A_2001 = "PDFX1A_2001"
        PDFX1A_2003 = "PDFX1A_2003"
        PDFX3_2002 = "PDFX3_2002"
        PDFX3_2003 = "PDFX3_2003"
        PDFX4 = "PDFX4"
        PDFX4P = "PDFX4P"
    class ContentType:
        BINARY = "BINARY"
        BMP = "BMP"
        GIF = "GIF"
        HTML = "HTML"
        JPEG = "JPEG"
        JSON = "JSON"
        NONE = "NONE"
        PDF = "PDF"
        PNG = "PNG"
        TEXT = "TEXT"
        TIFF = "TIFF"
        XML = "XML"
    class Doctype:
        AUTODETECT = "AUTODETECT"
        HTML5 = "HTML5"
        XHTML = "XHTML"
        XML = "XML"
    class Encryption:
        NONE = "NONE"
        TYPE_128 = "TYPE_128"
        TYPE_40 = "TYPE_40"
    class ErrorPolicy:
        LICENSE = "LICENSE"
        MISSING_RESOURCE = "MISSING_RESOURCE"
    class ExceedingContentAgainst:
        NONE = "NONE"
        PAGE_BORDERS = "PAGE_BORDERS"
        PAGE_CONTENT = "PAGE_CONTENT"
        PARENT = "PARENT"
    class ExceedingContentAnalyze:
        CONTENT = "CONTENT"
        CONTENT_AND_BOXES = "CONTENT_AND_BOXES"
        CONTENT_AND_STATIC_BOXES = "CONTENT_AND_STATIC_BOXES"
        NONE = "NONE"
    class HttpsMode:
        LENIENT = "LENIENT"
        STRICT = "STRICT"
    class JavaScriptMode:
        DISABLED = "DISABLED"
        ENABLED = "ENABLED"
        ENABLED_NO_LAYOUT = "ENABLED_NO_LAYOUT"
        ENABLED_REAL_TIME = "ENABLED_REAL_TIME"
        ENABLED_TIME_LAPSE = "ENABLED_TIME_LAPSE"
    class KeystoreType:
        JKS = "JKS"
        PKCS12 = "PKCS12"
    class LogLevel:
        DEBUG = "DEBUG"
        FATAL = "FATAL"
        INFO = "INFO"
        NONE = "NONE"
        PERFORMANCE = "PERFORMANCE"
        WARN = "WARN"
    class MediaFeature:
        ASPECT_RATIO = "ASPECT_RATIO"
        COLOR = "COLOR"
        COLOR_INDEX = "COLOR_INDEX"
        DEVICE_ASPECT_RATIO = "DEVICE_ASPECT_RATIO"
        DEVICE_HEIGHT = "DEVICE_HEIGHT"
        DEVICE_WIDTH = "DEVICE_WIDTH"
        GRID = "GRID"
        HEIGHT = "HEIGHT"
        MONOCHROME = "MONOCHROME"
        ORIENTATION = "ORIENTATION"
        RESOLUTION = "RESOLUTION"
        WIDTH = "WIDTH"
    class MergeMode:
        APPEND = "APPEND"
        ARRANGE = "ARRANGE"
        OVERLAY = "OVERLAY"
        OVERLAY_BELOW = "OVERLAY_BELOW"
        PREPEND = "PREPEND"
    class OutputIntentDefaultProfile:
        FOGRA39 = "Coated FOGRA39"
        GRACOL = "Coated GRACoL 2006"
        IFRA = "ISO News print 26% (IFRA)"
        JAPAN = "Japan Color 2001 Coated"
        JAPAN_NEWSPAPER = "Japan Color 2001 Newspaper"
        JAPAN_UNCOATED = "Japan Color 2001 Uncoated"
        JAPAN_WEB = "Japan Web Coated (Ad)"
        SWOP = "US Web Coated (SWOP) v2"
        SWOP_3 = "Web Coated SWOP 2006 Grade 3 Paper"
    class OutputType:
        BMP = "BMP"
        GIF = "GIF"
        JPEG = "JPEG"
        PDF = "PDF"
        PNG = "PNG"
        PNG_AI = "PNG_AI"
        PNG_TRANSPARENT = "PNG_TRANSPARENT"
        PNG_TRANSPARENT_AI = "PNG_TRANSPARENT_AI"
        TIFF_CCITT_1D = "TIFF_CCITT_1D"
        TIFF_CCITT_GROUP_3 = "TIFF_CCITT_GROUP_3"
        TIFF_CCITT_GROUP_4 = "TIFF_CCITT_GROUP_4"
        TIFF_LZW = "TIFF_LZW"
        TIFF_PACKBITS = "TIFF_PACKBITS"
        TIFF_UNCOMPRESSED = "TIFF_UNCOMPRESSED"
    class OverlayRepeat:
        ALL_PAGES = "ALL_PAGES"
        LAST_PAGE = "LAST_PAGE"
        NONE = "NONE"
        TRIM = "TRIM"
    class PageOrder:
        BOOKLET = "BOOKLET"
        BOOKLET_RTL = "BOOKLET_RTL"
        EVEN = "EVEN"
        ODD = "ODD"
        REVERSE = "REVERSE"
    class PagesPerSheetDirection:
        DOWN_LEFT = "DOWN_LEFT"
        DOWN_RIGHT = "DOWN_RIGHT"
        LEFT_DOWN = "LEFT_DOWN"
        LEFT_UP = "LEFT_UP"
        RIGHT_DOWN = "RIGHT_DOWN"
        RIGHT_UP = "RIGHT_UP"
        UP_LEFT = "UP_LEFT"
        UP_RIGHT = "UP_RIGHT"
    class PdfScriptTriggerEvent:
        AFTER_PRINT = "AFTER_PRINT"
        AFTER_SAVE = "AFTER_SAVE"
        BEFORE_PRINT = "BEFORE_PRINT"
        BEFORE_SAVE = "BEFORE_SAVE"
        CLOSE = "CLOSE"
        OPEN = "OPEN"
    class ProcessingPreferences:
        SAVE_MEMORY_IMAGES = "SAVE_MEMORY_IMAGES"
    class ResourceType:
        FONT = "FONT"
        IFRAME = "IFRAME"
        IMAGE = "IMAGE"
        OBJECT = "OBJECT"
        RUNNING_DOCUMENT = "RUNNING_DOCUMENT"
        SCRIPT = "SCRIPT"
        STYLESHEET = "STYLESHEET"
        UNKNOWN = "UNKNOWN"
    class SigningMode:
        SELF_SIGNED = "SELF_SIGNED"
        VERISIGN_SIGNED = "VERISIGN_SIGNED"
        WINCER_SIGNED = "WINCER_SIGNED"
    class ViewerPreferences:
        CENTER_WINDOW = "CENTER_WINDOW"
        DIRECTION_L2R = "DIRECTION_L2R"
        DIRECTION_R2L = "DIRECTION_R2L"
        DISPLAY_DOC_TITLE = "DISPLAY_DOC_TITLE"
        DUPLEX_FLIP_LONG_EDGE = "DUPLEX_FLIP_LONG_EDGE"
        DUPLEX_FLIP_SHORT_EDGE = "DUPLEX_FLIP_SHORT_EDGE"
        DUPLEX_SIMPLEX = "DUPLEX_SIMPLEX"
        FIT_WINDOW = "FIT_WINDOW"
        HIDE_MENUBAR = "HIDE_MENUBAR"
        HIDE_TOOLBAR = "HIDE_TOOLBAR"
        HIDE_WINDOW_UI = "HIDE_WINDOW_UI"
        NON_FULLSCREEN_PAGE_MODE_USE_NONE = "NON_FULLSCREEN_PAGE_MODE_USE_NONE"
        NON_FULLSCREEN_PAGE_MODE_USE_OC = "NON_FULLSCREEN_PAGE_MODE_USE_OC"
        NON_FULLSCREEN_PAGE_MODE_USE_OUTLINES = "NON_FULLSCREEN_PAGE_MODE_USE_OUTLINES"
        NON_FULLSCREEN_PAGE_MODE_USE_THUMBS = "NON_FULLSCREEN_PAGE_MODE_USE_THUMBS"
        PAGE_LAYOUT_ONE_COLUMN = "PAGE_LAYOUT_ONE_COLUMN"
        PAGE_LAYOUT_SINGLE_PAGE = "PAGE_LAYOUT_SINGLE_PAGE"
        PAGE_LAYOUT_TWO_COLUMN_LEFT = "PAGE_LAYOUT_TWO_COLUMN_LEFT"
        PAGE_LAYOUT_TWO_COLUMN_RIGHT = "PAGE_LAYOUT_TWO_COLUMN_RIGHT"
        PAGE_LAYOUT_TWO_PAGE_LEFT = "PAGE_LAYOUT_TWO_PAGE_LEFT"
        PAGE_LAYOUT_TWO_PAGE_RIGHT = "PAGE_LAYOUT_TWO_PAGE_RIGHT"
        PAGE_MODE_FULLSCREEN = "PAGE_MODE_FULLSCREEN"
        PAGE_MODE_USE_ATTACHMENTS = "PAGE_MODE_USE_ATTACHMENTS"
        PAGE_MODE_USE_NONE = "PAGE_MODE_USE_NONE"
        PAGE_MODE_USE_OC = "PAGE_MODE_USE_OC"
        PAGE_MODE_USE_OUTLINES = "PAGE_MODE_USE_OUTLINES"
        PAGE_MODE_USE_THUMBS = "PAGE_MODE_USE_THUMBS"
        PICKTRAYBYPDFSIZE_FALSE = "PICKTRAYBYPDFSIZE_FALSE"
        PICKTRAYBYPDFSIZE_TRUE = "PICKTRAYBYPDFSIZE_TRUE"
        PRINTSCALING_APPDEFAULT = "PRINTSCALING_APPDEFAULT"
        PRINTSCALING_NONE = "PRINTSCALING_NONE"
    class XmpPriority:
        HIGH = "HIGH"
        LOW = "LOW"
        NONE = "NONE"
