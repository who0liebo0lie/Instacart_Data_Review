#!/usr/bin/env python
# coding: utf-8

# # Sprint 2 EDA Project 
# This project aims to demonstrate competency in uploading files into a dataframe and cleaning the dataframe (finding and removing duplicate values, find and remove missing values)
# Once the dataframes are cleaned the program will attempt to answer some questions regarding the uploaded data using graphics. 
# Data is from grocery deliver company, Instacart.  There are five seperate files.
# 
# 
# In "orders" file each row is one order from the app and columsn for 'order_id'(ID number that uniquely identifies each order), 
# 'user_id'(ID number that uniquely identifies each customer account)'order_number'(the number of times this customer has placed
# an order), 'order_dow' (day of the week that the order placed), 'order_hour_of_day' (hour of the day that the order was 
# placed), 'days_since_prior_order'(number of days since this customer placed their previous order). 
# 
# In 'products' file each row corresponds to a unique product that customers can buy.  The columns are 'product_id' (ID number
# that uniquely identifies each product), 'product_name' (name of the product), 'aisle_id' (ID number that uniquely 
# identifies each grocery aisle category), 'department_id' (ID number that uniquely identifies each grocery department 
# category).  
# 
#  In order_products file each row corresponds to one item placed in an order.  The columns are 'order_id'(ID number that 
# uniquely identifies each order), 'product_id'(ID number that uniquely identifies each product), 'add_to_cart_order' (the 
# sequential order in which each item was placed in the cart), 'reordered' (0 if the customer has never ordered this product
# before, 1 if they have). 
# 
#  In aisles file is information regardin gthe aisle in the store.  The columns discuss 'aisle_id' (ID number that uniquely
# identifies each grocery aisle category) and 'aisle' (name of the aisle). 
# 
#  In departments file contains information regarding the departments in each grocery store.  The columns are 'department_id'
# (ID number that uniquely identifies each grocery department category) and 'department' (name of the department). 
# 

# In[1]:


import pandas as pd


# #import all csv files.  all have seperators as :. made dataframe name same as file name.  inserted column names. no decimals needed. 

# In[2]:


order_products = pd.read_csv('/datasets/order_products.csv',sep =';', low_memory=False)


# In[3]:


order_products.info()


# In[4]:


aisles = pd.read_csv('/datasets/aisles.csv',sep=';')


# In[5]:


aisles.info()


# In[6]:


departments = pd.read_csv('/datasets/departments.csv',sep=';')


# In[7]:


departments.info()


# In[8]:


products = pd.read_csv('/datasets/products.csv',sep=';')


# In[9]:


products.info()


# In[10]:


orders = pd.read_csv('/datasets/instacart_orders.csv',sep=';', low_memory=False)


# In[11]:


print(orders)


# ## Find and remove duplicate values (and describe why you make your choices)

# ### `orders` data frame

# In[12]:


# Checked for duplicated orders
#chose sum because if the returned result is zero indication that no duplicates exist 
print(orders.duplicated().sum())
orders.info()


# In[13]:


# Checked for all orders placed Wednesday at 2:00 AM
#create variable to search dataFrame if 2 am time and Wed. date selected. 
wed_2am_orders = orders[
    (orders['order_dow'] == 2) & 
    (orders['order_hour_of_day'] == 2)
]

print(wed_2am_orders)


# In[14]:


# Removed duplicate orders
#drop_duplicates used to identify the column to target for replicates of order.  
#if order_id is the same it is the same order number being repeated.  Reset the index so that if rows are removed there is no gaps. 
order_no_duplicates=orders.drop_duplicates(subset='order_id').reset_index(drop=True)
print(order_no_duplicates)


# In[15]:


# Double check for duplicate rows
#check for duplicates in newly created variable where they are dropped. checked with .info() to compare from original sount. 
print(order_no_duplicates.duplicated().sum())
order_no_duplicates.info()


# Appears that almost half of the orders were duplicates

# In[16]:


# Double check for duplicate order IDs only
#focus on column "order_id" to search for duplicates. double check with .info()
print(order_no_duplicates.duplicated('order_id').sum())
order_no_duplicates.info()


