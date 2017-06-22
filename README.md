# README #

### What is this? ###

* Scraper for financial data from cophieu68 and Vietstock.
* Including: Balance Sheets, Income Statements, Cash Flow Statements.
* Output format: `json`.

### Example of output ###
![Example.png](https://bitbucket.org/repo/Gg6aEj9/images/2645979444-Untitled.png)

### Preview of outputs ###

Visit https://drive.google.com/open?id=0B6OgUPdE214jNVV4QzNyS051Nk0 for a full view of our outputs.

### How to run? ###

* You need to have `python` and `scrapy` installed.
* At `root\cophieu\cophieu\spiders` folder, open command line.
    * Enter `scrapy crawl <spider_name>`
    * Particularly, `<spider_name>` can be:
        * `vietstock_finance_BS` for **balance sheets**.
        * `cophieu68_finance_IS` for **income statements**.
        * `cophieu68_finance_CF_indirect_v2` for **indirect cash flow statements**.
        * `cophieu68_finance_CF_direct_v2` for **direct cash flow statements**.
        
* Wait for miracle.
* Please note that you can only crawl for direct cash flow statements **after** crawling indirect cash flow statements.
* Please note that I did not split direct and indirect cash flow statements. That means outputs are in the same folder.

### Most recent significant updates ###

* Fixed a bug causing balance sheets spiders to return unordered timestamps.
* Added a spider to crawl *sector codes* and each sector's relevant tickers.
* Added 2 spiders to crawl Cash Flow data from cophieu68: direct CFs and indirect CFs.
* Added a spider to crawl Balance Sheet data from Vietstock, a more reliable source for all firms.
* Income Statements data still include banks, financial firms, insurance firms, which shall be exluded soon.
* Added scraping from Income Statements.
* Added error-logging to file.
* Fixed an error when scraping TOTAL ASSETS account.
* Initial: added Javascript to extract all tickers from raw source from cophieu68.

### What else can I say? ###

* For team NCKH FTU 2017.
