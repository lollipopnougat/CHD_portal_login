# 长安大学信息门户的模拟登录模块

本模块可以用于爬虫模拟登录长安大学信息门户

## 相关内容

- [学校信息门户模拟登录之密码加密](https://hanechiri.github.io/post/portal_login_encrypt/#more)
- [学校信息门户模拟登录](https://hanechiri.github.io/post/portal_login/#more)

## 构成

- `portal_login`

  - `__init__.py`
  - `encrypt.py`
  - `login.py`

## 示例代码

### 运行示例

首先请先安装依赖:

#### Windows 

以**管理员身份运行PowerShell或CMD**，输入

```bash
pip install pycryptodomex
```

#### Linux 和 Mac 

请使用 shell 执行 (这里还有坑!有些资料上说是 `pycryptodome` ，然而安上并不能用...最后还是用了 `pycryptodomex` )

```bash
pip install pycryptodomex
```

经过测试在 `Android` 上也能跑起来(使用[NeoTerm](https://github.com/NeoTerm/NeoTerm))

### 示例1 (原 `test.py`)

```python
from portal_login.login import *
if __name__ == '__main__':
    login_url = 'http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F'
    home_page_url = 'http://portal.chd.edu.cn/index.portal?.pn=p167'
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }
    cookies = login(login_url,headers,home_page_url)#此函数最终返回一个cookies
```

#### 示例1 运行结果

```bash
输入用户名: xxxxxxxxx
输入密码: xxxxxxxxx
登录成功
```

### 示例2

就是这个项目所附带的的 `test.py` ，包含了获取信息门户的成绩功能，具体请查看[代码](https://github.com/lollipopnougat/CHD_portal_login/blob/master/test.py)


#### 示例2 运行结果

![结果1](https://lollipopnougat.github.io/website-calculator/img/chdgpa1.png)
![结果2](https://lollipopnougat.github.io/website-calculator/img/chdgpa2.png)

# 登录过程分析

1. 浏览器获取登录表单数据，向`http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F`发起POST请求，得到302（重定向）的response，让浏览器请求其Location指示的网址。response给了浏览器几个cookies：CASPRIVACY、CASTGC和iPlanetDirectoryPro

2. 浏览器携带这些cookies，向新的网址`http://portal.chd.edu.cn/?ticket=ST-854426-Aye0eVjF4JmBvQyJa0le1563260380765-JRua-cas`发起GET请求，得到302的response，得到新的cookies：MOD_AUTH_CAS

3. 浏览器携带这些cookies，向新的网址`http://portal.chd.edu.cn/`发起GET请求，得到200的response，并给予新的cookies，也就是最重要的cookies：JSESSIONID

# 参考链接

- [使用cookies做PHP用户登录详解-CSDN](https://blog.csdn.net/awhip9/article/details/78007600)
- 如果导入本模块出了问题可以看这个：[Python 3.x可能是史上最详解的【导入（import）】-CSDN](https://blog.csdn.net/weixin_38256474/article/details/81228492)

