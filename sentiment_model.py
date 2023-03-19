from pullDataFromMongoDB import listDict, tb # ดึงเทเบิ้ลและข้อมูลทวิตทั้งหมดที่ออยู่ใน mongo
from textblob import TextBlob # import for use sentiment analysis 
import pandas as pd # import data frame เพื่อให้ง่ายต่อการเอาข้อมูลมาวิเคราะห์กับ python
from wordcloud import WordCloud
import matplotlib.pyplot as plt # ใช้สำหรับการพล็อตกราฟ

# สร้าง data frame โดยการเรียกข้อมูลที่เราดึงจากดาต้าเบสมาเก็บไว้ และให้ชื่อคอลัมว่า tweet
df = pd.DataFrame( [x for x in listDict] , columns= ['tweet']) 

# หาค่า Subjectivity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

# หาค่า Polarity เพื่อเอาไปวิเคราะห์แง่ความรู้สึกต่อ
def getPolarity(text):
    return TextBlob(text).sentiment.polarity

# เพิ่มช่องข้อมูลของ Subjectivity กับ Polarity ลงในดาต้าเฟรม
df['subjectivity'] = df['tweet'].apply(getSubjectivity)
df['polarity'] = df['tweet'].apply(getPolarity)

# วิเคราะห์ความรู้สึก จากค่า polarity ที่ได้จากการดึง text blob มาช่วยวิเคราะห์
def analysis(score):
    if score < 0:
        return 'neg'
    elif score == 0:
        return 'neu'
    else:
        return 'pos'

# เพิ่มช่องข้อมูลของการวิเคราะห์ความรู้สึกลงในดาต้าเฟรม
df['analysis'] = df['polarity'].apply(analysis)
print(df)

# เคลียร์ดาต้าเบสเพื่อรอรับข้อมูลครั้งใหม่
tb.delete_many({})
print('clearDB OK')

# gen all wordcloud in tag
# สร้างwordcloudจากข้อมูลทั้งหมด โดยสร้างตามความถี่ของข้อมูล
def genAllwordcloud():
    words = ' '.join( [ text for text in df['tweet']] ) # เอาคำทุกคำในมาต่อกัน
    genWordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=119).generate(words) #gen wordcould
    plt.imshow(genWordCloud, interpolation="bilinear")
    plt.axis('off')
    plt.title('Generate WordCloud')

    plt.savefig('static/img/01_genAllwordcloud.png') # save img
    # plt.show() # show


# gen positive wordcould
# สร้างwordcloudจากข้อมูลที่ผ่านการวิเคราะห์แล้วว่าเป็นด้านบวก
def genPOSwordcloud():
    df_pos = df[df['analysis'] == 'pos'] # สร้างดาต้าเฟรมใหม่สำหรับทวีตที่วิเคราะห์มาว่าเป็นความรู้สึกด้านบวก
    pos_words = ' '.join( [text for text in df_pos['tweet']] )  # เอาคำทุกคำในทวีตหมวดด้านบวกมาต่อกัน
    gen = WordCloud(width=500, height=300, random_state=21, max_font_size=119).generate(pos_words) #gen wordcould
    plt.imshow(gen, interpolation="bilinear")
    plt.axis('off')
    plt.title('Positive WordCloud')
    
    plt.savefig('static/img/02_genPOSwordcloud.png') # save img
    # plt.show() # show


# สร้างwordcloudจากข้อมูลที่ผ่านการวิเคราะห์แล้วว่าเป็นด้านลบ
def genNEGwordcloud():
    df_neg = df[df['analysis'] == 'neg'] #สร้างดาต้าเฟรมใหม่สำหรับทวีตที่วิเคราะห์มาว่าเป็นความรู้สึกด้านลบ
    neg_words = ' '.join( [text for text in df_neg['tweet']] )  #เอาคำทุกคำในทวีตหมวดด้านลบมาต่อกัน
    gen = WordCloud(width=500, height=300, random_state=21, max_font_size=119).generate(neg_words) #gen wordcould
    plt.imshow(gen, interpolation="bilinear")
    plt.axis('off')
    plt.title('Negative WordCloud')
    
    plt.savefig('static/img/03_genNEGwordcloud.png') # save img
    # plt.show() # show


# สร้างwordcloudจากข้อมูลที่ผ่านการวิเคราะห์แล้วว่าเป็นด้านเฉยๆ
def genNEUwordcloud():
    df_neu = df[df['analysis'] == 'neu'] # สร้างดาต้าเฟรมใหม่สำหรับทวีตที่วิเคราะห์มาว่าเป็นความรู้สึกเฉยๆ
    neu_words = ' '.join( [text for text in df_neu['tweet']] ) # เอาคำทุกคำในทวีตหมวดเฉยๆมาต่อกัน
    gen = WordCloud(width=500, height=300, random_state=21, max_font_size=119).generate(neu_words) #gen wordcould
    plt.imshow(gen, interpolation="bilinear")
    plt.axis('off')
    plt.title('Neutral WordCloud')
    
    plt.savefig('static/img/04_genNEUwordcloud.png') # save img
    # plt.show() # show
    
genNEUwordcloud()  # เรียกใช้ wordcloud ด้านเฉยๆ
genNEGwordcloud()  # เรียกใช้ wordcloud ด้านลบ
genPOSwordcloud()  # เรียกใช้ wordcloud ด้านบวก
genAllwordcloud()  # เรียกใช้ wordcloud แบบไม่แบ่งแยก