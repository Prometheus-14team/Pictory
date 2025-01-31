from konlpy.tag import Okt

sentence = "오늘은 아침에 일어나자마자 창밖 날씨가 눈에 들어왔다. 커피 한 잔 마시면서 멍하니 창밖을 바라봤다. 오전엔 회의가 있었고, 다들 무슨 말을 그렇게 많이 하는지 정신이 없었다. 점심엔 간단하게 샌드위치 먹었는데 생각보다 맛있어서 기분이 좀 나아졌다. 오후에는 프로젝트 때문에 자료를 정리하느라 시간이 훌쩍 지나갔고, 퇴근 후엔 집으로 돌아와 따뜻한 차 한 잔 하며 하루를 마무리했다. 오늘 하루도 그냥 그렇게 흘러갔다."

def stemmer(sentence):
    okt = Okt()  
    nouns = okt.nouns(sentence)  
    return nouns
