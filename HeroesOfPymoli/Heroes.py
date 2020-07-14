# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# %%
# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)
purchase_data.head

# %% [markdown]
# * Display the total number of players
# 

# %%
#Unique count to filter duplicate players and display in Dataframe
TotalPlayer = purchase_data["SN"].nunique()
TotalPlayers = pd.DataFrame({"Total Players": TotalPlayer}, index=[0])
TotalPlayers

# %% [markdown]
# ## Purchasing Analysis (Total)
# %% [markdown]
# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# %%
#Create DataFrame with 4 columns, using a dictionary with keys and values based on agg functions. 
SummaryDF = pd.DataFrame({"Number of Unique Items": [purchase_data["Item ID"].nunique()], 
                                "Average Price": [purchase_data["Price"].mean()],
                                "Number of Purchases": [purchase_data["Purchase ID"].count()],
                                "Total Revenue": [purchase_data["Price"].sum()]})

SummaryDF = SummaryDF.style.format({"Average Price": "${:,.2f}", "Total Revenue": "${:,.2f}"})
SummaryDF

# %% [markdown]
# ## Gender Demographics

# %%
#Create Dataframe with Gender as index, find total amount of players for each gender, removing duplicates. 
GenderDemo = purchase_data.drop_duplicates(subset="SN", keep = "first")
GenderDemo = GenderDemo.groupby("Gender").count()
GenderDemo = GenderDemo.iloc[:, 0:2]
GenderDemo.columns=["Total Count", "% of Players"]
GenderDemo["% of Players"] = GenderDemo["Total Count"]/TotalPlayer
#Formatting
GenderDemo = GenderDemo.rename_axis("Index").sort_values(by = ["Total Count", "Index"], ascending=[False, True])
GenderDemo = GenderDemo.style.format({"% of Players": "{:.2%}"})
GenderDemo

# %% [markdown]
# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 
# %% [markdown]
# 
# ## Purchasing Analysis (Gender)
# %% [markdown]
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# %%
#Get Purchase Count, Average Purchase Price, Total Purchase Price
GenderPurchase = purchase_data.groupby("Gender").agg({"SN": ["count"], "Price": ["mean", "sum"]})
#Rename columns
GenderPurchase.columns = ["Purchase Count", "Average Purchase Price", "Total Purchase Value"]
#Drop dups for Total Purch PER PERSON
NoDups = purchase_data.drop_duplicates(subset="SN", keep = "first")
NoDups = NoDups["Gender"].value_counts()
#Get Total by gender
TotalPur = purchase_data.groupby("Gender")["Price"].sum()
#equation
ATP = TotalPur/NoDups
#add to DF
GenderPurchase["Avg Total Purchase Per Person"] = ATP
#Format
GenderPurchase = GenderPurchase.style.format({"Average Purchase Price": "${:.2f}", "Total Purchase Value": "${:,.2f}", "Avg Total Purchase Per Person":"${:,.2f}"})
GenderPurchase

# %% [markdown]
# ## Age Demographics
# %% [markdown]
# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# %%
#Drop dups so peeps show up once
AgeDemo = purchase_data.drop_duplicates(subset="SN", keep = "first")
#my bins, my boxes, my categories
bins = [0, 9.9, 14.9, 19.9, 24.9, 29.9, 34.9, 39.9, 1000]
#My labels
labels=["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]
#Add to DF
AgeDemo["Age Demo"] = pd.cut(AgeDemo["Age"], bins, labels=labels, include_lowest=True)
#Get new index
AgeDemo = AgeDemo.groupby("Age Demo")
#Cull some columns, just need 1 count
AgeDemo = AgeDemo.count().iloc[:, 0:2]
#Rename
#AgeDemo.rename(columns={"Purchase ID": "Total Count", "SN": "% of Players"}, inplace=True )
AgeDemo.columns=[ "Total Count",  "% of Players"]
#Equation to get %
AgeDemo["% of Players"] = (AgeDemo["Total Count"]/TotalPlayer)*100
#Formatting
AgeDemo = AgeDemo.style.format({"% of Players":"{:,.2f}%"})
AgeDemo

# %% [markdown]
# ## Purchasing Analysis (Age)
# %% [markdown]
# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# %%
#my bins, my boxes, my categories
bins = [0, 9.9, 14.9, 19.9, 24.9, 29.9, 34.9, 39.9, 1000]
#My labels
labels=["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]
#Add to DF
PurAge = purchase_data
PurAge["Age Demo"] = pd.cut(PurAge["Age"], bins, labels=labels, include_lowest=True)
####################################
####Need this variable for later##
TotalAgePurchase = PurAge.groupby("Age Demo")["Price"].sum()
######################################

#Manipulate data and change DF index
PurAge = PurAge.groupby("Age Demo").agg({"SN":["count"], "Price":["mean", "sum"]})
#Rename DF columns
PurAge.columns = ["Purchase Count", "Average Purchase Price", "Total Purchase Value"]

#Avg Total Purchase Per Person
#Drop dups so peeps show up once
PerPerson = purchase_data.drop_duplicates(subset="SN", keep = "first")
PerPerson["Age Demo"] = pd.cut(PerPerson["Age"], bins, labels=labels, include_lowest=True)
OneAge = PerPerson["Age Demo"].value_counts()
ATP2 = TotalAgePurchase/OneAge
PurAge["Avg Total Purchase Per Person"] = ATP2
#Formatting
PurAge = PurAge.style.format({"Average Purchase Price": "${:.2f}", "Total Purchase Value": "${:,.2f}", "Avg Total Purchase Per Person":"${:,.2f}"})
PurAge

# %% [markdown]
# ## Top Spenders
# %% [markdown]
# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# %%
TopSpenders = purchase_data.groupby("SN").agg({"SN":["count"], "Price": ["mean", "sum"]})
TopSpenders.columns = ["Purchase Count", "Average Purchase Price", "Total Purchase Value"]
TopSpenders.sort_values(by=["Total Purchase Value"], ascending=False, inplace=True)
TopSpenders = TopSpenders.iloc[0:5,:]
TopSpenders = TopSpenders.style.format({"Average Purchase Price": "${:,.2f}", "Total Purchase Value": "${:,.2f}"})
TopSpenders

# %% [markdown]
# ## Most Popular Items
# %% [markdown]
# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 



# %%
PopItem = purchase_data.groupby(["Item ID","Item Name"]).agg({"Price": ["count", "first", "sum"]})
PopItem.columns = ["Purchase Count",  "Item Price", "Total Purchase Value"]
PopItem.sort_values(by=["Purchase Count"], inplace=True, ascending=False)
PopItem = PopItem.iloc[0:5,:]
PopItem = PopItem.style.format({"Item Price": "${:,.2f}","Total Purchase Value":"${:,.2f}"})

# %% [markdown]
# ## Most Profitable Items
# %% [markdown]
# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# %%
ProfitItem = purchase_data.groupby(["Item ID","Item Name"]).agg({"Price": ["count", "first", "sum"]})
ProfitItem.columns = ["Purchase Count",  "Item Price", "Total Purchase Value"]
ProfitItem.sort_values(by=["Total Purchase Value"], inplace=True, ascending=False)
ProfitItem = ProfitItem.iloc[0:5,:]
ProfitItem = ProfitItem.style.format({"Item Price": "${:,.2f}","Total Purchase Value":"${:,.2f}"})
ProfitItem


# %%


