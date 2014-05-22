#-*- coding:utf-8 -*-
import urllib2
import json
import httplib
from urlparse import urlparse
from urllib import quote
import time
from imaplib import Response_code

SWIFT_DATA_ENDPOINT = 'http://219.245.80.4:8090/v1/AUTH_'
SWIFT_TOKEN_ENDPOINT = 'http://219.245.80.4:8089/v2.0/tokens'

class Swift:
    
    """
    The __init__ method.
    @param auth_url: The url of the authorization.
    @type auth_url: URL string.
    @param data_url: The url of data operation.
    @type data_url: URL string.
    @param user_name: The name of the user.
    @type user_name: String.
    @param passwd: The password of the user.
    @type passwd: String.
    @param tenant_id: The id of the tenant.
    @type tenant_id: String.
    """
    def __init__(self, auth_url = None, data_url = None, user_name = None,
                 passwd = None, tenant_name = None):
        self.auth_url = auth_url
        self.data_url = data_url
        self.user_name = user_name
        self.password = passwd
        self.tenant_name = tenant_name

    """
    The get server request method.
    @param server_api: The url to get server_request.
    @type server_api: URL string.
    @param auth_token: The id of the token.
    @type auth_token: String.
    @param send_data: The data to send.
    @type: JSON String.
    @param method: The method of operation.
    @type method: String of operation type.
    """
    def get_server_request(self, server_api = None, auth_token = None,
                           send_data = None, method = None):
        if not server_api:
            return None
    
        server_request = urllib2.Request(server_api)
        if not server_request:
            return None

        server_request.add_header('Content-Type', 'application/json;charset=utf8')
        server_request.add_header('Accept', 'application/json')
        server_request.add_header('User-Agent', 'python-mikeyp')
        if auth_token:
            server_request.add_header('X-Auth-Token', auth_token)
        if send_data:
            server_request.add_header('Content-Length', len(send_data))
            server_request.add_data(send_data)
        if method:
            server_request.get_method = lambda: method
    
        return server_request
    
    """
    The get keystone token method.
    @param server_api: The url to get key stone token.
    @type server_api: URL string.
    @return: A tuple contains tenant_id and token_id.
    @rtype: Tuple.
    """
    def get_keystone_token(self, server_api):
        # Construct the data of the message to send.
        # The response is like the following:
        
