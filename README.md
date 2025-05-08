# MBTA-Web-App-Project
## Nearest MBTA station search

## 1. Project Overview

This web app project is designed using Flask, Python, html, and different python libraries to help users find the nearest MBTA public transportation stop based on a location they provide.
The location user provides has to be a named location that is stored in the Mapbox Geocoding database. The project utilizes the MApbox Geocoding API to convert place names into coordinates,
and the MBTA Realtime API to locate nearby stops and display real-time departure predictions. The app features a very simple user-friendly website form that allows users to enter any named
Boston-area location, and returns the nearest stop's name, its wheelchair accessibility status, and the soonest upcoming departure. In addition to meeting the core project requirements, I
extended the functionality by including the real-time arrival data and attempted sorting data by walk-plus-wait time to enhance user's decision making. 

## 2. Reflection. 

The project began with API exploration and progressed toward a full frontend-backend integration with FLask. Using mbta_helper.py for all API logic and app.py for user interaction and rendering
was key to successfully allocating parts of the project into a more concise form. This project gave me a lot of experience with debugging giving me a lot of learning opportunities. For example, 
there were a lot of early issues with managing inconsistent return values from helped functions while trying to implement additional layers and make the project cooler. The function used in the
helper module are very tightly related and changing just one of them to implement a new feature caused unexpected results and required a lot of editing and debugging in other functions. 
I was happy to learn how to incorporate API keys into the URLs and how to design them in the code to make sure they worked. Additionally, incorporating real-time data added complexity, especiallyu when filtering stop predictions and linking them to different stops, as well as formatting departure times. I worked on the project alone so there are no team dynamics to discuss.

From a learning perspective, the most valuable skills gained included working more with APIs, building a Flask app from scratch, and isolating the .env variables :). Parsing and interpreting 
JSON responses from two different APIs in tandem gave deeper insight into real-world web development. One especially useful takeaway was learning to encode user input safely for URLs using
urllib.parse.quote, which prevented many early buds. I also feel way more comfortable receiving errors when working with APIs as I understand better when the issue is with the code or the 
website, understand how to better handle missing data, e.g. when MBTA API didn't return nearby stations. Throughout the process I utilized multiple information sources provided in the 
assignment and in the resources folder of the repository. Additionally, AI tools like ChatGPT played a big role in my learning process. I used to understand bugs, summarize and explain 
different libraries and commands, and I feel like my prompts to it improved significantly throughout the semester. If I were to start over, I'd spend more time trying to learn more about Flask
as it is a crucial tool for web applications which is everything now. 