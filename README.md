# SQL query tester
## About This Project
### Features
- Table schemas for questions are generated automatically from answer_as_query's.
- Single command to dump all secondary_table data and initialize roles `flask db_custom seed_secondary_tables`.
- Reactive and Stateful front end using ReactJs.
- Single command `docker compose up` to host locally without worrying about fiddling with the installation of dependencies.

### How to deploy your own
#### Docker Compose
If you do not want to go through the effort of installing dependencies (aside from docker) and only want to use this app in a development environment. Simply run: `docker compose up` from the command line and navigate to `localhost:9090` in a browser of your choice.

#### Full Fleged Deployment
- [Front End](./front-end)
- [Back End](./back-end)

### Live deployment
https://sqltestapp.ml

<img src="./docs/preview.png" alt="preview" width="80%">



## Planning documentation
## Main Database
<img src="./docs/dbdiagram.png" alt="main_db" width="70%"/>

## Wire Frames
<img src="./docs/landing.png" alt="landing page" width="60%"/>
<img src="./docs/question.png" alt="question page" width="60%"/>

### Api documentation
https://editor.swagger.io/?url=https://raw.githubusercontent.com/mo-ccc/sql-query-test-application/master/docs/swagger.yml

### Kanban board
https://trello.com/b/MnSlqP47/sql-query-test-application

## Original Plan
1. When a user enters an email, main database is updated with a new `user` record and a new `test` record.
2. The test becomes accessible through the client as long as `test` record exists and has not been submitted.
3. User enters a query and presses execute causing `answer_as_query` to run on the question database alongside the user entered query. 
4. The two results are compared. If the results from the user entered query matches the `answer_as_query` results: the server will return that user has the right answer. query outcome is returned regardless.
5. User submits query. The query the user submitted is saved along with the time the user submitted the query and the result (either 0 or 1).
6. User is redirected to page with a thank you message.
