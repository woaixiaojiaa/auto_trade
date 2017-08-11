from urllib import request
import urllib
import urllib.parse
import time
import hashlib
import hmac
import re

def buy_coins(amount,price,coin='doge'):
    nonce=time.time()
    a='key=(pub_key)&nonce=%d&coin=%s&amount=%d&price=%f&version=2' % (nonce,coin,amount,price)
    self_key_md5=hashlib.md5('(priv_key)'.encode('utf-8')).hexdigest().encode('utf-8')
    data = {'key': '(pub_key)',
            'signature': hmac.new(self_key_md5,a.encode('utf-8'),digestmod=hashlib.sha256).hexdigest(),
            'nonce': '%d' % (nonce),
            'coin': '%s' % (coin),
            'amount': '%d' % (amount),
            'price': '%f' % (price),
            'version': '2',
    }
    postdata = urllib.parse.urlencode(data).encode('utf-8')
    ReqUrl='https://api.btctrade.com/api/buy/'
    request_data = urllib.request.Request(ReqUrl,postdata)
    postdata = urllib.parse.urlencode(data).encode('utf-8')
    with request.urlopen(request_data) as f:
        data = f.read().decode('utf-8')
        print(data)
        if(data.find('true') > 0):
            data_rn_line=list(data.split('"'))
            return int(data_rn_line[3])
        else:
            return 0

def sell_coins(amount,price,coin='doge'):
    nonce=time.time()
    a='key=(pub_key)&nonce=%d&coin=%s&amount=%d&price=%f&version=2' % (nonce,coin,amount,price)
    self_key_md5=hashlib.md5('(priv_key)'.encode('utf-8')).hexdigest().encode('utf-8')
    data = {'key': '(pub_key)',
            'signature': hmac.new(self_key_md5,a.encode('utf-8'),digestmod=hashlib.sha256).hexdigest(),
            'nonce': '%d' % (nonce),
            'coin': '%s' % (coin),
            'amount': '%d' % (amount),
            'price': '%f' % (price),
            'version': '2',
    }
    postdata = urllib.parse.urlencode(data).encode('utf-8')
    ReqUrl='https://api.btctrade.com/api/sell/'
    request_data = urllib.request.Request(ReqUrl,postdata)
    postdata = urllib.parse.urlencode(data).encode('utf-8')
    with request.urlopen(request_data) as f:
        data = f.read().decode('utf-8')
        if(data.find('true') > 0):
            data_rn_line=list(data.split('"'))
            print(data)
            return int(data_rn_line[3])
        else:
            print(data)
            return 0

#0:cancelled-->error occues exit now
#1:closed-->success,do next thing
#2:open-->wait and check twice
def check_order(ID):#checking if transaction success or not
    nonce=time.time()
    a='key=(pub_key)&nonce=%d&id=%d&version=2' % (nonce,ID)
    self_key_md5=hashlib.md5('(priv_key)'.encode('utf-8')).hexdigest().encode('utf-8')
    data = {'key': '(pub_key)',
            'signature': hmac.new(self_key_md5,a.encode('utf-8'),digestmod=hashlib.sha256).hexdigest(),
            'nonce': '%d' % (nonce),
            'id': '%s' % (ID),
            'version': '2',
    }
    postdata = urllib.parse.urlencode(data).encode('utf-8')
    ReqUrl='https://api.btctrade.com/api/fetch_order/'
    request_data = urllib.request.Request(ReqUrl,postdata)
    postdata = urllib.parse.urlencode(data).encode('utf-8')
    with request.urlopen(request_data) as f:
        data = f.read().decode('utf-8')
        print(data)
        if(data.find('cancelled') > 0):
            return 0
        elif(data.find('closed') > 0):
            return 1
        elif(data.find('open') > 0):
            return 2
        else:
            return 0

def cancel_order(ID):#cancel un wanted order
    nonce=time.time()
    a='key=(pub_key)&nonce=%d&id=%d&version=2' % (nonce,ID)
    self_key_md5=hashlib.md5('(priv_key)'.encode('utf-8')).hexdigest().encode('utf-8')
    data = {'key': '(pub_key)',
            'signature': hmac.new(self_key_md5,a.encode('utf-8'),digestmod=hashlib.sha256).hexdigest(),
            'nonce': '%d' % (nonce),
            'id': '%s' % (ID),
            'version': '2',
    }
    postdata = urllib.parse.urlencode(data).encode('utf-8')
    ReqUrl='https://api.btctrade.com/api/cancel_order/'
    request_data = urllib.request.Request(ReqUrl,postdata)
    postdata = urllib.parse.urlencode(data).encode('utf-8')
    with request.urlopen(request_data) as f:
        data = f.read().decode('utf-8')
        print('Data:', data.decode('utf-8'))
        if(data.find('true') > 0):            
            return 1
        else:
            print(data)
            return 0

