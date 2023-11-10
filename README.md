# osu361_trivia_app

This is an application written in Python that accesses a trivia API and filters questions that have multiple choices to answer with. Copy the next_page.py code and run it in an IDE of your choice.

# :pencil2: Communication Contract (Partner Microservice)

A. To request data, simply visit https://open-meteo.com/en/docs/historical-weather-api to find an updated API call that checks for three days prior or more as far as historical data. After selecting the API url, place it in the response variable that looks like:

response = requests.get("enter API here")

When running the code, you should be able to access all keys from the json formatted API call, this should be helpful to see what's going on, but is not necessary. I access only temperature in Fahrenheit and the datetime in this call.

B. To receive data, run the code. As long as you have followed the procedure given here you should now see all the dictionary keys of the json file and received the temperature in Fahrenheit and datetime from the call. Now, you will see the .txt file entitled microservice_data.txt, this will now be populated with two sets of values, separated by commas. This can be accessed by any other code that may be necessary. 


C. UML Diagram
<img width="879" alt="Screenshot 2023-11-09 at 3 02 25 PM" src="https://github.com/bluestonewhitestone/osu361_trivia_app/assets/89286297/95c44fb7-2338-4809-b986-90c16d2cae65">

