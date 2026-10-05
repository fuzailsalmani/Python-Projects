# Customer Feedback Analysis and Automated Response

Imarticus Data Science Internship - Assessment (Python Foundations & Gen AI)

The project was run from start to finish on real data: the Furniture reviews were downloaded from Kaggle, analysed, and three emails were written with the Gemini API. The analysis part gives the same result every time for the same file and row limit. The wording of the emails changes from run to run.

## Problem

A retail company gets thousands of customer reviews every week. The support team reads them one by one to find the angry ones and writes each apology email by hand. This takes a lot of time.

## What this project does

1. Downloads a set of Amazon product reviews from Kaggle.
2. Cleans the data with pandas.
3. Picks out the critical reviews (1 and 2 stars) using simple Python rules. No machine learning is used here.
4. Finds the most common complaint words.
5. Picks the 3 most critical and detailed reviews using a point system.
6. Asks Google Gemini to write a short, polite apology email for each of the 3 reviews.

## Dataset

- Source: [Amazon US Customer Reviews Dataset](https://www.kaggle.com/datasets/cynthiarempel/amazon-us-customer-reviews-dataset) on Kaggle. It has one file per product category.
- Default file: `amazon_reviews_us_Furniture_v1_00.tsv`. Furniture reviews have typical shop complaints (broken, late, missing parts), and the file is not too big.
- To use another category, pass `--category`, for example `--category Software_v1_00`. The category is the part of the file name between `amazon_reviews_us_` and `.tsv`.

### How the data is loaded

- `kagglehub` downloads only the one category file, not the whole dataset, and keeps a local copy. You do not download or rename anything, and no file path is written in the code.
- Kaggle may send the file as a zip even though the name ends in `.tsv`. The code checks the real file type and reads zip or gzip files directly.
- The header is checked first. The file must have these 12 columns: `marketplace`, `customer_id`, `review_id`, `product_id`, `product_title`, `product_category`, `star_rating`, `helpful_votes`, `total_votes`, `review_headline`, `review_body`, `review_date`. If some are missing, the program stops and lists them.
- Only these columns and the first 200,000 rows (`--max-rows`) are read, so the computer's memory is not filled by a huge file.

Loading from code keeps the run repeatable. Everyone gets the same file from the same place, and there is no manual step that can go wrong.

### Licence - please check

This dataset is not free to use for anything. The Kaggle page says the licence is "Other (specified in description)", and Amazon's terms allow the data to be used for academic research. Commercial use or republishing is not allowed. An internship assessment may or may not count as academic research, so please confirm with your instructor before you submit or publish anything that contains review text. That includes this repository, the notebook outputs and the CSV file.

## Data cleaning

The original `review_headline` and `review_body` columns are never changed. Three new columns are added:

- `review_headline_readable` and `review_body_readable`: HTML tags removed, HTML codes decoded, extra spaces removed. The wording stays the same. These are used for display and for the email prompt.
- `review_text_clean`: lower case, no URLs, no special characters. Used only for the analysis.

| Problem | What is done |
|---|---|
| Missing `review_id` | Row is dropped |
| Duplicate `review_id` | First one is kept |
| Missing or invalid `star_rating` (not 1 to 5) | Row is dropped |
| Missing or invalid vote counts | Set to 0 |
| Invalid `review_date` | Set to empty date, row is kept (date is not used) |
| Missing headline or body | Replaced with empty text. Rows with no text at all are dropped |
| Missing `product_title` or `product_id` | Replaced with `Unknown product` or `UNKNOWN` |
| HTML tags like `<br />` and codes like `&#34;` | Removed or decoded |
| URLs | Removed from the analysis text only |
| Capital letters, punctuation, symbols, extra spaces | Cleaned in the analysis text only |
| Short forms like `didn't` | Expanded to `did not`, so "did not work" can still be found |

The program prints how many rows each step changed.

## Critical reviews

A review is critical if `star_rating <= 2`. This is a normal pandas filter.

## Complaint keywords

- The cleaned text (headline and body) of each critical review is split into words of 3 or more letters.
- Common words are removed with a stop-word list. The list has ordinary words (the, and, with), general shopping words (product, item, bought, amazon) and praise words (great, good, love). Words like "not" and "never" are also removed, because on their own they mean little.
- `collections.Counter` counts the remaining words. The table shows how many times each word appears and in how many reviews. Counting reviews separately stops one very long review from dominating the list.
- Because "not" is removed from single words, two more views are shown: common complaint phrases (like `stopped working`, `did not work`, `waste of money`) and complaint themes (7 groups such as breakage, poor quality, delivery, customer service).
- The stop words, phrases and themes are at the top of `customer_feedback_analysis.py` and can be changed.

## Choosing the top 3 reviews

A review can be chosen only if it is critical, has at least 30 words and contains at least one complaint term. Each such review gets up to 100 points:

| Part | Points | Rule |
|---|---|---|
| Rating | 30 or 15 | 1 star gives 30, 2 stars give 15 |
| Length | up to 20 | More words give more points, full points at 150 words |
| Complaint density | up to 20 | Share of words that are complaint terms, full points at 10% |
| Specific problems | up to 15 | 5 points for each different complaint theme (max 3 themes) |
| Helpful votes | up to 15 | More votes give more points, full points at 10 votes |

If two reviews have the same score, the one with more helpful votes wins, then the smaller `review_id`. Reviews with identical text are skipped, and the 3 reviews come from 3 different products when possible. The 3 chosen reviews and their points are printed before anything is sent to Gemini. No machine learning, sentiment model or AI is used for filtering, keywords or selection.

## Email writing with Gemini

- Gemini is used only for writing the emails. Nothing else uses AI.
- The code uses the current Google SDK, `google-genai`. The link in the assignment shows the older SDK, which has been replaced.
- One request is made for each selected review, so 3 requests in total.
- The prompt is in the code (`SYSTEM_INSTRUCTION` and `USER_PROMPT_TEMPLATE`) and is printed when the program runs. It asks the model to act as a customer support agent and write an email with a subject line, a greeting, a sincere apology that mentions the real problems in the review, one next step, and 90 to 150 words. It must not invent order numbers, refund amounts, policies, company names or promises, and it must not say the email was written by an AI. The review text is placed between quotes and the model is told to treat it only as feedback.
- The dataset has no customer names, so each email starts with "Dear Customer," and ends with "Customer Support Team".
- Default model: `gemini-flash-latest` (Google's name for its current Flash model). Older versions such as `gemini-2.5-flash` are being phased out, so this name is safer. To use a different model, set `GEMINI_MODEL` (see the [model list](https://ai.google.dev/gemini-api/docs/models)). The model name is printed and saved in the CSV.

## API keys

**Gemini key.** Create one at <https://aistudio.google.com/apikey>.

- In the notebook, run the "Gemini API key" cell. It asks for the key in a hidden box and keeps it only while the notebook is open. It is not saved in the notebook.
- Or copy `.env.example` to a file named `.env` in the same folder as `customer_feedback_analysis.py` and write this line in it:
  ```
  GEMINI_API_KEY=your_real_key_here
  ```
  You can also set `GEMINI_API_KEY` as a normal environment variable.

The key is never written in the code. `.env` is listed in `.gitignore`. Do not put your real key in `.env.example`, because that file is meant to be shared.

**Kaggle login.** Normally the public dataset downloads without any setup. If Kaggle asks for credentials, create a token at <https://www.kaggle.com/settings> (API section) and add `KAGGLE_USERNAME` and `KAGGLE_KEY` (or `KAGGLE_API_TOKEN`) to `.env`, or put `kaggle.json` in the `.kaggle` folder in your home directory.

## Installation

Python 3.9 or newer is needed (tested on Python 3.13).

- Notebook: nothing to install by hand. The first code cell runs `%pip install` for all libraries. Keep the notebook in the same folder as `customer_feedback_analysis.py`.
- Script:
  ```bash
  python -m venv .venv
  # Windows: .venv\Scripts\activate      Mac/Linux: source .venv/bin/activate
  pip install -r requirements.txt
  ```
  `ipykernel` in `requirements.txt` is only needed to run the notebook.

## How to run

**Notebook (recommended).** Open `customer_feedback_analysis.ipynb`, choose a Python kernel and run the cells from top to bottom: the setup cell first, then the API key cell. The tables and the 3 emails are shown as Markdown. Save the notebook after it has run, so the outputs are stored in the file.

If Gemini is busy (error 503) or the model is not available, use the optional cell "choose a model / test the connection", pick another model, and run only the generation cells again.

**Script.**
```bash
python customer_feedback_analysis.py
```
Options:
```bash
python customer_feedback_analysis.py --category Software_v1_00 --max-rows 100000
python customer_feedback_analysis.py --skip-genai     # analysis only, no Gemini call
python customer_feedback_analysis.py --output outputs/my_emails.csv
```

The first run downloads the file from Kaggle, which can take some time. Later runs use the saved copy.

## What the output shows

1. Dataset information (source, file, columns checked, rows loaded)
2. Missing values in the raw data
3. Cleaning summary (rows changed in each step, rows before and after)
4. Number of critical reviews, with the split between 1 and 2 stars
5. Top complaint keywords, phrases and themes
6. The scoring rules
7. The 3 selected reviews with their points
8. The Gemini prompt
9. The 3 emails, each in its own block:

```
======================================================================
GENERATED EMAIL 1
Product: ...
Rating: ...
Customer Review:
...
AI-Generated Customer Response:
...
======================================================================
```

`outputs/generated_emails.csv` has one row per email: review details, score, model, `status` (`generated`, `failed` or `skipped`), `error` and `generated_email`.

## Error handling

If something goes wrong, the program prints a clear message. It never makes up an email: a failed email is marked `failed` or `skipped` on screen and in the CSV.

| Situation | What happens |
|---|---|
| `GEMINI_API_KEY` missing or still the placeholder | Says where it looked for `.env`, makes no API call. The analysis still runs |
| Invalid key (HTTP 400 "API key not valid", 401, 403) | Clear message, no more calls |
| Quota used up (HTTP 429) | Says the quota is exceeded and you must wait for the reset or use a project with a higher quota. No retry, no more calls |
| Model not found (HTTP 404) | Tells you to set `GEMINI_MODEL`, no more calls |
| Server problem (5xx, for example 503 "high demand") or network problem | Up to 2 retries after 5 and 10 seconds, then a message with the HTTP code, and no more calls. Wait and run again, or choose another model |
| Empty, blocked or incomplete answer (no `Subject:` line or too short) | Marked as failed, not retried |
| Missing columns in the dataset file | Lists the missing and the found columns |
| Kaggle download problem | Shows the reason and what to check |

When everything works, the program makes exactly 3 generation requests.

## Files

```
customer_feedback_analysis/
├── customer_feedback_analysis.py    # the code (also run from the command line)
├── customer_feedback_analysis.ipynb # the same steps as a notebook
├── README.md
├── requirements.txt
├── .env.example                     # template, copy it to .env
├── .gitignore                       # keeps .env out of git
└── outputs/
    └── generated_emails.csv         # created when the project runs
```

## Limitations

- Only the first `--max-rows` rows of one category are used. The results describe this sample, not all Amazon reviews, and the first rows of a file are not a random sample.
- The reviews are from 1995 to 2015 and are not a real company's support tickets.
- The keyword search uses hand-made lists. It does not understand sarcasm or spelling mistakes, and a word like `late` or `return` can sometimes be used in a non-complaint way.
- Characters outside English letters and numbers (other languages, emoji) are removed from the analysis text.
- The emails are drafts and a person should read them before sending. The model does not know the customer's order or the company's real policies, and it can misread a review. For example, it may say "our previous communication fell short" when the earlier reply actually came from the manufacturer, or it may not mention a personal event the customer wrote about. The prompt lowers these mistakes but cannot remove them.
- The reviews are real people's texts and can include personal details. They are used only for this exercise and should not be republished.
- The default Gemini model name points to whatever Google currently offers. Set `GEMINI_MODEL` to fix one model. Free quotas and model availability change over time.
- The file names `amazon_reviews_us_<category>.tsv` come from the dataset's Kaggle page. If Kaggle renames them, the download fails with a message to check the category name.

## Assignment checklist

| Requirement from the assignment | Where it is done | Status |
|---|---|---|
| Get a review dataset from Kaggle with text and 1-5 star ratings | `download_category_file()` downloads a category file of the Amazon US reviews with `kagglehub` | Done and run |
| Load the data with pandas | `load_reviews()` (`pd.read_csv`, header check, needed columns only, row limit) | Done |
| Handle missing values | `summarize_missing_values()` shows them, `clean_reviews()` drops or fills them (see the cleaning table) | Done |
| Clean the text (special characters, same case) | `make_readable()` and `clean_review_text()`. Original text is kept | Done |
| Filter critical reviews without machine learning | `filter_critical_reviews()` with `star_rating <= 2` | Done |
| Function for the most common complaint keywords (string methods or `Counter`) | `extract_keywords()` with `Counter` and a stop-word list, plus `count_complaint_phrases()` and `count_complaint_themes()` | Done |
| Pick 3 of the most critical, detailed reviews | `score_reviews()` and `select_top_reviews()` | Done |
| Script that sends each review to a Gen AI API | `generate_email()` and `generate_emails()` use Google Gemini, one request per review | Done and run |
| Prompt as a support agent: short, personal, empathetic apology that covers the specific complaints | `SYSTEM_INSTRUCTION` and `USER_PROMPT_TEMPLATE` | Done |
| Jupyter Notebook with clear, commented code | `customer_feedback_analysis.ipynb` | Done |
| Markdown cells with the insights and the 3 emails | Notebook cells show them as Markdown after running | Save the notebook after running it |
| README with cleaning, rules, how to run and API keys | This file | Done |
| No machine learning for filtering and insights | No ML model of any kind is used before the Gemini step | Done |
| No API key in the code, `.env` ignored | `os.getenv("GEMINI_API_KEY")`, `.env.example`, `.gitignore` | Done |
| Handle API errors and never fake an email | See the error table above | Done |
| Dataset licence | See the Licence section | Check with your instructor |

## Dataset and licence note

Dataset: Amazon US Customer Reviews Dataset (Amazon.com), shared on Kaggle by Cynthia Rempel. Kaggle licence: "Other (specified in description)". The terms behind it allow use for academic research. Do not republish the data, including long parts of it in this repository or in the notebook outputs, and ask your instructor if your use is allowed.
