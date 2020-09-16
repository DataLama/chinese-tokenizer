# Chinese Tokenizer
Simple Comparison of chinese word segmentation and pos tagger for text mining.

### 1) Chinese Word Segmentation comparison
The most basic feature of chinese tokenizer is word segmentation

**PKUSEG**
- CRF based model. (seg, pos)
- developed by peking university
- https://github.com/lancopku/pkuseg-python

**LAC**
- bi-gru + crf (seg, pos, ner)
- developed by baidu
- https://github.com/baidu/lac

**thulac**
- LR maximum entropy approach (seg, pos)
- developed by Tsinghua University
- model_3 needs contact 
- https://github.com/thunlp/THULAC-Python

**monpa**
- albert based tokenizer (seg, pos, ner)
- developed by monpa team
- https://github.com/monpa-team/monpa

**jiagu**
- simple perceptron (seg, pos, ner)
- developed by ownthink
- https://github.com/ownthink/Jiagu

**hanlp**
- albert-large based tokenizer (seg, pos, ner)
- developed by hankcs
- https://github.com/hankcs/HanLP

**[etc] deeplearning based SoTA model**
- https://github.com/SVAIGBA/TwASP
- https://github.com/ShannonAI/glyce


> hanlp, LAC is good to use.


### 2) Chinese KeyPhrase Extractor
- hanlp + pos
- lac + pos
- BERT-JointKPE