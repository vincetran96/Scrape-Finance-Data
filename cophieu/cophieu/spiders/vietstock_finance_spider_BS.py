import scrapy
import sys
import json
import traceback
import os

FINANCE_PATH = "balance_sheets/"

INDENT = 2


def make_directory(path, filename):
    path_to_file = path + filename
    if not os.path.exists (path_to_file):
        os.makedirs (os.path.dirname (path_to_file), exist_ok=True)
    return path_to_file


def handle_error(response):
    exc_type, exc_value, exc_traceback = sys.exc_info ()
    err_details = repr (traceback.format_exception (exc_type, exc_value, exc_traceback))
    error_dict = dict (error_Name=err_details, ticker=response.meta["ticker"], page=response.meta["page_n"])
    return error_dict


def extract_tickers(tickerfile):
    tickers_list = []
    with open (tickerfile, encoding="utf-8") as jsonfile:
        text = json.load (jsonfile)
        for line in text:
            ticker = line["stockname"]
            if ticker != "000001.SS" and ticker.find ("^") == -1:
                tickers_list.append (line["stockname"])
        return tickers_list


def get_quarter_data(response, account, section, i, quarter_dict):
    quarter_data = response.xpath ("//td[contains(., $account)]/parent::tr/td/descendant-or-self::*\
                                    [@class='rpt_chart']/text()", account=account)\
                                    .extract_first ().replace (".00", "").split (",")[i]
    try:
        quarter_dict[section][account] = int (quarter_data)
    except:
        quarter_dict[section][account] = "N/A"


ASSETS = ["SHORT-TERM ASSETS",
          "Cash and cash equivalents",
          "Cash",
          "Cash equivalents",
          "Short-term financial investments",
          "Available for sale securities",
          "Provision for diminution in value of available for sale securities (*)",
          "Held to maturity investments",
          "Short-term receivables",
          "Short-term trade accounts receivable",
          "Short-term prepayments to suppliers",
          "Short-term inter-company receivables",
          "Construction contract progress receipts due from customers",
          "Short-term loan receivables",
          "Other short-term receivables",
          "Provision for short-term doubtful debts (*)",
          "Assets awaiting resolution",
          "Inventories",
          "Inventories",
          "Provision for decline in value of inventories",
          "Other short-term assets",
          "Short-term prepayments",
          "Value added tax to be reclaimed",
          "Taxes and other receivables from state authorities",
          "Government bonds",
          "Other short-term assets",
          "LONG-TERM ASSETS",
          "Long-term receivables",
          "Long-term trade receivables",
          "Long-term prepayments to suppliers",
          "Capital at inter-company",
          "Long-term inter-company receivables",
          "Long-term loan receivables",
          "Other long-term receivables",
          "Provision for long-term doubtful debts",
          "Fixed assets",
          "Tangible fixed assets",
          "Cost",
          "Accumulated depreciation",
          "Financial leased fixed assets",
          "Cost",
          "Accumulated depreciation",
          "Intangible fixed assets",
          "Cost",
          "Accumulated depreciation",
          "Investment properties",
          "Cost",
          "Accumulated depreciation",
          "Long-term assets in progress",
          "Long-term production in progress",
          "Construction in progress",
          "Long-term financial investments",
          "Investments in subsidiaries",
          "Investments in associates, joint-ventures",
          "Investments in other entities",
          "Provision for diminution in value of long-term investments",
          "Held to maturity investments",
          "Other long-term investments",
          "Other long-term assets",
          "Long-term prepayments",
          "Deferred income tax assets",
          "Long-term equipment, supplies, spare parts",
          "Other long-term assets",
          "Goodwill",
          "TOTAL ASSETS"
          ]

