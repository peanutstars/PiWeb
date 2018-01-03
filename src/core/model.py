
class WebResponse(dict):
    def __init__(self, success, value, errorMsg=''):
        super(WebResponse, self).\
            __init__(success=success, value=value, errorMsg=errorMsg)
