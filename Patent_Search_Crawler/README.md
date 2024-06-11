# 專利爬蟲  

## REMEMBER
* del the save page part of `get_page()`  
or your computer will be filled with htmls  

## 環境安裝  
1. `python -m venv venv`  
1. `venv/Script/Activate`  
1. `pip install -r requirements.txt`  
  
## Proxy Pool 使用  
~~還沒測試 大致上有實做~~  
~~搭配 [proxy_pool](https://github.com/jhao104/proxy_pool) 的 docker~~  
目前使用webshare 的免費帳號提供的10個proxy
之前的repo有洩漏我的API
如果之後要改成public repo 要處理掉

## TODO  
- [ ] SQLite logger  
- [ ] Async (may not because of the website anti crawl)  
- [X] fix next page? (im not sure if it brokes)  

## FIXME
- [X] 使用proxy，否則超快就擋connections  

