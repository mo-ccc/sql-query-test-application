# SQL query tester
## Main Database
![main_db](./docs/dbdiagram.png)

## Plan
- Have a main database which will contain all user data.
- Have a question database that will handle testing specifically.

1. When a user enters an email, main database is updated with a new `user` record and a new `test` record.
2. The test becomes accessible through the client as long as `test` record exists and has not been submitted.
3. User enters a query and presses execute causing `answer_as_query` to run on the question database alongside the user entered query. 
4. The two results are compared. If the results from the user entered query matches the `answer_as_query` results: the server will return that user has the right answer. query outcome is returned regardless.
5. User submits query. The query the user submitted is saved along with the time the user submitted the query and the result (either 0 or 1).
6. User is redirected to homepage with a thank you message.