# ### `products` data frame

# In[17]:


# Check for fully duplicate rows
#use duplicated to check and sum to give the count of anything duplicated
print(products.duplicated().sum())
products.info()


# In[18]:


# Check for just duplicate product IDs
print(products['product_id'].duplicated().sum())
products.info()


# In[19]:


# Check for just duplicate product names (convert names to lowercase to compare better)
#first confirm what df looks like before beginning. 
print(products['product_name'])


# In[20]:


#reassing lowered case to same name 
products['product_name']=products['product_name'].str.lower()


# In[21]:


#confirm command changed case
products


# In[22]:


#remove all rows without data in original dataframe
products = products.dropna(subset=['product_name'])


# In[23]:


#sum values that are duplicated. 
products['product_name'].duplicated().sum()


# In[24]:


products.info()


# In[25]:


# Check for duplicate product names that aren't missing
display(products[~products['product_name'].isna()])
products[~products['product_name'].isna()].duplicated().sum()


# ### `departments` data frame

# In[26]:


#decide to check for duplicates in entire row 
departments.duplicated().sum()
#check for duplicates in each column 
departments['department_id'].duplicated().sum()
departments ['department'].duplicated().sum()


# In[27]:


#decide to check for any empty cells
display(departments[~departments['department_id'].isna()])
display(departments[~departments['department'].isna()])


# ### `aisles` data frame

# In[28]:


#decide to check for duplicates in entire row 
aisles.duplicated().sum()
#check for duplicates in each column 
aisles['aisle_id'].duplicated().sum()
aisles['aisle'].duplicated().sum()


# In[29]:


#decide to check for any empty cells
display(aisles[~aisles['aisle_id'].isna()])
display(aisles[~aisles['aisle'].isna()])


# ### `order_products` data frame

# In[30]:


# Check for fullly duplicate rows
order_products.duplicated().sum()


# In[31]:


# Double check for any other tricky duplicates
#decided to look for partial duplicates
order_products[['order_id','product_id']].duplicated().sum()

#order_products['order_id','product_id', 'add_to_cart_order', 'reordered'].duplicated().sum()
#thought about look for duplicates with case differences but all four of the columns are numbers so not needed  
# check if any empty frields
#display(order_products[~order_products['product_id'].isna()])
#order_products[~order_products['product_id'].isna().all]
#print(order_products[~order_products['order_id'].isa()].all)
#print(order_products[~order_products['add_to_cart_order'].isa().all])
#print(order_products[~order_products['reordered'].isa().all])
#print(order_products[~order_products[''].isa().all])


# ## Find and remove missing values
# 

# ### `products` data frame

# In[32]:


#find missing values
products.info()
products.isna().sum()


# In[33]:


# Are all of the missing product names associated with aisle ID 100?
#filter on multiple conditions
print(len(products[(products['product_name'].isnull()) & (products['aisle_id'] == 100)])==products['product_name'].isna().sum())


# In[34]:


# Are all of the missing product names associated with department ID 21?
print(len(products[(products['product_name'].isnull()) & (products['department_id'] == 21)])==products['product_name'].isna().sum())


# In[35]:


# What is this ailse and department?
print(products[(products['department_id'] == 21) & (products['aisle_id'] == 100)])


# In[36]:


# Fill missing product names with 'Unknown'
products['product_name'].fillna('Unknown', inplace=True)
print(products.isna().sum())


# ### `orders` data frame

# In[37]:


#check for missing values 
orders.isna().sum()


# In[38]:


# Are there any missing values where it's not a customer's first order?
# only column with missing values is in "days_since_prior_order" so check that column for null when order_number solidified 
print(len(orders[(orders['days_since_prior_order'].isnull()) & (orders['order_number'] == 100)])==orders['days_since_prior_order'].isna().sum())


# ### `order_products` data frame

# In[39]:


order_products.isna().sum()


# In[40]:


order_products.isnull().sum()


# In[41]:


# What are the min and max values in this column?
print(order_products.groupby('add_to_cart_order').max())
print(order_products.groupby('add_to_cart_order').min())


# In[42]:


