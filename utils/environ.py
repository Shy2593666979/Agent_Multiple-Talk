import os
import config

def set_proxy_environ():

    os.environ['http_proxy']="http://192.168.102.51:8080"

    os.environ['https_proxy']="http://192.168.102.51:8080"

    os.environ['REQUESTS_CA_BUNDLE']="/home/z00013696/Xfusion_Rootcert.crt"

def set_Google_environ():
    os.environ['http_proxy']="http://192.168.102.51:8070"

    os.environ['https_proxy']="http://192.168.102.51:8070"

    os.environ['REQUESTS_CA_BUNDLE']= ''

    os.environ['SERPAPI_API_KEY'] = config.google_key


def set_None_environ():
    
    os.environ['http_proxy']= ''

    os.environ['https_proxy']= ''

    os.environ['REQUESTS_CA_BUNDLE']= ''