LIABILITIES = ["LIABILITIES",
               "Short -term liabilities",
               "Short-term trade accounts payable",
               "Short-term advances from customers",
               "Taxes and other payables to state authorities",
               "Payable to employees",
               "Short-term acrrued expenses",
               "Short-term inter-company payables",
               "Construction contract progress payments due to suppliers",
               "Short-term unearned revenue",
               "Other short-term payables",
               "Short-term borrowings and financial leases",
               "Provision for short-term liabilities",
               "Bonus and welfare fund",
               "Price stabilization fund",
               "Government bonds",
               "Long-term liabilities",
               "Long-term trade payables",
               "Long-term advances from customers",
               "Long-term acrrued expenses",
               "Inter-company payables on business capital",
               "Long-term inter-company payables",
               "Long-term unearned revenue",
               "Other long-term liabilities",
               "Long-term borrowings and financial leases",
               "Convertible bonds",
               "Preferred stock (Debts)",
               "Deferred income tax liabilities",
               "Provision for long-term liabilities",
               "Fund for technology development",
               "Provision for severance allowances"
               ]

EQUITY = ["OWNER'S EQUITY",
          "Owner's equity",
          "Owner's capital",
          "Common stock with voting right",
          "Preferred stock",
          "Share premium",
          "Convertible bond option",
          "Other capital of owners",
          "Treasury shares",
          "Assets revaluation differences",
          "Foreign exchange differences",
          "Investment and development fund",
          "Fund to support corporate restructuring",
          "Other funds from owner's equity",
          "Undistributed earnings after tax",
          "Accumulated retained earning at the end of the previous period",
          "Undistributed earnings in this period",
          "Reserves for investment in construction",
          "Minority's interest",
          "Financial reserves",
          "Other resources and funds",
          "Subsidized not-for-profit funds",
          "Funds invested in fixed assets",
          "MINORITY'S INTEREST",
          "TOTAL OWNER'S EQUITY AND LIABILITIES"
          ]

# DATA TIME-FRAME RANGES FROM 2016 TO 2008
N = [1, 2, 3, 4, 5, 6, 7, 8, 9]


class FinanceSpider (scrapy.Spider):
    name = "vietstock_finance_BS"
    ticker_dict = {}

    def start_requests(self):
        tickers_list = extract_tickers("tickerz.json")

        for ticker in tickers_list:
            self.ticker_dict[ticker] = {"ticker": ticker, "data": []}
            for page_n in reversed(N):
                # page_n is a page in VStock, includes 4 quarters
                request = scrapy.Request ('http://finance.vietstock.vn/Controls/Report/Data/GetReport.ashx?rptType=CDKT\
                                         &scode={0}&bizType=1&rptUnit=1000000&rptTermTypeID=2&page={1}'
                                          .format (ticker, page_n),
                                          callback=self.parse,
                                          cookies={'finance_lang': 'en-US'})
                request.meta["ticker"] = ticker
                request.meta["page_n"] = page_n
                yield request

                # PROCESS ALL REQUESTS BEFORE WRITING EACH TO FILE

        # IF THIS DOES NOT RUN AGAIN, HAVE TO USE PIPELINES
        for ticker, data in self.ticker_dict.items():
            filename = "Vietstock_BS_data_{0}.json".format(ticker)
            file_path = make_directory (FINANCE_PATH, filename)
            with open (file_path, 'w') as fp:
                json.dump (self.ticker_dict[ticker], fp, indent=INDENT)

    def parse(self, response):
        result = []

        if not response.xpath ("//table"):
            return
        else:
            try:
                for i, quarter in enumerate (response.xpath ("//td[@class = 'BR_colHeader_Time']/text()").extract ()):
                    quarter_dict = {
                        "quarter": quarter,
                        "assets": {},
                        "liabilities": {},
                        "equity": {}
                    }
                    for account in ASSETS:
                        get_quarter_data (response, account=account, section="assets", i=i,
                                          quarter_dict=quarter_dict)
                    for account in LIABILITIES:
                        get_quarter_data (response, account=account, section="liabilities", i=i,
                                          quarter_dict=quarter_dict)
                    for account in EQUITY:
                        get_quarter_data (response, account=account, section="equity", i=i,
                                          quarter_dict=quarter_dict)

                    result.append (quarter_dict)

                self.ticker_dict[response.meta["ticker"]]["data"] += result

            except:
                error_data = handle_error (response)
                with open ("Vietstock_error_{0}.json".format (response.meta["ticker"]), "w") as error_file:
                    json.dump (error_data, error_file, indent=INDENT)
