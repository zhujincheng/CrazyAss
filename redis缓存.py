#_author:  Administrator
#date:  2018/3/26 0026
import redis

r = redis.Redis(host='192.168.0.125', port=6379,)
r.set('foo', 'Bar')
print(r.get('foo'))
print(r.get('name'))
print(r.set('hello'))
      
"""
注释1
"""
