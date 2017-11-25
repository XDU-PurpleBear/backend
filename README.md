# backend


3个分支 X Z K

backend 分成5个模块
	
* main.py
* database.py
* frontend.py
* user.py
* book.py

分工：

曾：User book <=> DB
许：John <=> login logout Infomation
康：frontend <=> signup


前端API：

login: 

* request: tele/usrname password
* response: Success/Fail & information

logout:

* request: token
* response: Success/Fail & information

signup:

* request: usrname password
* response: Success/Fail & information

UsrInfoModified:

* request: token
* response: Success/Fail & information


login:

* usr/librian login API
* ADDR: /api/v1/login
* METHOD:POST
* HEAD:tel-number/usrname password 
* RETURN: success,token,token-date,usrtype / fail & error information


logout:

* usr/librian logout API
* ADDR: /api/v1/logout
* METHOD:POST
* HEAD:token
* RETURN:success/fail & error information

signup:

* usr/librian signup API
* ADDR:/api/v1/signup
* METHOD:POST
* HEAD:usrname password
* RETURN:success /fail & error information

UsrInfoModified:

* usr information Modified API
* ADDR: /api/v1/usrinfoModified
* METHOD:POST
* HEAD:token Info
* RETURN: success /fail & error information,token-time

getApiVersion:

* developer getApiVersion API
* ADDR:api/api-version
* METHOD:POST
* HEAD:api-version
* RETURN:api-version:v1/v2/...