#         {
#     'access': {
#         'token': {
#             'issued_at': '2014-05-21T12: 12: 37.655205',
#             'expires': '2014-05-22T12: 12: 37Z',
#             'id': 'MIIGNgYJKoZIhvcNAQcCoIIGJzCCBiMCAQExCTAHBgUrDgMCGjCCBIwGCSqGSIb3DQEHAaCCBH0EggR5eyJhY2Nlc3MiOiB7InRva2VuIjogeyJpc3N1ZWRfYXQiOiAiMjAxNC0wNS0yMVQxMjoxMjozNy42NTUyMDUiLCAiZXhwaXJlcyI6ICIyMDE0LTA1LTIyVDEyOjEyOjM3WiIsICJpZCI6ICJwbGFjZWhvbGRlciIsICJ0ZW5hbnQiOiB7ImRlc2NyaXB0aW9uIjogbnVsbCwgImVuYWJsZWQiOiB0cnVlLCAiaWQiOiAiZWYyN2IyMjE4Y2MyNGFmMzg5NGQ5YzlhYzZhMzNhZTciLCAibmFtZSI6ICJoaGg0In19LCAic2VydmljZUNhdGFsb2ciOiBbeyJlbmRwb2ludHMiOiBbeyJhZG1pblVSTCI6ICJodHRwOi8vMTkyLjE2OC4wLjIwOjgwODAvdjEvQVVUSF9lZjI3YjIyMThjYzI0YWYzODk0ZDljOWFjNmEzM2FlNyIsICJyZWdpb24iOiAiUmVnaW9uT25lIiwgImludGVybmFsVVJMIjogImh0dHA6Ly8xOTIuMTY4LjAuMjA6ODA4MC92MS9BVVRIX2VmMjdiMjIxOGNjMjRhZjM4OTRkOWM5YWM2YTMzYWU3IiwgImlkIjogIjA5YjA1ZGNmZWFhZDRjNjY4MDQwOTY2ZDhlMTVmNTE0IiwgInB1YmxpY1VSTCI6ICJodHRwOi8vMTkyLjE2OC4wLjIwOjgwODAvdjEvQVVUSF9lZjI3YjIyMThjYzI0YWYzODk0ZDljOWFjNmEzM2FlNyJ9XSwgImVuZHBvaW50c19saW5rcyI6IFtdLCAidHlwZSI6ICJvYmplY3Qtc3RvcmUiLCAibmFtZSI6ICJzd2lmdCJ9LCB7ImVuZHBvaW50cyI6IFt7ImFkbWluVVJMIjogImh0dHA6Ly8xOTIuMTY4LjAuMjA6MzUzNTcvdjIuMCIsICJyZWdpb24iOiAiUmVnaW9uT25lIiwgImludGVybmFsVVJMIjogImh0dHA6Ly8xOTIuMTY4LjAuMjA6NTAwMC92Mi4wIiwgImlkIjogIjM3ZGEwMzgyOTRlZDRhOTdiZDk5MTQ4ODUwODJjNGVjIiwgInB1YmxpY1VSTCI6ICJodHRwOi8vMTkyLjE2OC4wLjIwOjUwMDAvdjIuMCJ9XSwgImVuZHBvaW50c19saW5rcyI6IFtdLCAidHlwZSI6ICJpZGVudGl0eSIsICJuYW1lIjogImtleXN0b25lIn1dLCAidXNlciI6IHsidXNlcm5hbWUiOiAiaGhoNCIsICJyb2xlc19saW5rcyI6IFtdLCAiaWQiOiAiZTcxODBjMDc4OWY5NGIyN2IzMDljMTg4YmI2ODJkYmYiLCAicm9sZXMiOiBbeyJuYW1lIjogImFkbWluIn1dLCAibmFtZSI6ICJoaGg0In0sICJtZXRhZGF0YSI6IHsiaXNfYWRtaW4iOiAwLCAicm9sZXMiOiBbIjY4ODViN2FhMDc3ODRjYTc5YWNmMGRlNmQ1MzRmNTEyIl19fX0xggGBMIIBfQIBATBcMFcxCzAJBgNVBAYTAlVTMQ4wDAYDVQQIDAVVbnNldDEOMAwGA1UEBwwFVW5zZXQxDjAMBgNVBAoMBVVuc2V0MRgwFgYDVQQDDA93d3cuZXhhbXBsZS5jb20CAQEwBwYFKw4DAhowDQYJKoZIhvcNAQEBBQAEggEAdJpgUC+OH9liFL7RI6N-8zW9MBUsa5sk7st-rvBRitp+Ja0Tez9h0NGyB3vyJcz64trSg51qQ3N4znkaPALilKFXgHneDqwUPNTnhyORt5xbvwc8InxDwZ5dHWYbU51aroynAFHCgWhjnDSxEgkdfWiUot6EcRpuHV0U7SCSvrdd6ZHYrWa+7qMj8UBpdLzAI5V7KGi5W4fB9d00DnIYlDkeEQqnCm8OfbWGNlXla0DJUFFuTIC-nsLwNF0UEJgTS-czP5YHYYYd3W+cDThJHtntTfXuCagkLqpWSBe3Uiv3GOgPo8bhYJFsnvNjtTIDkpp1OH8dL1TOVgV+BVY0NQ==',
#             'tenant': {
#                 'enabled': True,
#                 'description': None,
#                 'name': 'hhh4',
#                 'id': 'ef27b2218cc24af3894d9c9ac6a33ae7'
#             }
#         },
#         'serviceCatalog': [
#             {
#                 'endpoints_links': [
#                      
#                 ],
#                 'endpoints': [
#                     {
#                         'adminURL': 'http: //192.168.0.20: 8080/v1/AUTH_ef27b2218cc24af3894d9c9ac6a33ae7',
#                         'region': 'RegionOne',
#                         'publicURL': 'http: //192.168.0.20: 8080/v1/AUTH_ef27b2218cc24af3894d9c9ac6a33ae7',
#                         'internalURL': 'http: //192.168.0.20: 8080/v1/AUTH_ef27b2218cc24af3894d9c9ac6a33ae7',
#                         'id': '09b05dcfeaad4c668040966d8e15f514'
#                     }
#                 ],
#                 'type': 'object-store',
#                 'name': 'swift'
#             },
#             {
#                 'endpoints_links': [
#                      
#                 ],
#                 'endpoints': [
#                     {
#                         'adminURL': 'http: //192.168.0.20: 35357/v2.0',
#                         'region': 'RegionOne',
#                         'publicURL': 'http: //192.168.0.20: 5000/v2.0',
#                         'internalURL': 'http: //192.168.0.20: 5000/v2.0',
#                         'id': '37da038294ed4a97bd9914885082c4ec'
#                     }
#                 ],
#                 'type': 'identity',
#                 'name': 'keystone'
#             }
#         ],
#         'user': {
#             'username': 'hhh4',
#             'roles_links': [
#                  
#             ],
#             'id': 'e7180c0789f94b27b309c188bb682dbf',
#             'roles': [
#                 {
#                     'name': 'admin'
#                 }
#             ],
#             'name': 'hhh4'
#         },
#         'metadata': {
#             'is_admin': 0,
#             'roles': [
#                 '6885b7aa07784ca79acf0de6d534f512'
#             ]
#         }
#     }
# }
        
        if self.user_name and self.password and self.tenant_name:
            send_data = {'auth': {'tenantName': self.tenant_name, 'passwordCredentials': \
                               {'username': self.user_name, 'password': self.password}}}
        if not send_data:
            return None, None
        
        # Get server request.
        server_request = self.get_server_request(server_api, None, json.dumps(send_data), None)
        
        if not server_request:
            return None, None
        try:
            server_response = urllib2.urlopen(server_request)
            receiver_data = server_response.read()
            if receiver_data:
                data = json.loads(receiver_data)