def get_account_info():#checking if transaction success or not
    nonce=time.time()
    coin_remain=[]        #[doge_reserved,cny_reserved]
    a='key=(pub_key)&nonce=%d&version=2' % (nonce)
    self_key_md5=hashlib.md5('(priv_key)'.encode('utf-8')).hexdigest().encode('utf-8')
    data = {'key': '(pub_key)',
            'signature': hmac.new(self_key_md5,a.encode('utf-8'),digestmod=hashlib.sha256).hexdigest(),
            'nonce': '%d' % (nonce),
            'version': '2',
    }
    postdata = urllib.parse.urlencode(data).encode('utf-8')
    ReqUrl='https://api.btctrade.com/api/balance/'
    request_data = urllib.request.Request(ReqUrl,postdata)
    postdata = urllib.parse.urlencode(data).encode('utf-8')
    with request.urlopen(request_data) as f:
        data = f.read().decode('utf-8')
        m=eval(data)                    #use this way!
        coin_remain.append(float(m['doge_balance']))
        coin_remain.append(float(m['cny_balance']))
    return coin_remain
        
def ask_price(coin):
    price_info=[]
    with request.urlopen('https://api.btctrade.com/api/ticker?coin=%s' % (coin)) as f:
        data = f.read().decode('utf-8')
        #print(data)
        m=eval(data)
        price_info.append(float(m['buy']))
        price_info.append(float(m['sell']))
        #print(price_info)
        return price_info


def conv_price(delay_line,coef_line):#no length check
    result=0.0
    for i in range(len(delay_line)):
        #print(result)
        result=result+(delay_line[i]*coef_line[i])
    return result


account_data=get_account_info()
doge_reserved=account_data[0]
cny_reserved=account_data[1]
doge_buy_price=0.0
doge_sell_price=0.0
delay_line=[0]*64
coef_line=[-8.8056015e-06,-1.7276451e-05,3.9229831e-05,5.9760851e-05,-1.1110593e-04,-1.5866617e-04,2.6063316e-04,3.5434807e-04,-5.3790522e-04,-7.0586957e-04,1.0123268e-03,1.2924484e-03,-1.7748880e-03,-2.2171129e-03,2.9422679e-03,3.6121562e-03,-4.6646098e-03,-5.6508587e-03,7.1432502e-03,8.5747661e-03,-1.0672886e-02,-1.2759479e-02,1.5746005e-02,1.8883779e-02,-2.3335992e-02,-2.8423758e-02,3.5811141e-02,4.5478118e-02,-6.0994078e-02,-8.7364515e-02,1.4869640e-01,4.4948803e-01,4.4948803e-01,1.4869640e-01,-8.7364515e-02,-6.0994078e-02,4.5478118e-02,3.5811141e-02,-2.8423758e-02,-2.3335992e-02,1.8883779e-02,1.5746005e-02,-1.2759479e-02,-1.0672886e-02,8.5747661e-03,7.1432502e-03,-5.6508587e-03,-4.6646098e-03,3.6121562e-03,2.9422679e-03,-2.2171129e-03,-1.7748880e-03,1.2924484e-03,1.0123268e-03,-7.0586957e-04,-5.3790522e-04,3.5434807e-04,2.6063316e-04,-1.5866617e-04,-1.1110593e-04,5.9760851e-05,3.9229831e-05,-1.7276451e-05,-8.8056015e-06
]
while True:
    price_info=[]
    price_info=ask_price(coin='doge')
    
    doge_buy_price=price_info[0]
    #print(doge_buy_price)
    doge_sell_price=price_info[1]
    #print(doge_sell_price)
    delay_line.pop()
    delay_line.insert(0,doge_sell_price)
    #print(delay_line)
    mean_price=conv_price(delay_line,coef_line)
    print('price_now : %f , price_estimate : %f' % (doge_sell_price,mean_price))
    time.sleep(0.1)
