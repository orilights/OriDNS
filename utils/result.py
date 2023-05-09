class Result():

    @staticmethod
    def ok(msg='success', data=None):
        return {'success': True, 'msg': msg, 'data': data}

    @staticmethod
    def fail(msg):
        return {'success': False, 'msg': msg}