# Save all order IDs with at least one missing value in 'add_to_cart_order'
#create assigned variable to store the order_id number when value missing in column"add_to_cart_order"
add_to_cart_order=order_products.loc[order_products['add_to_cart_order'].isna(),'order_id'].tolist()
print(add_to_cart_order)


# In[43]:


# Do all orders with missing values have more than 64 products?
order_products[order_products['add_to_cart_order'].isna()].groupby('order_id')['product_id'].count().reset_index()['product_id'].sort_values


# In[44]:


order_products['add_to_cart_order'].isna().sum


# In[45]:


# Replace missing values with 999 and convert column to integer type
order_products['add_to_cart_order']=order_products['add_to_cart_order'].where(order_products['add_to_cart_order'] == 'add_to_cart_order', '999')
order_products['add_to_cart_order']=order_products['add_to_cart_order'].astype(int)
print(order_products['add_to_cart_order'].head())


# In[46]:


len(order_products['product_id'].unique())


# ###  Verify that the `'order_hour_of_day'` and `'order_dow'` values in the `orders` tables are sensible (i.e. `'order_hour_of_day'` ranges from 0 to 23 and `'order_dow'` ranges from 0 to 6)

# In[47]:


#import plotting library to enable visualizations
from matplotlib import pyplot as plt


# In[48]:


#filter for multiple factors to ensure column of ordering day has values between o and 23
orders_sensible=(orders[(orders['order_hour_of_day']>=0) & (orders['order_hour_of_day']<=23)])
print(orders_sensible)


# In[49]:


ordering_hour_graph=orders.groupby('order_hour_of_day').size()
print(ordering_hour_graph)


# In[50]:


ordering_hour_graph.plot(kind='bar', title='Verify Ordering Hour is Sensible', xlabel='Ordering Hour', ylabel= "frequency of Occurance")


# In[51]:


#create table to visualize data
#orders['order_hour_of_day'].plot(title='Verify Ordering Hour is Sensible',xlabel='Order Hour of Day', ylabel='Order Frequency', style='0',xlim=[0,25])

plt.bar(ordering_hour_graph.index, ordering_hour_graph.values, color='purple')

# Add labels and title
plt.xlabel('Order Hour of Day')
plt.ylabel('Order Frequency')
plt.title('Verify Ordering Hour is Sensible')

# Show the plot
plt.show()


# In[52]:


#filter for multiple factors to ensure column of ordering day has values between o and 6
hour_sensible=(orders[(orders['order_dow']>=0) & (orders['order_dow']<=6)])
print(hour_sensible)


# In[53]:


#verify via graph 
#create variable of grouped information from column 
hour_sensible_grouped=orders.groupby('order_dow').size()
print(hour_sensible_grouped)
hour_sensible_grouped.plot(kind='bar', title='Verify Ordering Day is Sensible', xlabel='Ordering Day', ylabel= "Frequency of Occurance")


# ### What time of day do people shop for groceries?

# In[54]:


grocery_order_hour=orders['order_hour_of_day'].value_counts()
print(grocery_order_hour)
#perform a value count for the hour of day when orders occur.  Most frequent appears to be at 10 am since numbers on a 24 hour cycle. 


# In[55]:


plt.bar(grocery_order_hour.index, grocery_order_hour.values, color='pink')

# Add labels and title
plt.xlabel('Order Hour of Day')
plt.ylabel('Order Frequency')
plt.title('Verify Time of Day to Order')

# Show the plot
plt.show()


# It seems the most common time to order is between 10 am and 4 pm.  Most specific hour surge is at 10 am.  

# ### What day of the week do people shop for groceries?

# In[56]:


#use value_counts to sort column for day people shop into number of people on each day.  People shop everyday but the most orders are created on Monday. 
weekday_shopping=orders['order_dow'].value_counts()
print(weekday_shopping)


# In[57]:


plt.bar(weekday_shopping.index, weekday_shopping.values, color='red')

# Add labels and title
plt.xlabel('Day of Week')
plt.ylabel('Order Frequency')
plt.title('Frequent Weekday Shopping')

# Show the plot
plt.show()


