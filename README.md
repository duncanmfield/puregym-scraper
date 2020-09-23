## puregym-scraper
This script logs into the PureGym website and records the number of users in
your local gym to a file, at an interval of your choice. For example, setting
the interval to 15 minutes will record data at 0, 15, 30, and 45 minutes
past each hour.

A short script to plot the data is also included.

### PureGym set up
* You must be a member of PureGym to use this script
* On the PureGym website, ensure that your local gym is set to the
gym which you wish to scrape the number of users for

## How to use it

```bash
$ # Get the code
$ git clone https://github.com/duncanmfield/puregym-scraper.git
$ cd puregym-scraper
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$
$ # Install modules
$ pip install -r requirements.txt
$
$ # Execute
$ python main.py
$
$ # Visualise data
$ # python visualiser.py
```

NB: You will need to set your email in `config.py`. You can also tweak options such as 
the output file name and the interval between scrapes.

### Output
Data will be output to `puregym.log` by default. Example of the output:
```
2020-09-16 06:15:02 -> 36
2020-09-16 06:30:02 -> 44
```
The datetime format is YYYY-MM-DD HH:MM:SS.
