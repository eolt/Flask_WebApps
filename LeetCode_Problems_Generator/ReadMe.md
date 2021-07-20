# LeetCode Problems Generator

## Brief Description 

This program will use python request and Selenium to scrape and get problems and solutions from LeetCode.

This repository runs the program through main.py. The file can request api from LeetCode, store the problems lists depending on difficulty, and run Selenium to obtain the descriptions of each problem.

There is currently and additional setup to run flask locally which generates a web browser form to enter first name and email. The process of saving the emails is done by mailchimp marketing api.

## TODOs
- I plan to use a mailing api to send a random problem by email at a daily or custom schedule.
- The question will be properly formatted and designed for readability and responsiveness. 
- ~~Implement Flask framework to recieve user emails~~
- Create a login where users can customize type of problems and delivery schedule. 
