# NLPStatTest

## Flask and Electron Local GUI

My starting point is this tutorial:
	https://www.techiediaries.com/flask-electron-tutorial/
	
Their basic setup starts with:
```
git clone https://github.com/techiediaries/python-electron-app
cd python-electron-app
npm install
npm start
```
Then, to setup Flask:
```
pipenv --three
pipenv install flask 
pipenv install statsmodels
pipenv install scipy
pipenv install numpy
pipenv install matplotlib
pipenv shell # start the pipenv
npm start # Launch Electron
```

