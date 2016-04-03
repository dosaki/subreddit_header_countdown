# Subreddit Header Countdown
Update your subreddit header with a countdown!


# Run
Change the contents of `settings.cfg` to suit your needs. Then run

```bash
python header_img_text.py
```

## Add it to Crontab
```bash
crontab -e
```
Use one of these below
```bash
* * * * * /usr/bin/python /path/to/script/header_img_text.py # every minute
*/30 * * * * /usr/bin/python /path/to/script/header_img_text.py # every half-hour
0 * * * * /usr/bin/python /path/to/script/header_img_text.py # every hour
0 0 * * * /usr/bin/python /path/to/script/header_img_text.py # every day
```


# Setup dev environment
to setup with conda:
```bash
conda env create
```

to setup with pip / python 2.7.11:
```bash
pip install pillow
pip install praw
```

# Test
to test:
```bash
cd subreddit_header_countdown
python test/test_img_text.py
```
