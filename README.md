# Break the Budget
### my EPA web application for the Software Engineering & Agile module.

---

To run the application, first open your browser of choice and navigate to https://breakthebudget.org. 
You will be greeted on the landing page. In the top right corner of the page, there is a “Login” button, 
press it, and it will take you to the appropriate “Login” page. Enter the below credentials from the table below
into the username and password on the page and press “Log in”. 

---
These credentials are for a user with 
admin privileges.

| Userame   | Password  |
|-----------|-----------|
| QAadmin1! | QAadmin1! |
---

Navigate to the Statement List page via the “Statements” button in the navigation bar in the top area of the page. 
From the GitHub repository, download one of the three “.csv” files found in the “data” folder and then press the “Choose file” button. 
Choose the downloaded “.csv” file, click “OK” and then press the “Upload Statement” button. On the page, 
a notification will appear showing the result of the operation. If the notification shows an error, try a different “.csv” file 
from the “data” directory in the GitHub repository. 

If the file was successfully uploaded, press the “Budgets” button in the navigation bar, which will take you to the Budget List page. 
Press the “Create New Budget” button on the page, that will redirect you to a new Budget. In the “Budget Name” field, 
remove the “New Budget” text and type in “Travel”. Below is the field “Monthly Budget Amount” currently showing “0.0”, 
change that number to “100”. The last field on the page has the placeholder “Type text here”, type in it “Pocket Withdrawal”. 
Next, press the “Add Clause” button which is right next to the field and lastly press the “Update” button. After that, 
you should have received the “Budget updated successfully” notification.

Lastly, press the “Account” button in the navigation bar. This is the page where it is possible to view sums of money
spent and earned in a month. There are two dropdown lists on the page, one called “Select Year” and the other “Select Month”. 
Press each dropdown and select an available year and month. In addition, tick the “Re-calculate Summary” checkbox. Finally, 
press the “Get Summary” button. This will calculate all totals of money going in and out of the tracked account from the 
transactions in the uploaded bank statements and will display the results. A new card will appear with the text “Travel” 
and amounts for “Total Money In” and “Total Money Out” which show the total amount of debit and credit from transactions 
with the description “Pocket Withdrawal”, as well as “Monthly Limit: 100.00”.

To complete the process as a different user, press the “Logout” button in the top right corner of the page, 
and choose to log in with the second pair of credentials provided in the table below.

---

These credentials are for a user with 
basic privileges.

| Userame   | Password  |
|-----------|-----------|
| QAbasic1! | QAbasic1! |