# It appears the most common days for ordering is the beginning of the week.  This would be on Sunday and Monday. 

# ### How long do people wait until placing another order?

# In[58]:


length_wait=orders['days_since_prior_order'].value_counts()


# In[59]:


#Show via plot 
plt.bar(length_wait.index, length_wait.values, color='green')

# Add labels and title
plt.xlabel('Days Wait to Reorder')
plt.ylabel('Quantity of Users')
plt.title('Time Users Wait Before Reorder')


# People seem to vary in their reorder time but most common is 30 days after their prior order 

# ### Is there a difference in `'order_hour_of_day'` distributions on Wednesdays and Saturdays?

# In[60]:


from matplotlib import pyplot as plt


# In[61]:


orders[orders['order_dow']==2]['order_hour_of_day'].plot(kind='hist',bins=20)
orders[orders['order_dow']==6]['order_hour_of_day'].plot(kind='hist',bins=20, alpha=0.5, title="Ordering Hour Distribution", xlabel="Hour of Ordering")
plt.legend(['Wed.','Saturday'])
plt.show


# It seems the distrubtion between Wed. and Saturday is similiar.  However it appears more orders are made on Wed. overall. 

# ###  What's the distribution for the number of orders per customer?

# In[62]:


orders_per_customer = orders.groupby('user_id')['order_id'].count()
#create a new grouping of each unique user id compared to unique order numbers 


# In[63]:


plt.figure(figsize=(10, 6))
plt.hist(orders_per_customer, bins=range(1, orders_per_customer.max() + 1), edgecolor='k', alpha=0.7)
plt.title('Distribution of Number of Orders per Customer')
plt.xlabel('Number of Orders')
plt.ylabel('Frequency')
plt.xticks(range(1, orders_per_customer.max() + 1))
plt.show()


# ### What are the top 20 popular products (display their id and name)?

# In[64]:


top_products = order_products['product_id'].value_counts().reset_index().head(20)
top_products.columns = ['product_id', 'count']


# In[65]:


top_products_named = top_products.merge(products, on='product_id')[['product_id', 'count', 'product_name']]
display(top_products_named)


# ### For each product, what proportion of its orders are reorders?

# In[66]:


reordered_products = order_products.groupby('product_id').agg({'reordered': ['sum', 'count', 'mean']}).reset_index()
#create a new table where the product id column is filtered through for their sum, count, and mean, if the item was reordered. 


# In[67]:


reordered_products.columns = ['product_id', 'total_reorders', 'total_orders', 'reorder_proportion']
#identify column names to new table. 


# In[68]:


display(reordered_products)
#display table 


# ###  For each customer, what proportion of their products ordered are reorders?

# In[69]:


#create new variable and name the columns if grouped by the unique user id and items reordered
order_id_df = pd.merge(order_products, orders, on='order_id')
#create a merged dataframe from order_products and orders around the column 'order_id'


# In[70]:


reorder_proportions = order_id_df.groupby('user_id')['reordered'].mean().reset_index()
reorder_proportions.rename(columns={'reordered': 'reorder_proportion'}, inplace=True)
print(reorder_proportions)
#group the data by user_id, then calculate the mean of the reordered column for each group. The reordered column contains binary data so taking the mean gives you the proportion of reordered items for each user.


# In[71]:


print(reorder_proportions['reorder_proportion'].mean())
#seems that almost half of each users order is repeated 


# In[72]:


#plt.figure(figsize=(10,6))
plt.bar(reorder_proportions['user_id'], reorder_proportions['reorder_proportion'], color='skyblue')
plt.xlabel('User ID')
plt.ylabel('Reorder Proportion')
plt.title('Unique Customer Reorder Proprtions')
plt.show()  


# Instant Data Review Conclusions
# Most common order time was between 10 am and 4 pm.  Most common day to order is Sunday or Monday. Routinely people wait 30 days between reorders. Hypothesize that people who only order groceries once a month are in a higher tax bracket and routine Instacart users. Majority of customers only utilized the service for less than 4 orders. Indication that users took advantage of a special or that the service was not helpful in their lifestyle. Out of the top 20 items ordered, 15 of them are fruit. 
# 
