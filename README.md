# 가상화폐 자동투자 프로그램  
업비트 API 와 pyupbit 라이브러리를 사용하여 가상화폐 자동거래를 해 주는 프로그램입니다.  

### 파일구성  
+ backtesting.py : 변동성 돌파 전략 백테스팅 코드  
+ backtesting_v2.py : 변동성 돌파 + best_K 전략 백테스팅 코드
+ cryptoAutoTrade_v0 : 이평선 돌파전략 코드  
+ cryptoAutoTrade_v1 : 변동성 돌파 전략 코드  
+ cryptoAutoTrade_v2 : 변동성 돌파 + best_K 전략 코드(미완)
+ cryptoAutoTrade_v3 : slack 메신저 알람 기능 추가 버전

### 구동
1. 업비트에 고객센터에서 API 를 발급받은 후 access key, secret key 저장한다.
2. crypto-auto 폴더 안에 auth.py 파일을 하나 만들고 access = "본인의 access key 값" secret = "본인의 secret key 값" 을 넣고 저장한다. 이 값은 cryptoAutoTrade 코드에서 import 하여 사용된다. cryptoAutoTrade_v3 이상의 버전에서는 slack 메신저를 위해 myToken = "본인의 slack API OAuth token 값", channel = "알림을 받을 채널명" 도 추가해줘야 한다.
3. backtesting, cryptoAutoTrade 파일 내부 변수를 원하는 변수로 바꾸어준다. coin : 투자할 가상화폐의 ticker, fees : 수수료, day_count : 백테스팅 시 불러올 데이터의 수 등
4. 필요한 모듈 다운로드
    + pip install pyupbit
    + pip install openpyxl
    + pip install requests
    + ...
5. 실행

### 백그라운드 실행(서버)
+ 패키지 목록 업데이트: sudo apt update
+ pip3 설치: sudo apt install python3-pip
+ 서버시간 설정 : sudo ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime  
+ 백그라운드 실행 : nohup python cryptoAutoTrade_v3.py > output.log &  
+ 프로세스 확인 : ps -ef | grep .py  
+ 프로세스 종료 : kill -9 PID  (PID 는 ps 명령의 출력값에서 해당 프로세스의 맨 앞의 숫자)  

### 개발 과정 포스팅
1. 업비트 API : https://poalim.tistory.com/27  
2. 변동성 돌파 전략 및 백테스팅 : https://poalim.tistory.com/29
3. 변동성 돌파전략 구현 : https://poalim.tistory.com/30
4. best_K 전략 추가 및 백테스팅 : https://poalim.tistory.com/31
5. slack 메신저 알람기능 추가 : https://poalim.tistory.com/32
