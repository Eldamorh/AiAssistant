# AiAssistant with Memory 
This is a web application, a chat with artificial intelligence. 
The server side is implemented using the Django Framework. The work of the artificial intelligence itself is the GPT-3.5-turbo API with the langchain library. 
Database for storing conversation memory - Chromadb.

# Installation
First clone this repo

`git clone https://github.com/Eldamorh/AiAssistant.git`

Install all of the requirements:

```
cd AiAssistant
pip install -r requirements.txt
```

There can be an error with installing chromadb:

`ERROR: Could not build wheels for llama-cpp-python, hnswlib, which is required to install pyproject.toml-based projects`

If you on Mac try:

`export HNSWLIB_NO_NATIVE=1`

Ubuntu:

```
sudo apt install python3-dev
sudo apt-get install build-essential -y
```

Windows:
You need to download https://visualstudio.microsoft.com/visual-cpp-build-tools/ first.

Next, navigate to "Individual components", find these two

![image](https://github.com/Eldamorh/AiAssistant/assets/75213027/cf70376c-dd5c-4f3e-85bb-c159049bf0d3)

![image](https://github.com/Eldamorh/AiAssistant/assets/75213027/648bf455-fb9f-43c1-9c07-cffa893de277)

This should fix this error. More information in these threads:
[link](https://stackoverflow.com/questions/73969269/error-could-not-build-wheels-for-hnswlib-which-is-required-to-install-pyprojec)
[link2](https://github.com/yoheinakajima/babyagi/issues/244)


Last step is to start Django Server and make migrations:
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```



