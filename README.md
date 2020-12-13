"# Python-flask-web-2020" 


### Flask는 웹 어플리케이션 개발을 위해 파이썬으로 구동되는 프레임워크이다.  
Flask 프레임워크: https://palletsprojects.com/p/flask/  
 물론 파이썬으로 웹 개발을 할 때 많이 쓰이는 프레임워크로 가장 유명한 것은 Django(장고).  
 웹에 대한 이해가 풍부한 사람은 복잡하고 기능이 많은 장고를 잘 활용할 수 있을 것이다.
flask는 Django프레임워크보다 가볍고, 작은 서버부터 스케일 큰 서버를 만들수가 있으며,   
Jinja와 Werkzeug를 포함하고 있다.  

최소한의 구성 요소와 요구 사항을 제공하기 때문에 시작하기 쉽고 필요에 따라 유연하게 사용할 수 있다.   
그렇다고 해서 완전한 기능을 갖춘 앱을 만들기에 제약이 있다는 뜻은 아니고,  
오히려 쉽게 확장할 수 있도록 설계되어 있기 때문에 개발을 하는 입장에서는 본인이 필요한 도구와 라이브러리를 자유롭게 선택해서 적용 가능하다는 게 가장 큰 장점이 아닐까 싶다.   
(데이터베이스를 통합하거나 계정 인증 등을 포함하는 복잡한 앱 뿐만 아니라 단순한 정적 웹 사이트를 만드는 데도 유용하다.)   feat.아무튼워라밸


###Jinja2란
Jinja2(이하 Jinja)는 Python 웹 프레임워크인 Flask에 내장되어 있는 Template 엔진이다.   
Jinja는 JSP의 문법이나 ES6의 template string과 비슷한 문법을 가지고 있다.  
(이 템플릿엔진을 사용해서 애플리케이션 내 변수와 반복문, 조건문 등을 포함하는 HTML 파일을 렌더링할 수 있다. )  

Jinja 문법은 간단히 아래와 같다.  
> {{ ... }} : 변수나 표현식  
> {% ... %} : if나 for같은 제어문  
> {# ... #} : 주석  
Jinja의 자세한 문법참조 https://jinja.palletsprojects.com/en/2.10.x/   
