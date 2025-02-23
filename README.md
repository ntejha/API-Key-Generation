# API-Key-Generation

LLM's are very powerful tools, in order to use them carefully. we need to use them through an API (Application Programming Interface).

We are going to write a very simple python API to control access to an LLM or an AI model.

### Why do you need an API ?

Lets take an example, you want to run an LLM. like deepseek, wither your going to run it locally or going to use a cloud provider. API key this is where you end request any time to use the LLM.

In production environment, if we are going to connect the frontend to the API. this will lead to a security risk. Where, if someone has access to the frontend code. Then, he would have use it to some other purposes and cost you a ton of money.

The main idea, is going to be what all the application these days are doing. The front-end users is going to request something, that request is going to go to the backend. Then the backend will decide, should we allow this or not. Lets take the user has 10 credits -> 10 LLM calls, after ending this credits he pays us to use it.

We need to be able to control the calls to our LLM, so that we can decide which users can call it or not call it and make sure that it doesn't cost us a lot of money.

### Initial Setup

We are going to setup some things to do this, which are :

- Git clone this repository
- ```pip install -r requirements.txt```
- ```uvicorn main:app --reload```
- run ```python test-api.py```

This is the whole running of this project.


I am also thinking to see this videos and enhance the project.

01 : https://www.youtube.com/watch?v=5GxQ1rLTwaU
02 : https://www.youtube.com/watch?v=UtSSMs6ObqY