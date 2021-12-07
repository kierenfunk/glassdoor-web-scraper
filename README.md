# Glassdoor Web Scraper
> Web scraper for glassdoor job listings platform with python.

Inspiration from [kelvinxuande](https://github.com/kelvinxuande/glassdoor-scraper).

Works without sign-in, user provides a job role and a location and the script returns output in json or csv format.
Location can be either a city or a country, the most likely match will be taken from glassdoor's matching url.
Python script interacts with glassdoor's graphql backend to return results.

## Get Started

### Requirements

- Python 3
- `pipenv`

### Installation

With `pipenv`
```bash
pipenv install
pipenv shell
python src/main.py
```

## Usage

## Testing

For linting:
```bash
bash scripts/lint.sh
```

To run all tests
```bash
pytest --cov
```