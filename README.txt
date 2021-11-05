# Full Stack API Final Project


## Introduction
This is a Udacity course project implementing Trivia game functionalities:
1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.
For more information, please refer to https://github.com/udacity/FSND/tree/master/projects/02_trivia_api/starter.


## Getting Started
To install all dependencies, use terminal to enter the frontend folder and run "npm install", then change directory to the backend folder and run "pip install -r requirements.txt".
To run the app, run "set FLASK_APP=flaskr" in the backend folder to export the app and "flask run --reload" to run the server, then change to the frontend diretory and run "npm start" to build up the app.
Go to http://localhost:3000 to use it.


## Errors
Errors are returned as JSON objects in the following format:
{
    "success": False, 
    "error": 404,
    "message": "Not found"
}
The API will return two error types when requests fail:
404: Not found
422: Unprocessable


## Endpoints
GET /questions
return paginated questions (default ten questions per page), total questions, all categories, and get categories.
EXAMPLE curl http://127.0.0.1:5000/questions
{"categories":{"1":"Science","2":"Art","3":"Geography","4":"History","5":"Entertainment","6":"Sports"},"currentCategory":5,"questions":[{"answer":"Edward Scissorhands","category":5,"difficulty":3,"id":6,"question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"},{"answer":"Brazil","category":6,"difficulty":3,"id":10,"question":"Which is the only team to play in every soccer World Cup tournament?"},{"answer":"Uruguay","category":6,"difficulty":4,"id":11,"question":"Which country won the first ever soccer World Cup in 1930?"},{"answer":"George Washington Carver","category":4,"difficulty":2,"id":12,"question":"Who invented Peanut Butter?"},{"answer":"Lake Victoria","category":3,"difficulty":2,"id":13,"question":"What is the largest lake in Africa?"},{"answer":"The Palace of Versailles","category":3,"difficulty":3,"id":14,"question":"In which royal palace would you find the Hall of Mirrors?"},{"answer":"Agra","category":3,"difficulty":2,"id":15,"question":"The Taj Mahal is located in which Indian city?"},{"answer":"Escher","category":2,"difficulty":1,"id":16,"question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"},{"answer":"Mona Lisa","category":2,"difficulty":3,"id":17,"question":"La Giaconda is better known as what?"},{"answer":"One","category":2,"difficulty":4,"id":18,"question":"How many paintings did Van Gogh sell in his lifetime?"}],"totalQuestion":17}


GET /categories
return all categories
EXAMPLE curl http://127.0.0.1:5000/categories
{"categories":{"1":"Science","2":"Art","3":"Geography","4":"History","5":"Entertainment","6":"Sports"}}


GET /categories/{category_id}/questions
return all question in given category, number of them, and current category
EXAMPLE curl http://127.0.0.1:5000/categories/1/questions
{"currentCategory":1,"questions":[{"answer":"The Liver","category":1,"difficulty":4,"id":20,"question":"What is the heaviest organ in the human body?"},{"answer":"Alexander Fleming","category":1,"difficulty":3,"id":21,"question":"Who discovered penicillin?"},{"answer":"Blood","category":1,"difficulty":4,"id":22,"question":"Hematology is a branch of medicine involving the study of what?"},{"answer":"no","category":1,"difficulty":1,"id":42,"question":"is earth a plane"}],"totalQuestion":4}


DELETE /question/{question_id}
delete the given question, return deleted question id
EXAMPLE curl -X DELETE http://127.0.0.1:5000/questions/10
{"question_id":10}


POST /question
If request body contains "searchTerm", search an existing question, return paginated questions that satisfy, number of them, and current category. If request body stores a new question, post a new question, return this question.
EXAMPLE curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"searchTerm":"What"}'
{"currentCategory":5,"questions":[{"answer":"Edward Scissorhands","category":5,"difficulty":3,"id":6,"question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"},{"answer":"Lake Victoria","category":3,"difficulty":2,"id":13,"question":"What is the largest lake in Africa?"},{"answer":"Mona Lisa","category":2,"difficulty":3,"id":17,"question":"La Giaconda is better known as what?"},{"answer":"The Liver","category":1,"difficulty":4,"id":20,"question":"What is the heaviest organ in the human body?"},{"answer":"Blood","category":1,"difficulty":4,"id":22,"question":"Hematology is a branch of medicine involving the study of what?"}],"totalQuestions":5}
EXAMPLE curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question":"is earth a plane","answer":"no","difficulty":1,"category":1}'
{"question":{"answer":"no","category":1,"difficulty":1,"id":42,"question":"is earth a plane"}}


POST /quizzes
return a random question in the given category and is not repetitive to given previous met questions
EXAMPLE curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [1,2,3,4],"quiz_category": {"type": "Science", "id": "1"}}'
{"question":{"answer":"Blood","category":1,"difficulty":4,"id":22,"question":"Hematology is a branch of medicine involving the study of what?"}}

