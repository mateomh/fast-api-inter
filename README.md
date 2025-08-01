### Installing dependencies
Uvicorn is the web server for fast api
```
pipenv install fastpi
pipenv install "uvicorn[standard]"
```

### Installing dependecies with just pip
Create the `requirements.tx` from the pipfile
```
pipenv requirements
```


Then run
```
pip install -r requirements.txt
```

### Running a FastAPi application
```
uvicorn <file_name_no_ext>:app --reload
```

Or

```
fastapi run <file_name_w_ext>
```

[Swagger UI](http://localhost:8000/docs)