#                 catalogs = data['access']['serviceCatalog']
#                 for service in catalogs:
#                     if service['type'] == 'object-store':
#                         url = service['endpoints'][0]['publicURL']
                token_id = data['access']['token']['id']
                tenant_id = data['access']['token']['tenant']['id']
                return (tenant_id, token_id)
            else:
                return None, None
        except Exception:
            return None, None

    """
    The get container list method.
    @param server_api: The url to get key stone token.
    @type server_api: String.
    @param tenant_id: The id of the tenant.
    @type tenant_id: String.
    @param token_id: The id of the token.
    @type token_id: String.
    @return: A list contains the name of the containers.
    @rtype: List.
    """
    def container_list(self, server_api = None, tenant_id = None, token_id = None):
        if server_api and tenant_id:
            server_api += tenant_id
        else:
            return False
        
        # Get server request.
        try:
            server_request = self.get_server_request(server_api, token_id, None, None)
            if not server_request:
                return False

            server_response = urllib2.urlopen(server_request)
            receiver_data = server_response.read()
            if receiver_data:
                # The receiver-data is in type:
#                 [{"count": 20,
#                      "bytes": 258299710, 
#                      "name": "myfile"}, 
#                  {"count": 1, 
#                      "bytes": 72, 
#                      "name": "mytest"}]
                data = json.loads(receiver_data) # Deserialize receiver_dat to a Python object.
                con_list = []
                for d in data:
                    con_list.append(d['name'])
                return con_list
            return False
        except Exception:
            return False

    """
    The create container method, can't create container in Chinese.
    @param server_api: The url to get key stone token.
    @type server_api: String.
    @param tenant_id: The id of the tenant.
    @type tenant_id: String.
    @param container_name: The name of the container to create.
    @type container_name: String.
    @param token_id: The id of the token.
    @type token_id: String.
    @return: The status of create containers.
    @rtype: Booleans
    """
    def container_create(self, server_api = None, tenant_id = None, container_name = None,
                         token_id = None):
        if server_api and tenant_id and container_name and token_id:
            if container_name in self.container_list(server_api, tenant_id, token_id):
                return True
            server_api += tenant_id + "/" + container_name
        else: # At leat one param is none.
            return False
#         if not server_api:
#             return False
    
        try:
            server_request = self.get_server_request(server_api, token_id, None, "PUT")
            if not server_request:
                return False
            server_response = urllib2.urlopen(server_request)
            response_code = server_response.getcode()
            if response_code in range(200, 300): # The code is possibly be 201 or 202
                return True
            else:
                return False
#             receiver_data = server_response.read()
#             print "receiver_data:", receiver_data
#             if receiver_data:
#                 data = json.dumps(receiver_data)
#                 return data
#                 return True
        except Exception as exception:
            print exception
            return False
    
    """
    The delete container method, currently can't delete container
    that contains object in Chinese due to encode charset.
    @param server_api: The url to get key stone token.
    @type server_api: String.
    @param container_name: The name of the container to delete.
    @type container_name: String.
    @param tenant_id: The id of the tenant.
    @type tenant_id: String.
    @param token_id: The id of the token.
    @type token_id: String.
    @return: The status of create containers.
    @rtype: Booleans
    """
    def container_delete(self, server_api = None, container_name = None, tenant_id = None, token_id = None):
        if container_name not in self.container_list(server_api, tenant_id, token_id):
            return True # The container is not in the container list.
        obj_list= self.object_list(server_api, tenant_id, container_name, token_id)
        if obj_list:
            for obj in obj_list:
