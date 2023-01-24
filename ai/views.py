from django.shortcuts import render, redirect

import logging
from django.conf import settings
from django.core.files.storage import default_storage
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import numpy as np
from tqdm import tqdm, tqdm_notebook
#kobert
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model
import pandas as pd
import pandas as pd
from .models import Place


# from pybo.model import Result
from .models import Result
from .models import AiModel
bertmodel, vocab = get_pytorch_kobert_model()
tokenizer = get_tokenizer()
tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)

class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len,
                 pad, pair):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)

        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))

    def __len__(self):
        return (len(self.labels))
def predict(predict_sentence):

    data = [predict_sentence, '0']
    dataset_another = [data]

    another_test = BERTDataset(dataset_another, 0, 1, tok, 64, True, False)
    test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=2, num_workers=0)
    model = BERTClassifier(bertmodel,  dr_rate=0.5)
    model_path = AiModel.objects.get(pk=1).ai_file.path
    model.load_state_dict(torch.load(model_path,map_location=torch.device('cpu')))
    model.eval()

    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
        token_ids = token_ids.long().to('cpu')
        segment_ids = segment_ids.long().to('cpu')

        valid_length= valid_length
        label = label.long().to('cpu')
        
        out = model(token_ids, valid_length, segment_ids)
    
    return out
class BERTClassifier(nn.Module):
    def __init__(self,
                 bert,
                 hidden_size = 768,
                 num_classes=771,   ##클래스 수 조정##
                 dr_rate=None,
                 params=None):
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate
                 
        self.classifier = nn.Linear(hidden_size , num_classes)
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)
    
    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()

    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)
        
        _, pooler = self.bert(input_ids = token_ids, token_type_ids = segment_ids.long(), attention_mask = attention_mask.float().to(token_ids.device),return_dict=False)
        if self.dr_rate:
            out = self.dropout(pooler)
        return self.classifier(out)

def result(request):
             
    result = Result()
    
    text = request.POST.get('input_text',None)
    result.input = text
    pred = predict(text)
    pred = pred.detach().cpu().numpy()
    top5 =sorted(pred[0], reverse = True)[:5]
    top10 =sorted(pred[0], reverse = True)[:10]
    df = pd.read_csv('label/label_lst_3.csv')
    lst = df['name']
    idx = [] # top5 index 찾기
    for i in top5:
        idx.append(np.where(pred == i)[1][0])

    result_lst = [] # top5 index로 가게 이름 찾기
    for i in idx:
        result_lst.append(lst[i])
    
    result.result = result_lst
    result.save()


    num_lst = [round((2**i)*(i/sum(top5)),2) for i in top5]
    visual_df = pd.DataFrame(columns = ['추천 결과', '추천 수치'])
    visual_df['추천 결과'] = result_lst
    visual_df['추천 수치'] = num_lst

    context = {
        'result': result,
        'result_lst':result_lst,
        'chart_percent' : num_lst
        }
    
    return render(request, 'result.html', context)

def info(request):
    info = request.POST.get('result_info',None) 
    place = Place.  objects.get(place_name = info)
    address = place.place_address
    latitude = place.place_latitude
    longitude = place.place_longitude
    phone = place.place_phone
    context = {
        'info' : info,
        'address': address,
        'latitude': latitude,
        'longitude': longitude,
        'phone' : phone,
    }
    return render(request,'info.html',context)

def db_upload(request):
    df = pd.read_csv("./db_221231_je.csv") 
    
    for i in range(df.shape[0]):
        db =  Place()
        db.place_name = df.iloc[i]['명칭']
        db.place_address = df.iloc[i]['주소']
        db.place_latitude = df.iloc[i]['위도']
        db.place_longitude = df.iloc[i]['경도']
        db.place_phone = df.iloc[i]['문의 및 안내']
        db.save()
    
    return render(request,'db_upload.html')