import gzip
from StringIO import StringIO


from device.targets import INSTACAM, IPCAM


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


class InstacamCleaner(Cleaner):
    def __init__(self):
        super(InstacamCleaner, self).__init__(target_url_token=INSTACAM.CLEAN_URL_TOKEN, target_content_token=INSTACAM.CLEAN_CONTENT_TOKEN)

    def clean_content(self, content, environ):
        content = gzip.GzipFile(fileobj=StringIO(content)).read()
        content = content.replace("var address = 'ws://' + window.location.host + '/ws';",
                                  "var address = 'ws://' + window.location.href.split('//')[1] + 'ws';")

        out = StringIO()
        with gzip.GzipFile(fileobj=out, mode="w") as f:
            f.write(content)

        return super(InstacamCleaner, self).clean_content(out.getvalue(), environ)

    def clean_headers(self, headers, environ, url=None, content=None):
        adjusted_headers = headers

        if url and "instacam.amalgamation.js" in url:
            adjusted_headers = [ ]
            for header in headers:
                if header[0].lower() == "content-length":
                    adjusted_headers.append( ("Content-Length", "61505") )
                else:
                    adjusted_headers.append(header)

        return super(InstacamCleaner, self).clean_headers(adjusted_headers, environ, url=url, content=content)


class IPCamCleaner(Cleaner):
    def __init__(self):
        super(IPCamCleaner, self).__init__(target_url_token=IPCAM.CLEAN_URL_TOKEN, target_content_token=IPCAM.CLEAN_CONTENT_TOKEN)

    def clean_content(self, content, environ):
        content = content.replace("<script type=\"text/javascript\" src=\"/jquery-1.8.2.min.js\"></script>",
                                  "<script type=\"text/javascript\" src=\"jquery-1.8.2.min.js\"></script>" )

        content = content.replace("$.getJSON(\"/parameters",
                                  "$.getJSON(\"parameters")

        content = content.replace("$(\"#live\").attr(\"src\", \"/live\");",
                                  "$(\"#live\").attr(\"src\", \"live\");")

        return super(IPCamCleaner, self).clean_content(content, environ)

    def clean_headers(self, headers, environ, url=None, content=None):
        # if url[-1] == "/":
        #     return 500

        return super(IPCamCleaner, self).clean_headers(headers, environ, url=url, content=content)
