import os
import config

# 根据环境进行修改，大部分情况不需要有这些
def set_proxy_environ():

    os.environ['http_proxy']="http://127.0.0.1:8080"

    os.environ['https_proxy']="http://127.0.0.1:8080"

    os.environ['REQUESTS_CA_BUNDLE']="xxxxxxxxxxxxxxxxxxxxxxxxxxx.crt"

def set_Google_environ():
    os.environ['http_proxy']="http://127.0.0.1:8070"

    os.environ['https_proxy']="http://127.0.0.1:8070"

    os.environ['REQUESTS_CA_BUNDLE']= ''

    os.environ['SERPAPI_API_KEY'] = config.google_key


def set_None_environ():
    
    os.environ['http_proxy']= ''

    os.environ['https_proxy']= ''

    os.environ['REQUESTS_CA_BUNDLE']= ''
