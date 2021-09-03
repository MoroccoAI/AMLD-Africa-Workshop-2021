from bs4 import BeautifulSoup
import pandas as pd
import re
import nltk
nltk.download('stopwords')

def clean_data(data):
  cleaned_data = []

  # get the xml data
  Bs_data = BeautifulSoup(data, "xml")

  # Finding all instances of tag # `text`
  b_name = Bs_data.find_all('text')

  # Finding all instances of tag # `title`
  title_name = Bs_data.find_all('title')
  for i in range(0,len(b_name)):
    rows = [title_name[i].get_text(), b_name[i].get_text()]
    cleaned_data.append(rows)
  
  # construct the dataframe
  df = pd.DataFrame(cleaned_data,columns = ['title','text'], dtype = float)
  
  #Apply the first round of text cleaning techniques on column 'Text'
  df['text'] = df['text'].str.replace('\d+', ' ')
  df['text'] = df['text'].str.replace('\n', ' ')
  df['text'] = df['text'].str.replace('/', ' ')
  df['text'] = df['text'].str.replace("عيون لكلام", " ")
  df['text'] = df['text'].str.replace(":تصنيف", " ")
  df['text'] = df['text'].str.replace("تحويلات", " ")
  df['text'] = df['text'].str.replace("مقالات", " ")
  df['text'] = df['text'].str.replace("{{عيون}}", " ")
  df['text'] = df['text'].str.replace("زريعة", " ")
  df['text'] = df['text'].str.replace("ضبط مخازني", " ")
  df['text']= [re.sub(r'[^\w\s]','',c) for c in df['text']]
  df['text']= [re.sub(r'[a-zA-Z ]',' ',c) for c in df['text']]
  df['text']= df["text"].str.replace('\s+', ' ', regex=True)

  #Apply the second round of text cleaning techniques on column 'Text'
  df['text'] = df['text'].str.replace("تحويل", " ")
  df['text'] = df['text'].str.replace("تصنيف", " ")

  # We define some Darija specific Stopwords
  add_stpw=['ديال','اللي','ولا']
  arb_stopwords = list(set(nltk.corpus.stopwords.words("arabic")))+ add_stpw
  df['text'] = df['text'].apply(lambda x: ' '.join([word for word in x.split() if word not in (arb_stopwords)]))

  #We will remove Tifinagh Characters as our text contains those special characters
  tifinagh='ⴰ|ⴱ|ⴲ|ⴳ|ⴴ|ⴵ|ⴶ|ⴷ|ⴸ|ⴹ|ⴺ|ⴻ|ⴼ|ⴽ|ⴾ|ⴿ|ⵀ|ⵁ|ⵂ|ⵃ|ⵄ|ⵅ|ⵆ|ⵇ|ⵈ|ⵉ|ⵊ|ⵋ|ⵌ|ⵍ|ⵎ|ⵏ|ⵐ|ⵑ|ⵒ|ⵓ|ⵔ|ⵕ|ⵖ|ⵗ|ⵘ|ⵙ|ⵚ|ⵛ|ⵜ|ⵝ|ⵞ|ⵟ|ⵠ|ⵡ|ⵢ|ⵣ|ⵤ|ⵥ|ⵦ|ⵧ|ⵯ||⵰'
  df['text']= [re.sub(tifinagh,'',c) for c in df['text']]

  return df