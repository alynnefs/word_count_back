[![Build Status](https://app.travis-ci.com/alynnefs/word_count_back.svg?token=hqbqCmyo5nLQPrVtRR4v&branch=main)](https://app.travis-ci.com/alynnefs/word_count_back)

# Word Count - Back

The project consists of getting a text passed by the front end and counting how many words it has.

## Running with Docker

To create the docker image, run the following command in the project root:

```
docker image build -t cw_back .
```

The result should be

![](https://i.imgur.com/7aUHiW2.png)

After created, run the container with:


```
docker container run -d -p 5000:5000 cw_back
```

To see if the container is running, just use the `docker container ls` command. The output should look something like this:
    
![](https://i.imgur.com/4EOHsSQ.png)


## Running locally

### Specifications used in development

Operating System: Ubuntu 20.04.5 LTS
NPM: 9.2.0
Docker: 20.10.21, build baeda1f
Vue/cli: 5.0.8


### How to run

To create the virtual environment, run:

```
virtualenv --python=python3.9 .venv
```

To activate it:

```
source .venv/bin/activate
```

To install the dependencies:

```
pip install -r requirements.txt
```

With everything installed, simply run the project in the root folder:

```
flask --app app/main run
```

### Using the front

> The front-end of this project and how to run it can be seen [at this link](https://github.com/alynnefs/word_count_front).

In the browser, enter the link http://127.0.0.1:8080. The last IP number may change.

Use the text box to count the number of words of the text you want.

![](https://i.imgur.com/Co3Mwu7.png)

You can add more than one space between words, either at the end or at the beginning. This will not change the number of words.

![](https://i.imgur.com/x6lctZH.png)



### Using cURL

Examples of requests to be made on the terminal, with the container running:

```
curl 127.0.0.1:5000/count/apple
curl 127.0.0.1:5000/count/an%20apple # %20 is because of the space between words
```

## Tests

### Testing at Travis CI

To see the tests that were run on Travis, just click [on this link](https://app.travis-ci.com/github/alynnefs/word_count_back) or the button at the top of this file. Whenever a commit is added to the main branch, Travis will run the tests again. In it you can see the history of the test execution:

![](https://i.imgur.com/OPAoaIM.png)

If there is an error, it tells you what it is.


### Running the tests locally

Considering that you are in the virtual environment and have the dependencies installed, just run:

```
pytest tests/*
```

The result will be:

![](https://i.imgur.com/UXkgZar.png)


This command will run all the tests on all the files that are inside this folder. If you want to run only one of the tests, you can use this command as an example:

```
pytest tests/tests_count_the_words.py::test_many_words
```

The result will be:

![](https://i.imgur.com/tt6t7pg.png)


### Test Coverage

To check the test coverage, just run the `coverage run -m pytest tests/*` command from the project root. It will create a folder called `htmlcov` and inside it you just need to open the `index.html` file. The page will look like this:

![](https://i.imgur.com/HnghuOB.png)


If you click on any of the files, you can see which lines are covered.

![](https://i.imgur.com/om0f08w.png)