#                 print "obj:", obj
                self.object_delete(server_api, tenant_id, token_id, container_name, obj)
    
        if server_api and tenant_id and container_name:
            server_api += tenant_id + "/" + container_name
    
        if not server_api:
            return False
    
        try:
            server_request = self.get_server_request(server_api, token_id, None, "DELETE")
    
            if not server_request:
                return False
            server_response = urllib2.urlopen(server_request)
            response_code = server_response.getcode()
            if response_code in range(200, 300): # The code is possibly be 204.
                return True
            else:
                return False
#             receiver_data = server_response.read()
#             if receiver_data:
#                 data = json.dumps(receiver_data)
#                 return data
        except Exception as exception:
            print exception
            return False
    
    """
    The get object list method.
    @param server_api: The url to get key stone token.
    @type server_api: String.
    @param tenant_id: The id of the tenant.
    @type tenant_id: String.
    @param container_name: The name of the container to create.
    @type container_name: String.
    @param token_id: The id of the token.
    @type token_id: String.
    @return: The list of objects in specified container.
    @rtype: List.
    """
    def object_list(self, server_api = None, tenant_id = None, container_name = None, token_id = None):
        if server_api and tenant_id and container_name:
            server_api += tenant_id + "/" + container_name
        else:
            return False
    
        try:
            server_request = self.get_server_request(server_api, token_id)
    
            if not server_request:
                return False
            server_response = urllib2.urlopen(server_request)
    
            receiver_data = server_response.read()
            if receiver_data:
                data = json.loads(receiver_data)
                obj_list = []
                for d in data:
                    obj_list.append(d['name'])
                return obj_list
            return False
    
        except Exception:
            return False
    
    '''
    Setup an http connection.
    '''
    def http_connection(self, url, proxy = None):
        parsed = urlparse(url) # Parse an url into 6 parts.
