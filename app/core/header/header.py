
def header_builder(response):

    acces_control_allow_origin = '*'  # 'http://' + request.remote_addr
    acces_control_allow_Header = 'Origin, X-Requested-With, Content, Accept, Content-Type, Authorization'
    Access_Control_Allow_Methods = 'GET, POST, PUT, DELETE, PATCH'

    response.headers.set('Access-Control-Allow-Origin', acces_control_allow_origin)
    response.headers.set('Access-Control-Allow-Headers', acces_control_allow_Header)
    response.headers.set('Access-Control-Allow-Methods', Access_Control_Allow_Methods)
