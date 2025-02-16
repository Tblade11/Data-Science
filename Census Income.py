'''
This project is to predict if someone makes over $50k based on
data collected from the Census Bureau in 1994.
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

'''
Column definitions
Age- how old they are
workclass-working class definition; self-employed,never worked,fed,state etc.
education-bachelor,masters,voc etc
education-num = year of education
marital status-married armed forces,married civilian, single,single w/ kid(s)etc
occupation-workforce category
relationship-husband, wife,single w/ kid(s),single etc.
race-ethnicity
sex-gender
capital gain-profit
capital loss- loss in wages, income etc
hours per week-hours worked per week
native country-country origin
income=making more or less than 50k/yr
'''

#loading csv file and cleaning data
census_df = pd.read_csv('C:/Users/Skits/Documents/Data Science Cert/income.csv')

census_df.head()

census_df.dropna()#remove empty rows

census_df.dtypes

census_df.info()

census_df.isnull().sum()#output sum of empty cells in dataset per column

census_df = census_df.dropna(how='any',axis=0)#remove null in columns

census_df.isnull().sum()

census_df.info()

'''convert column data type to integer
df['points'] = df['points'].astype(int64)
'''
census_df['age'] = census_df['age'].astype("int64")
census_df['fnlwgt'] = census_df['fnlwgt'].astype("int64")
census_df['education.num'] = census_df['education.num'].astype("int64")
census_df['capital.gain'] = census_df['capital.gain'].astype("int64")
census_df['capital.loss'] = census_df['capital.loss'].astype("int64")
census_df['hours_per_week'] = census_df['hours_per_week'].astype("int64")

census_df.info()

#remove rows in dataset where a cell = '?'
census_df.drop(census_df[census_df['Native_country'] == ' ?'].index,inplace=True)
census_df.drop(census_df[census_df['occupation'] == ' ?'].index,inplace=True)
census_df.drop(census_df[census_df['workclass'] == ' ?'].index,inplace=True)

#find correlation amongst categories
census_df.corr()

#capital gain,capital loss are not necessary for this report
#both education columns are redudant so one needs to be removed
#remove these columns
census_df.drop(census_df.columns[[3,10,11]],axis=1)
census_df.head()

# Plotting histogram for age vs distribution of population
plt.figure(figsize=(15,4))
plt.hist(census_df['age'],bins=10,histtype='bar',color='red',density=True,rwidth=0.9)
plt.xlabel('Age')
plt.ylabel('Percent of Total People')
plt.show()

#Majority of pop in dataset is less than 50yr old

#Box & Whiskers plot Nationality based with race and edu. and omit the outliers
sns.boxplot(x='race',y='education.num',data=census_df)
plt.xticks(rotation=90)
#hue for subgroup and sym for no outliers
plt.show()

'''Higher Edu is higher for White and Asian Pacific Islander races
which means higher salaries'''

#Line Graph for relationship status vs age based on income

sns.set(font_scale=1.5)
sns.catplot(x="relationship", y="age",
			data=census_df,
            kind="point",hue='Income',
            capsize=0.4,ci=None,aspect=2)
plt.xticks(rotation=90)
plt.show()

'''This graph depicts if you start a family 
around the age of 25, you can expect to have lower income
than people who start a family later in life'''

#Distribution of income to working hours based on relationship status

sns.set(font_scale=1)
sns.relplot(x="education.num", y="hours_per_week", 
            data=census_df, kind="line",row='Income' ,
            ci=None,
            hue="relationship",
            style="relationship",markers=True,dashes=False,aspect=2)
plt.xticks(rotation=90)
plt.show()

'''These graphs shows that even with low education
people are still earning more than 50k
but we also see that people that are single work more hours
if they make more than 50k'''

#distribution of hours per week vs occupation amongst men and women

men1 = census_df[(census_df['Income'] == ' >50K') & (census_df['sex']==" Male")]
wmen1 = census_df[(census_df['Income'] == ' >50K') & (census_df['sex']==" Female")]
print("Average hours per week for Women",wmen1['hours_per_week'].mean())
print("Average hours per week for Men",men1['hours_per_week'].mean())
#avg hours per week for Men and Women who make more than 50k

men2 = census_df[(census_df['Income'] == ' >50K') & (census_df['hours_per_week']<=40)&(census_df['sex']==" Male")]
wmen2 = census_df[(census_df['Income'] == ' >50K') & (census_df['hours_per_week']<=40)&(census_df['sex']==" Female")]
#Men and women who makes more than 50k but work less than 40 hours/wk

#occupation count
b1=men2['occupation'].value_counts(normalize=True)
b2=wmen2['occupation'].value_counts(normalize=True)

#plotting comparisons

fig, axes = plt.subplots(1, 2)
p1=b1.plot(kind='barh',ax=axes[0],color='g',figsize=(22, 5),alpha=0.7,title=("Men "))
p2=b2.plot(kind='barh',ax=axes[1],color='r',figsize=(22, 5),alpha=0.7,title=("Women "))

axes[0].tick_params(labelsize=15)
axes[1].tick_params(labelsize=15)

plt.show()


