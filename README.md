# SmartBag-Flipkart-Grid-3.0
SmartBag Creator Challenge - Flipkart Grid 3.0

We solved the SmartBag creator challenge problem of Flipkart Grid 3.0 using React for frontend
and flask for backend of our project.
As Flipkart database gets updated frequently, we decided to fetch the data, train on it and
update smartbags for all users after a fixed period of time. For example, after every 12 hours
the users’ smartbag gets updated with the most recent predictions using the most recent data.
For predicting the smartbag for a certain user, rather than using the data of all the users we
decided to make clusters of similar users and use only the data of the users in that particular
cluster of which, the user for whom we are predicting the smart bag, is part of. By doing so,
the predicted items will be more relevant to that particular user.


for details refer documentation
