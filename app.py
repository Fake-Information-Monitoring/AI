import jieba
from numpy.core.multiarray import ndarray
from sanic import Sanic
from sanic.response import json as sanicJson
from sklearn.preprocessing import PolynomialFeatures

from DFA import getFilter
from config import *
from loadingData import wash_sentence
from loadingModel import load, save

app = Sanic("FakeNews")
poly = PolynomialFeatures(degree=40)


@app.post("/VerifyRumor")
async def verifyRumor(request):
    try:
        text: str = request.form['text'][0]
        if text is None:
            return sanicJson({
                "code": 401,
                "success": False,
                "data": "表单为空！"
            })
        test = [wash_sentence(text), ]
        test = rumor_tfidf.transform(test)
        score: ndarray = rumor_model.predict_proba(test)
        data = {}
        for i in range(0, 2):
            data[result[i]] = score[0][i]
        return sanicJson({
            "code": 200,
            "success": True,
            "data": data
        })
    except Exception as e:
        return sanicJson({
            "code": 500,
            "success": False,
            "data": str(e)
        })


@app.post("/VerifyOtherWords")
async def verifyOtherNews(request):
    try:
        text: str = request.form['text'][0]
        if len(text) < 1:
            return sanicJson({
                "code": 401,
                "success": False,
                "msg": "表单为空！"
            })
        data = {}
        for model in models:
            text, words = model.filter(text)
            data[result_[model.type]] = words
        return sanicJson({
            "code": 200,
            "success": True,
            "data": {
                "text": text,
                "result": data
            }
        })
    except Exception as e:
        return sanicJson({
            "code": 500,
            "success": False,
            "data": str(e)
        })


if __name__ == '__main__':
    rumor_model = load("./models/rum_model.pkl")
    rumor_tfidf = load('./models/rum_tfidf.pkl')
    models = []
    for key, value in path_list.items():
        models.append(getFilter(value, key))
    for model in models:
        save(model, "./models/"+result_[model.type] + ".pkl")
    # for i in result_.values():
    #     model = load("./models/" + i + ".pkl")
    #     models.append(model)
    app.run(host="127.0.0.1", port=4336, debug=True)