#         print "http_connection:", parsed.netloc
        conn = httplib.HTTPConnection(parsed.netloc) # Get an HTTPConnection instance.
        return parsed, conn
    
    """
    The delete object method.
    @param server_api: The url to get key stone token.
    @type server_api: String.
    @param tenant_id: The id of the tenant.
    @type tenant_id: String.
    @param token_id: The id of the token.
    @type token_id: String.
    @param container_name: The name of the container the object is in.
    @type container_name: String.
    @param object_name: The name of the object to delete.
    @type object_name: String.
    @param http_conn: An instance of http connection.
    @type http_conn: Instance.
    @param headers: The headers of an http request.
    @type headers: Dictionary.
    @param proxy: The address of proxy.
    @type proxy: URL string.
    @return: The status of deleting specified object.
    @rtype: Booleans.
    """
    def object_delete(self, server_api = None, tenant_id = None, token_id = None,
                     container_name =None, object_name = None, http_conn = None,
                     headers = None, proxy = None):
        if http_conn:
            parsed, conn = http_conn
        elif server_api and tenant_id:
            server_api += tenant_id
            parsed, conn = self.http_connection(server_api, proxy=proxy)
        path = parsed.path
        if container_name:
            path = '%s/%s' % (path.rstrip('/'), quote(container_name))
        if object_name:
            path = '%s/%s' % (path.rstrip('/'), quote(object_name))
        if headers:
            headers = dict(headers)
        else:
            headers = {}
        if token_id:
            headers['X-Auth-Token'] = token_id
        conn.request('DELETE', path, '', headers)
        resp = conn.getresponse()
        resp.read()

        status = resp.status # Get the response code.
        if status in range(200, 300): # The code is possibly be 204.
            return True
        else:
            return False

    
    '''
    def object_upload(self, server_api = None, tenant_id = None, token_id = None,
                      local_path = None, container_name = None, object_name = None):
        
        if server_api and tenant_id:
            server_api += tenant_id
        else:
            return False
        
        if not local_path:
            return False
        local_path = unicode(local_path,'utf8') # Encode into utf8, incase of Chinese character.
        with open(local_path, 'rb') as contents:
            chunk_size=65536
            parsed, conn = self.http_connection(server_api)
            path = parsed.path
            path = '%s/%s' % (path.rstrip('/'), quote(container_name))
    #        name =name.encode('utf8')
            path = '%s/%s' % (path.rstrip('/'), quote(object_name))
            headers = {}
            headers['X-Auth-Token'] = token_id
            conn.putrequest('PUT', path)
            for header, value in headers.iteritems():
                conn.putheader(header, value)
            conn.putheader('Transfer-Encoding', 'chunked')
            conn.endheaders()
            chunk = contents.read(chunk_size)
            while chunk:
                conn.send('%x\r\n%s\r\n' % (len(chunk), chunk))
                chunk = contents.read(chunk_size)
            conn.send('0\r\n\r\n')
    
        resp = conn.getresponse()
        body = resp.read()
        return body
    '''

    """
    The upload object method.
    @param server_api: The url to get key stone token.
    @type server_api: String.
    @param tenant_id: The id of the tenant.
    @type tenant_id: String.
    @param token_id: The id of the token.
    @type token_id: String.
    @param local_path: The file path of local file to upload.
    @type local_path: File path string.
    @param container_name: The name of the container the object is uploading to.
    @type container_name: String.
    @param object_name: The name of the object to upload
    @type object_name: String.
    @param content: The content to send.
    @type content: String.
    @param content_length: The length of the content.
    @type content_length: Integer.
    @param etag: A tag of the header.
    @type etag: String.
    @param chunk_size: The size of the block to send.
    @type chunk_size: Integer.
    @param content_type: The type of the content to send.
    @type content_type: String.
    @param headers: The headers of an http request.
    @type headers: Dictionary.
    @param http_conn: An instance of http connection.
    @type http_conn: Instance.
    @param proxy: The address of proxy.
    @type proxy: URL string.
    @return: The status of uploading specified object.
    @rtype: Booleans.
    """
    def object_upload(self, server_api = None, tenant_id = None, token_id = None,
                      local_path = None, container_name = None, object_name = None,
                      content = None, content_length = None, etag = None, chunk_size = 65536,
                   content_type = None, headers = None, http_conn = None, proxy = None):
        if container_name not in self.container_list(server_api, tenant_id, token_id):
            return False
        if http_conn:
            parsed, conn = http_conn
        elif server_api and tenant_id: # The sever_api and id of the tenant.
            server_api += tenant_id
            parsed, conn = self.http_connection(server_api, proxy=proxy)
        else:
            return False
        path = parsed.path
        if container_name and object_name:
            path = '%s/%s' % (path.rstrip('/'), quote(container_name))
            path = '%s/%s' % (path.rstrip('/'), quote(object_name))
        else:
            return False
        if headers:
            headers = dict(headers)
        else:
            headers = {}
        if token_id:
            headers['X-Auth-Token'] = token_id
        else:
            return False
        if etag:
            headers['ETag'] = etag.strip('"')
        if content_length is not None:
            headers['Content-Length'] = str(content_length)
        else:
            for n, v in headers.iteritems():
                if n.lower() == 'content-length':
                    content_length = int(v)
        if content_type is not None:
            headers['Content-Type'] = content_type
        if local_path:
            local_path = unicode(local_path, 'utf8') # Encode into unicode.
        else:
            return False
        with open(local_path, 'rb') as contents: # Open in 'rb' mode to be more portable.
            if hasattr(contents, 'read'):
                conn.putrequest('PUT', path)
                for header, value in headers.iteritems():
                    conn.putheader(header, value)
                if content_length is None:
                    conn.putheader('Transfer-Encoding', 'chunked')
                    conn.endheaders()
                    chunk = contents.read(chunk_size)
                    while chunk:
                        conn.send('%x\r\n%s\r\n' % (len(chunk), chunk))
                        chunk = contents.read(chunk_size)
                    conn.send('0\r\n\r\n')
                else: # content_length is set.
                    conn.endheaders()
                    left = content_length
                    while left > 0:
                        size = chunk_size
                        if size > left:
                            size = left
                        chunk = contents.read(size)
                        conn.send(chunk)
                        left -= len(chunk)
            else:
                conn.request('PUT', path, contents, headers) # Send a request to the server.
        resp = conn.getresponse() # Get the server response, and get an instance of HTTPResponse.
        resp.read() # Read the response, so you can do another request.
        headers = {'X-Auth-Token': token_id}
