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

### Ollama

We are going to learn how to use Ollama to run LLM models locally.

#### Downloading Ollama

- Go to internet and type Ollama and download it.
- then go to terminal and type Ollama, to confirm the installation.
- run ```ollama run mistral``` 
- In order to see the list of Ollama models in your system, ```ollama list``` 
- If you want to come out of the LLM, you type```/bye``` 
- In order to start the Ollama server to startup, if not type ```ollama serve```
- To remove model from the list just type ```ollama rm mistral```
#### Customization of a model

- Create a file named Modelfile
- add this code inside that Modelfile
```
FROM mistral

PARAMETER temperature 1

SYSTEM """
You are mario from Super Mario Bros. Answer as Mario, the assistant, only.
"""
```
- go to the folder this code is in terminal
- type this ```ollama create mario -f Modelfile```
- To use this model just type ```ollama run mario```


### Quickly Authenticate Users with FastAPI and Token Authentication

#### Essential Libraries

The libraries, which we need would be : 
- Python 3.8 or above
- FastAPI
- uvicorn
- python-multipart
- python-jose[cryptography]
- passlib[[[bcrypt]]]

#### Setting up a basic FastAPI

```
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel  # this is for giving the type is going to accept

app = FastAPI()   # Intializing the FastAPI instance

class Data(BaseModel):
	name: str
@app.post("/create/") #For accepting API requests
async def create(data: Data):
	return {"data": data}
	
@app.get("/test/{item_id}/")   # creation of endpoints
async def test(item_id: str, query: int):  #item_id is path parameter and query is query parameter
	return {"hello":item_id}

```

Save this file as main.py, just go to terminal and go to the folder and type ```uvicorn main:app --reload```

#### Setting up API User Authentication

```
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWError, jwt
from passlib.contex import CryptoContext

SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

db = {
	"tim":{
		"username":"Tejha",
		"full_name":"Tejha N",
		"email":"lol@gmail.com",
		"hashed_password":"",
		"disabled":False      #incase the api got expired
	}
}

class Token(BaseModel):
	access_token: str
	token_type: str

class TokenData(BaseModel):
	username: str or None = None

class User(BaseModel):
	username:str
	email: str or None = None
	full_name: str or None = None
	disabled: bool or None = None

class UserDB(User):
	hashed_password: str

pwd_context = CryptoContext(schemes=["bcrypt], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_password(plain_password, hashed_password):
	return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
	return pwd_context.hash(password)

def get_user(db, username: str):
	if username in db:
		user_data = db[username]
		return UserInDB(**user_data)

def authenticate_user(db, username: str, password: str):
	user = get_user(db, username)
	if not user:
		return False
	if not verify_password(password, user.hashed_password):
		return False
	return user

def create_access_token(data: dict, expires_delta: timedelta or None = None):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=15)
		
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
	return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_schema)):
	credential_exception = HTTPException((status_code=status.HTTP_401_AUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"}))
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		username: str = payload.get("sub")
		if username is None:
			raise credential_exception
		token_data = TokenData(username=username)
		
	except JWTError:
		return credential_exception

	user = get_user(db, username=token_data.username)
	if user is None:
		raise credential_exception
	
	return user

async def get_current_active_user(cuurent_user: UserInDB = Depends(get_current_user)):
	if current_user.disabled:
		raise HTTPException(status_code=400, detail="Inactive user)

	return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
	user = authenticate_user(db, form_data.username, form_data.password)
	if not user:
		raise HTTPException(status_code=status.HTTP_401_AUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
	access_token = create_token(data={"sub":username}, expires_delta=access_token_expires)
	return {"access_token":access_token, "token_type":"bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
	return current_user

@app.get("/users/me/items")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
	return [{"item_id":1,"owner":current_user}]
```

- In terminal, to generate the secret key type ```openssl rand -hex 32```