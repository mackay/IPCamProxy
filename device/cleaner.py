
class Cleaner(object):

    def __init__(self, target_url_token=None, target_content_token=None):
        self.target_url_token = target_url_token
        self.target_content_token = target_content_token

    def is_target(self, url, content):

        if self.target_content_token:
            if self.target_content_token in content:
                if self.target_url_token:
                    return self.target_url_token in url
                return True

            return False

        return self.target_url_token in url

    def clean_content(self, content, environ):
        return content

    def clean_headers(self, headers, environ, url=None, content=None):
        return headers