#         return resp.getheader('etag', '').strip('"')
        status = resp.status # Get the HTTPResponse code.
        if status in range(200, 300): # The code is possibly be 201
            return True
        else:
            return False

    '''
    The download object method.
    @param server_api: The url to get key stone token.
    @type server_api: String.
    @param tenant_id: The id of the tenant.
    @type tenant_id: String.
    @param token_id: The id of the token.
    @type token_id: String.
    @param container_name: The name of the container the object is uploading to.
    @type container_name: String.
    @param object_name: The name of the object to upload
    @type object_name: String.
    @param local_path: The file path of local file to upload.
    @type local_path: File path string.
    @return: The status of downloading specified object.
    @rtype: Booleans.
    '''
    def object_download(self, server_api = None, tenant_id = None, token_id = None,
                        container_name = None, object_name = None, local_path = None):
        resp_chunk_size = 65536 # The size of downloading big files.
        if not object_name:
            return False
        else:
            uobject_name = unicode(object_name,'utf8') # Encode into utf8, then check the list of objects.
            if uobject_name not in self.object_list(server_api, tenant_id, container_name, token_id):
                return False
        if server_api and tenant_id:
            server_api += tenant_id
            parsed, conn = self.http_connection(server_api)
        else:
            return False
        if container_name and object_name:
            path = '%s/%s/%s' % (parsed.path, quote(container_name), quote(object_name))
        else:
            return False
        method = 'GET'
        headers = {'X-Auth-Token': token_id}
        conn.request(method, path, '', headers)
        resp = conn.getresponse() # Get the server response, and get an instance of HTTPResponse.
        buf = resp.read(resp_chunk_size) # Read data into buffer.
        local_path = unicode(local_path,'utf8') # The name to store the downloaded file.
        file_object = open(local_path,'wb') # Open the local file in 'wb' mode to write into the file.
        while buf: # While the buffer is not empty, write into the file.
            file_object.write(buf)
            buf = resp.read(resp_chunk_size)
        file_object.close()
        resp_headers = {}
        for header, value in resp.getheaders(): # Construct the response headers.
            resp_headers[header.lower()] = value
#         return resp_headers

# The resp_headers is something like the following.
#     {
#     "content-length": "156455055",
#     "accept-ranges": "bytes",
#     "last-modified": "Thu, 22May201403: 46: 40GMT",
#     "etag": "c4977c11bec3b9554d999cdfe35d130e",
#     "x-timestamp": "1400730400.02008",
#     "date": "Thu, 22May201403: 46: 55GMT",
#     "content-type": "video/x-flv"
#     }

        status = resp.status # The status code is possibly be 200.
        if status in range(200, 300):
            return True
        else:
            return False

    
if __name__ == '__main__':
    swift_op = Swift(SWIFT_TOKEN_ENDPOINT, SWIFT_DATA_ENDPOINT, 'hhh4', '123', 'hhh4')
    tenant_id, token_id = swift_op.get_keystone_token(SWIFT_TOKEN_ENDPOINT)
#     print tenant_id
#     print token_id
# Container operation.
#     print swift_op.container_list(SWIFT_DATA_ENDPOINT, tenant_id, token_id)
#     print swift_op.container_create(SWIFT_DATA_ENDPOINT, tenant_id, "mytest", token_id)
#     print swift_op.container_list(SWIFT_DATA_ENDPOINT, tenant_id, token_id)

# Object upload operation.
#     print swift_op.object_list(SWIFT_DATA_ENDPOINT, tenant_id, "mytest", token_id)
#     print swift_op.object_upload(SWIFT_DATA_ENDPOINT, tenant_id, token_id, "C:/Users/Jack/Desktop/测试/红包.txt",
#                                 "mytest", "ios2.txt")
#     print swift_op.object_list(SWIFT_DATA_ENDPOINT, tenant_id, "mytest", token_id)

# Object upload operation.

#     print swift_op.object_download(SWIFT_DATA_ENDPOINT, tenant_id, token_id, "mytest", "红包.txt",
#                                    "C:/Users/Jack/Desktop/红包.txt")

# Object delete operation.
#     print swift_op.object_list(SWIFT_DATA_ENDPOINT, tenant_id, "mytest", token_id)
#     print swift_op.object_delete(SWIFT_DATA_ENDPOINT, tenant_id, token_id, "mytest", "ios2.txt")
#     print swift_op.object_list(SWIFT_DATA_ENDPOINT, tenant_id, "mytest", token_id)
#     
#     print swift_op.container_delete(SWIFT_DATA_ENDPOINT, "mytest", tenant_id, token_id)
#     print swift_op.container_list(SWIFT_DATA_ENDPOINT, tenant_id, token_id)