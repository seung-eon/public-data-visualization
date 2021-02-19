#!/usr/bin/env python
# coding: utf-8

# ## 전통시장 위치와 편의시설

# In[2]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[3]:


# 한글, -(마이너스) 깨짐 없이 보기
plt.rc("font", family="Malgun Gothic")
plt.rc("axes", unicode_minus=False)


# In[4]:


# 폰트가 선명하게 보이도록 설정
from IPython.display import set_matplotlib_formats

set_matplotlib_formats("retina")


# In[5]:


# 확인
pd.Series([-1, 0, 1, 3, 5]).plot(title="한글폰트")


# In[6]:


# 위경도 포함된 데이터 불러오기
df1 = pd.read_csv("data/서울시 전통시장 현황.csv", encoding='CP949')
df1.shape


# In[7]:


df1.head(1)


# In[8]:


df1.isnull().sum()


# In[9]:


df1.info()


# In[12]:


# df 1 컬럼 정리
columns1 = ['자치구명', '전통시장명', '주소명', '경도', '위도']

df1 = df1[columns1].copy()
df1.shape


# In[13]:


df1.info()


# In[14]:


# 컬럼 이름 변경
df1.columns = ['구', '시장명', '주소명', '경도', '위도']
df1.head()


# In[16]:


# 시장 이름에 '시장'이 들어가는 데이터만 보기

df_market = df1["시장명"].str.contains("시장").copy()
df_market.value_counts()


# In[18]:


# 시장 이름에 '시장'이 들어가는 데이터만 추출

df_mk = df1.loc[df1["시장명"].str.contains("시장")].copy()
df_mk.head(10)


# In[19]:


# 구별 시장 수 막대그래프

plt.figure(figsize=(15, 4))
sns.countplot(data=df_mk, x="구")


# In[20]:


df_mk[["위도", "경도"]].plot.scatter(x="경도", y="위도")


# In[21]:


sns.scatterplot(data=df_mk, x="경도", y="위도", hue="구")

# 레전드값 옆으로
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# In[22]:


# 편의시설 데이터 불러오기
df2 = pd.read_csv('data/전통시장현황_20200226..csv', encoding='CP949')
df2.shape


# In[23]:


df2.info()


# In[24]:


# 컬럼 보기
df2.columns


# In[25]:


# 결측치 보기
df2.isnull().sum().plot.barh(figsize=(10,25))


# In[34]:


# 주력 상품 결측치 보기

df2["시장/상점가의 주력 상품의 상품명"].isnull().value_counts()


# In[51]:


# 사용할 컬럼만 지정
columns2 = ['시장명','시군구','시도', '보유갯수 - 16시장전용 고객주차장',
           '시장/상점가의 주력 상품 여부(1=있음, 2=없음)','보유현황 - 10쇼핑카트(1=있음, 2=없음)',
           '시장/상점가의 주력 상품의 상품명']


# In[52]:


# 컬럼 줄어든 것 확인
df2 = df2[columns2].copy()
df2.shape


# In[28]:


# 메모리 줄어든 것 확인
df2.info()


# In[29]:


# 시도가 서울인 것만 사용

df_seoul = df2[df2["시도"] == "서울"].copy()
df_seoul.shape


# In[30]:


# 시장명에 '시장'이 들어가는 것만

df_seoul = df_seoul[df_seoul["시장명"].str.contains("시장")]
df_seoul


# In[32]:


df_seoul[df_seoul["시장명"]=="강남시장"]


# In[35]:


df_mk[df_mk["시장명"]=="강남시장"]


# In[54]:


# 두 데이터 프레임을 '시장명'을 기준으로 합치기

# 병합할 컬럼의 이름이 '시장명'으로 같으므로 
# left_on='시장명', right_on='시장명' 옵션은 생략

df = pd.merge(df_mk, df_seoul).copy()
df.shape


# In[40]:


# 두 데이터의 차집합 보기
set(df_mk['시장명'].unique()) - set(df_seoul['시장명'].unique())


# In[41]:


# 두 데이터의 차집합 보기
set(df_seoul['시장명'].unique()) - set(df_mk['시장명'].unique()) 


# In[56]:


df["시장/상점가의 주력 상품의 상품명"].isnull().value_counts()


# In[59]:


df


# In[57]:


import folium


# In[58]:


long = df["경도"].mean()
lat = df["위도"].mean()


# In[62]:


m = folium.Map([lat,long], zoom_start=12)

for i in df.index:
    sub_lat = df.loc[i, "위도"]
    sub_long = df.loc[i, "경도"]
    title = f'{df.loc[i, "시장명"]} ({df.loc[i, "주소명"]})'
    info =  f'{df.loc[i, "시장명"]} (주력 상품: {df.loc[i, "시장/상점가의 주력 상품의 상품명"]})'
    
    icon_color = "red"
    
    folium.Marker([sub_lat, sub_long],
                  icon=folium.Icon(color=icon_color),
                  tooltip=title,
                  popup=f'<i>{info}</i>').add_to(m)

# for문 끝나고 지도 출력
m


# In[65]:


# 다른 스타일
m = folium.Map(location=[lat, long], zoom_start=12, tiles="Stamen Toner")

for i in df.index[:100]:
    tooltip = f'{df.loc[i, "시장명"]} ({df.loc[i, "시장/상점가의 주력 상품의 상품명"]})'
    lat = df.loc[i, "위도"]
    long = df.loc[i, "경도"]

    folium.CircleMarker([lat, long], tooltip=tooltip, radius=3).add_to(m)
    
m


# In[78]:


# 겹친 아이콘 처리
from folium.plugins import MarkerCluster

# icon=folium.Icon(color=icon_color) 로 아이콘 컬러를 변경가능

m = folium.Map([lat,long], zoom_start=12)
marker_cluster = MarkerCluster().add_to(m)

for i in df.index:
    sub_lat = df.loc[i, "위도"]
    sub_long = df.loc[i, "경도"]
    title = f'{df.loc[i, "시장명"]} ({df.loc[i, "주소명"]})'
    info =  f'{df.loc[i, "시장명"]} (주력 상품: {df.loc[i, "시장/상점가의 주력 상품의 상품명"]}, 고객주차장 개수 : {df.loc[i, "보유갯수 - 16시장전용 고객주차장"]}, 쇼핑카트 유무(1=있음, 2=없음) : {df.loc[i, "보유현황 - 10쇼핑카트(1=있음, 2=없음)"]})'
    popup = folium.Popup(f'<i>{info}</i>', max_width=600, max_height=600)
    icon_color = "red"
    
    folium.Marker([sub_lat, sub_long],
                  icon=folium.Icon(color=icon_color),
                  popup=popup, 
                  tooltip=title).add_to(marker_cluster)

m


# In[79]:


# html로 저장

m.save('서울시 전통시장 위치와 편의시설 정보.html')

