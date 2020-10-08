import re
import emoji
from bs4 import BeautifulSoup
from soynlp.normalizer import repeat_normalize

from typing import List

from LAC import LAC



lac = LAC(mode='lac', use_cuda=False)



class Transform(object):
    def __init__(self, 
                 tokenizer, 
                 args):

        self.args = args
        self.tokenizer = tokenizer
        
        # stopwords
#         with open(f'{args.tokenizer_path}/STOPWORDS.txt') as f:
#             self.STOPWORDS = [s.strip() for s in f.readlines()]
        
        # regular expression
        self.html = re.compile("<(\"[^\"]*\"|'[^']*'|[^'\">])*>")
        emojis = ''.join(emoji.UNICODE_EMOJI.keys())
        self.zh_pattern = re.compile(f'[^ .,?!/@$%~％·∼()。、，《 》“”：0-9a-zA-Z\u4e00-\u9fff{emojis}]+') # 기호, 영어, 중국어, 이모티콘
        self.url = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
        self.email = re.compile('([0-9a-zA-Z_]|[^\s^\w])+(@)[a-zA-Z]+.[a-zA-Z)]+')
        
        self.emo = emoji.get_emoji_regexp()
        self.image = re.compile(r'(\[image#0\d\])')
        self.hashtag = re.compile(r'#(\w+)')
        
    def _strpreprocess(self, string):
        """모델링용 텍스트 전처리 (중국어 키워드 추출에 적합하게 변경 필요함.)"""
        
        # compile basics
        
        url = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
        email = re.compile('([0-9a-zA-Z_]|[^\s^\w])+(@)[a-zA-Z]+.[a-zA-Z)]+')
        emojis = ''.join(emoji.UNICODE_EMOJI.keys())
        zh_pattern = re.compile(f'[^ .,?!/@$%~％·∼()。、，《 》“”：0-9a-zA-Z\u4e00-\u9fff{emojis}]+') # 기호, 영어, 중국어, 이모티콘

        # process
        if self.html.search(string) != None: # html js 처리
            soup = BeautifulSoup(string, "lxml")
            for script in soup(["script", "style"]):
                script.decompose()
            string = soup.get_text()
        string = string.strip()
        string = self.zh_pattern.sub(' ', string) # 숫자, 문자, whitespace, 이모지, 일반특수문자를 제외한 모든 유니코드 제거.
        string = re.sub('&nbsp;',' ', string) #&nbsp; 제거
        string = repeat_normalize(string, num_repeats=3) # repeats
        string = self.url.sub(' [URL] ', string) # url
        string = self.email.sub(' [EMAIL] ', string) # email
        # 요기에 보존리스트 추가하자.
        string = re.sub(r'\s+',' ', string) #white space character 변환 연속 하나로
        return string.strip()
        
    def _get_keywords(self, token_list: List[str]) -> List[str]:
        """
        step 1) stopwords 제외하기.
        step 2) pos == L part일 경우, Punctuation을 제외함.
        pos 관련 필터는 이 내부에 구현?
        """
        keywords = []
        for token, pos in zip(token_list, pos):
            if token in self.STOPWORDS:
                continue
            elif pos == 'L':
                """
                tokenizer에서 후처리로 하나의 토큰안에 문자 + 구둣점의 케이스를 분리함. 그러므로 full match.
                """
                # if re.fullmatch(rf'[{string.punctuation}]+',token) == None: # punctuation case의 경우.
                if token.strip(string.punctuation) == '':
                    continue
                else:
                    keywords.append(token)
            else:
                continue
                
        return keywords

    def _gen_ngrams(self, doc, n_gram=1):
        ngrams = zip(*[doc[i:] for i in range(n_gram)])
        return [" ".join(ngram) for ngram in ngrams]
    
    def keyword_test(self, doc):
        return 
    
    def transform(self, doc):
        pass

