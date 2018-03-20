
# coding: utf-8

# In[46]:


import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')


# In[47]:


df_main = pd.read_csv("../Team/saurabh_new.csv")
inverse_df_main = df_main


# In[48]:


df_main['arrival_time'] = pd.to_datetime(df_main['arrival_time'])
df_main['departure_time'] = pd.to_datetime(df_main['departure_time'])

inverse_df_main['arrival_time'] = pd.to_datetime(inverse_df_main['arrival_time'])
inverse_df_main['departure_time'] = pd.to_datetime(inverse_df_main['departure_time'])


# In[49]:


lb = LabelEncoder()


# In[50]:


df_main = df_main.drop(labels='feedback_msg',axis=1)
inverse_df_main = inverse_df_main.drop(labels='feedback_msg',axis=1)


# In[51]:


df_main['transit_via'] = lb.fit_transform(df_main['transit_via'])
# inverse_df_main['transit_via'] = lb.fit_transform(inverse_df_main['transit_via']) # dont uncomment this
# inverse_df_main


# # How monument visited depends upon the transport taken

# In[86]:


# how visiting monument is dependent upon the transport type taken
plt.figure(0)
a=sns.barplot(df_main['monument_id'],inverse_df_main['transit_via'])
a.figure.savefig("../Team/images/plots/admin/mon_vs_transit_1.png")
plt.figure(1)
b=sns.swarmplot(df_main['monument_id'],inverse_df_main['transit_via'])
b.figure.savefig("../Team/images/plots/admin/mon_vs_transit_2.png")
# plt.figure(2)
# sns.lmplot(df_main['monument_id'],inverse_df_main['transit_via'],df_main)


# In[102]:


# how transit_via and monument_id depends lineraly
plt.figure(3)
c= sns.regplot(df_main['monument_id'],df_main['transit_via'])
c.figure.savefig("../Team/images/plots/admin/mon_vs_transit_3.png")


# In[103]:


#these are point estimates of monument_id and transport taken
plt.figure(4)
d= sns.pointplot(x=df_main["monument_id"],y=inverse_df_main["transit_via"])
d.figure.savefig("../Team/images/plots/admin/mon_vs_transit_4.png")


# # How number of visits depends upon the average rating 

# In[104]:


plt.figure(5)
e= sns.barplot(df_main['total_no_of_visits'],df_main['average rating'],orient='h')
e.figure.savefig("../Team/images/plots/admin/visit_vs_avgrating_1.png")


# In[105]:


plt.figure(6)
f= sns.boxplot(df_main['total_no_of_visits'],df_main['average rating'],orient='h')
f.figure.savefig("../Team/images/plots/admin/visit_vs_avgrating_2.png")


# In[106]:


plt.figure(7)
g= sns.swarmplot(df_main['total_no_of_visits'],df_main['average rating'],orient='h')
g.figure.savefig("../Team/images/plots/admin/visit_vs_avgrating_3.png")


# In[107]:


# reg point
plt.figure(8)
h = sns.regplot(df_main['total_no_of_visits'],df_main['average rating'])
h.figure.savefig("../Team/images/plots/admin/visit_vs_avgrating_4.png")


# In[108]:


plt.figure(9)
i = sns.pointplot(df_main['total_no_of_visits'],df_main['average rating'],orient='h')
i.figure.savefig("../Team/images/plots/admin/visit_vs_avgrating_5.png")


# In[63]:


import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier


# In[64]:


encoded_df = pd.read_csv("../Team/saurabh_new.csv")
for cols in encoded_df.columns:
    encoded_df[cols] = lb.fit_transform(encoded_df[cols])


# In[65]:


Y = encoded_df.iloc[:,-2] # total no of visits
X = encoded_df.iloc[:,df_main.columns != 'total_no_of_visits']


# In[66]:


split = int(0.8*X.shape[0])
X_train = X[:split]
Y_train = Y[:split]

X_test = X[split:]
Y_test = Y[split:]


# In[67]:


rc= RandomForestClassifier()


# In[68]:


rc.fit(X_train,Y_train)


# In[69]:


predicted = rc.predict(X_test)


# In[70]:


rc.score(X_train,Y_train)


# In[77]:


acc = rc.score(X_train,Y_train)
print("Today accuracy is "+str(int(acc*100))+' percent')


# In[109]:


plt.figure(10)
plt.plot(np.asarray(predicted),'r--')
plt.plot(np.asarray(Y_test),'bo-')
plt.ylabel("footfall")
plt.xlabel("frequency of testing points")
plt.title("predicted footfall")
plt.savefig("../Team/images/plots/admin/footfall_prediction.png")


# In[80]:


# Average rating of monument(plot)
# sns.matrix(df_main['average rating'],df_main['monument_id'])


# In[99]:


clustermp = sns.clustermap(encoded_df)
clustermp.savefig("../Team/images/plots/admin/clustermp.png")


# # Sentiment Analysis Of Feedback Message

# In[82]:


df_with_feedback = pd.read_csv("../Team/saurabh_new.csv")


# In[83]:


from textblob import TextBlob
import re

def cleanfeedback(feedback):
    return (' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", feedback).split()))

def analyse_sentiment(feedback):
    analysis = TextBlob(cleanfeedback(feedback))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity ==0:
        return 0
    else:
        return -1
    
df_with_feedback['SA'] = np.array([analyse_sentiment(feedback) for feedback in df_with_feedback['feedback_msg']])



# In[84]:


pos_feedback = [feedback for index, feedback in enumerate(df_with_feedback['feedback_msg']) if df_with_feedback['SA'][index]>0]
neg_feedback = [feedback for index, feedback in enumerate(df_with_feedback['feedback_msg']) if df_with_feedback['SA'][index]<0]
neutral_feedback = [feedback for index, feedback in enumerate(df_with_feedback['feedback_msg']) if df_with_feedback['SA'][index]==0]


# In[85]:


print("Percentage of positive feedback:{}%".format(len(pos_feedback)*100/len(df_with_feedback['feedback_msg'])))
print("Percentage of negative feedback:{}%".format(len(neg_feedback)*100/len(df_with_feedback['feedback_msg'])))
print("Percentage of neutral feedback:{}%".format(len(neutral_feedback)*100/len(df_with_feedback['feedback_msg'])))


# In[101]:


# some complex graphs
g = sns.PairGrid(df_main)
g = g.map(plt.scatter)
g.savefig("../Team/images/plots/admin/pairgrid.png")


# In[100]:


# some complex graphs
pai = sns.pairplot(inverse_df_main)
pai.savefig("../Team/images/plots/admin/pairplot.png")

