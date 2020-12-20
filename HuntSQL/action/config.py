# APS scheduler自动任务的类
#flask-aps scheduler
class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': '__main__:hunt',
            'trigger': 'interval',  
            'seconds': 2000,#15min自动寻宝时间
        },
        {
            'id': 'job2',
            'func': '__main__:labour',
            'trigger': 'interval',
            'seconds': 2000,#15min自动interval
        }
    ]