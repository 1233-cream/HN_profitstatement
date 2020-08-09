a='123是{0}'
b='asd数字asd'
c='qwt'
try:
    exec("""prin{1}('123是{0}')
    """.format(b[3:],c[2]))
except:
    pass