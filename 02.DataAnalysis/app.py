from flask import Flask, render_template, session, escape, url_for, flash, redirect, request
from fbprophet import Prophet
from datetime import datetime, timedelta
from my_util.weather import get_weather
from my_util.forms import RegistrationForm
import os
import pandas as pd
import pandas_datareader as pdr
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rc('font', family='Malgun Gothic')
mpl.rc('axes', unicode_minus=False)

app = Flask(__name__)
app.secret_key = 'qwert12345'
nasdaq_dict, kospi_dict, kosdaq_dict = {}, {}, {}  # 기업리스트가 자주바뀌지않으니, 전역변수로만들어놓기


def get_weather_main():
    weather = None
    try:
        weather = session['weather']
    except:
        app.logger.debug("get new weather info")
        weather = get_weather()
        session['weather'] = weather
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=60)
    return weather


@app.before_first_request  # 최초 한번만 실행하는 방식(플라스크는 이런식)
def before_first_request():
    nasdaq = pd.read_csv('./static/data/NASDAQ.csv', dtype={'Symbol': str})
    for i in nasdaq.index:
        nasdaq_dict[nasdaq['Symbol'][i]] = nasdaq['Name'][i]
    kospi = pd.read_csv('./static/data/KOSPI.csv', dtype={'종목코드': str})
    for i in kospi.index:
        kospi_dict[kospi['종목코드'][i]] = kospi['기업명'][i]
    kosdaq = pd.read_csv('./static/data/KOSDAQ.csv', dtype={'종목코드': str})
    for i in kosdaq.index:
        kosdaq_dict[kosdaq['종목코드'][i]] = kosdaq['기업명'][i]


@app.route('/')
def index():
    menu = {'ho': 1, 'da': 0, 'ml': 0, 'se': 0,
            'co': 0, 'cg': 0, 'cr': 0, 'st': 0, 'wc': 0, 're': 0}
    return render_template('09.main.html', menu=menu, weather=get_weather_main())


@app.route('/park')
def park():
    menu = {'ho': 0, 'da': 1, 'ml': 0, 'se': 1,
            'co': 0, 'cg': 0, 'cr': 0, 'st': 0, 'wc': 0, 're': 0}
    return render_template('11.park.html', menu=menu, weather=get_weather_main())


@app.route('/stock', methods=['GET', 'POST'])
def stock():
    menu = {'ho': 0, 'da': 0, 'ml': 1, 'se': 0, 'co': 0,
            'cg': 0, 'cr': 0, 'st': 1, 'wc': 0, 're': 0}
    if request.method == 'GET':
        return render_template('10.stock.html', menu=menu, weather=get_weather_main(),
                               nasdaq=nasdaq_dict, kospi=kospi_dict, kosdaq=kosdaq_dict)
    else:
        market = request.form['market']
        if market == 'KS':
            code = request.form['kospi_code']
            company = kospi_dict[code]
            code += '.KS'
        elif market == 'KQ':
            code = request.form['kosdaq_code']
            company = kosdaq_dict[code]
            code += '.KQ'
        else:
            code = request.form['nasdaq_code']
            company = nasdaq_dict[code]
        learn_period = int(request.form['learn'])
        pred_period = int(request.form['pred'])  # 클라이언트에게 입력받고
        today = datetime.now()  # 기준이 될 오늘날짜 받고
        start_learn = today - timedelta(days=learn_period*365)  # 기간 정리해서
        end_learn = today - timedelta(days=1)

        stock_data = pdr.DataReader(
            code, data_source='yahoo', start=start_learn, end=end_learn)  # 야후주식으로부터 실데이터가져오기
        app.logger.debug(f"get stock data: {code}")  # 터미널에서 확인가능한 개발자확인용
        # model에 적용시키려는 작업(눈으로 확인하려면 주피터노트북에서)
        df = pd.DataFrame({'ds': stock_data.index, 'y': stock_data.Close})
        df.reset_index(inplace=True)
        del df['Date']

        model = Prophet(daily_seasonality=True)  # 학습모델prophet에 적용시키고
        model.fit(df)
        future = model.make_future_dataframe(
            periods=pred_period)  # 사용자가 입력한 기간까지 예측한다
        forecast = model.predict(future)

        fig = model.plot(forecast)  # 그래프그리기
        img_file = os.path.join(
            app.root_path, 'static/img/stock.png')  # 지정한위치에 지정한파일명으로 저장해라
        fig.savefig(img_file)  # 클라이언트에게 보여주기 위해 파일저장
        mtime = int(os.stat(img_file).st_mtime)  # 이미지저장 즉각반영

        fig = model.plot_components(forecast)  # 시즌분석그래프그리기
        img_file = os.path.join(
            app.root_path, 'static/img/stock_plt.png')
        fig.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        return render_template('10.stock_res.html', menu=menu, weather=get_weather_main(), mtime=mtime, company=company, code=code)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    menu = {'ho': 0, 'da': 0, 'ml': 0, 'se': 0, 'co': 0,
            'cg': 0, 'cr': 0, 'st': 0, 'wc': 0, 're': 1}
    if form.validate_on_submit():
        # 알람 카테고리에 따라 부트스트랩에서 다른 스타일을 적용 (success, danger)
        flash(f'{form.username.data} 님 가입 완료!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form, menu=menu, weather=get_weather_main())


if __name__ == '__main__':
    app.run(debug=True)
