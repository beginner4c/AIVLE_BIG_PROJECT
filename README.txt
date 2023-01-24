**가상환경 만들고 라이브러리 설치하기**
** KOBERT 사용하기 위해 필수**
1.
Anaconda Prompt 실행
conda create -n py37 python=3.7
conda activate py37

2.
vscode F1 눌러서 select Interpreter 검색
py37 선택

3.
vscode의 작업 폴더 cmd창 열기 -> interpreter 변경 후 터미널 닫고 새로 열기!!
pip install numpy==1.16.6
pip install pandas==1.2.1
pip install mxnet==1.7.0.post2
pip install gluonnlp==0.6.0
pip install torch==1.10.1
pip install pandas tqdm
pip install sentencepiece==0.1.96
pip install transformers==3.0.2
pip install onnxruntime==1.8.0
pip install boto3==1.15.18

4. 
코버트 폴더 다운로드
git clone https://github.com/SKTBrain/KoBERT.git

5.
다운받은 코버트 폴더 내 requirement.txt 아래처럼 변경
----------------------------------------------------------------
boto3 ==1.15.18
gluonnlp == 0.6.0
mxnet == 1.7.0.post2
onnxruntime == 1.8.0
sentencepiece == 0.1.96
torch == 1.10.1
transformers == 3.0.2
----------------------------------------------------------------

6.
cd KoBERT (코버트 다운받은 경로로 이동)
pip install -r requirements.txt
pip install .


- return_dict 오류: 
vscode 열려있는 폴더 한글 지우기
C:\Users\anaconda3\envs\가상환경명\lib\site-packages\kobert\pytorch_kobert.py
위의 파일에서 27번줄 return_dict=False 지우기

- 여기서부턴 순서대로 설치
pip install git+https://github.com/huggingface/transformers
pip install gluonnlp==0.8.0
pip install transformers==4.15.0
pip install git+https://github.com/MikeHibbert/arweave-python-client.git
pip install transformers==4.10.0
pip install tensorflow==2.7.0 

!!!
빨간 글씨로 ERROR: pip dependency ~ 오류나면서
kobert require ~ 어쩌구 여러줄 떠도 무시하고 쭉 설치하기!!!




===================================================

JAVA HOME 오류나면 

1.
https://www.oracle.com/java/technologies/downloads/#jdk19-windows
위 링크로 이동해서
x64 Compressed Archive 혹은 x64 Installer 설치 

2.
https://clsrn4561.tistory.com/1 참고해서 환경변수 수정하기

3.
py파일에 아래 코드 넣기
import os
os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-19' #여기서 본인의 jdk 경로
print('JAVA_HOME' in os.environ)