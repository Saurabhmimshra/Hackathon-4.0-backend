
# coding: utf-8

# In[27]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# In[28]:


df = pd.read_csv("../Team/final_funding_in_csv.csv",error_bad_lines=False)
df.head()


# In[31]:


df = df.fillna(value=0)


# In[52]:




X = df.iloc[:,1:-2]
Y = df.iloc[:,df.columns=='2017-18']
X


# In[45]:


split = int(0.8*X.shape[0])

X_train = X[:split]
Y_train = Y[:split]

X_test = X[split:]
Y_test = Y[split:]


# In[46]:


from sklearn.ensemble import RandomForestClassifier


# In[47]:


rfc = RandomForestClassifier()


# In[48]:


rfc.fit(X_train,Y_train)


# In[49]:


rfc.score(X_test,Y_test)


# In[50]:


predic = rfc.predict(X_test)


# In[51]:


predic


# In[64]:


plt.plot(np.array(predic),'bo-')
plt.plot(np.array(Y_test),'r--')
plt.ylabel("Amount in rupees")
plt.xlabel("Frequency of testing points")
plt.title("Prediction of funds you should apply")
plt.savefig("../Team/images/plots/admin/predict.png")
acc = rfc.score(X_test,Y_test)
print("The current accuracy of the model is "+ str(acc*100) + " percent")

