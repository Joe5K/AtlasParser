# AtlasParser

Parser as test assignment to Atlas company

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```

## Usage

```bash
cd WebApp
set FLASK_APP=app.py
flask run
```

You can parse `idnes.cz` news by choosing number of articles to download and clicking Refresh button. At the each article you can see `Details` button which will redirect you to page with all the details and comments.

At the top right corner there is the `Filter` button. You can find article with most comments and most common words there.

Alterantively, you can run parser from terminal.
```bash
cd Parser
python run.py 5 #5 is the optional parameter for number of articles 
```

## Dependencies
You need to run MongoDB server on ```mongodb://localhost:27017/```

## License
idk