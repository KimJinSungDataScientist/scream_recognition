from flask import Flask, request
from haversine import haversine

app = Flask(__name__)

@app.route('/')
def root():
    safe=False # 이탈 했는지 Check

    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return 'No parameter'

    safe=False # 이탈 했는지 Check / 함수 불릴때마다 초기화
    
    

    my_location = list(map(lambda x : float(x), request.args['my_location'].split(',')))
    total_location = list(map(lambda x : [float(i) for i in x.split(',')], request.args['total_location'].split('/')))

    before_location = request.args['before_location'] # 내 이전 경로
    count = request.args['count'] # 제자리 얼마나 가만히 있는지 카운트(30 시작 -> 10초마다 -1)



    for i in total_location: # 모든 경로중에 30m 내에 없는 경우 
        # 오차범위 20m + 실제 이탈 10m
        if haversine(i, my_location, unit = 'm')<30:
            safe=True
    
    if int(count)<=0: # -> 제자리 300초 동안 있을경우
        return '제자리 5분 동안 위치중..',400

    if before_location != my_location: # 제자리 이탈 -> 정상 운행중
        if safe==False:
            return '경로이탈!',400
        else:
            return '안전 귀가중!',202
    ###################### 나누기 ##########################


    


if __name__ == '__main__':
    app.debug = True
    app.run()