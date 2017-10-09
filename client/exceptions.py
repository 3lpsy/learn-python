class Http500Exception(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self,*args,**kwargs)

class Http404Exception(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self,*args,**kwargs)
