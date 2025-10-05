# Options Trading Assistant

<div align="right">
	[<a href="README.md">中文</a> | English(Current)</a>]
</div>

## 1 Introduction

### 1.1 Purpose of Writing

This chapter is the detailed design specification for the options trading application. The overall design section presents the software requirements, environment, and structure; the module design section describes the relationships among software modules and the specific implementation of each module; the user guide section provides detailed instructions on how to use the software.

### 1.2 Background

Software name: Options Trading Assistant

Theoretical basis: Black–Scholes (B–S) option pricing model and the warrant trading model based on the B–S option pricing model.

### 1.3 Definitions

* **Stock options**: Option contracts with index funds as the underlying assets. They follow the stock option quotes displayed on the *Sina Finance → Options → Stock Options* page (link: `https://stock.finance.sina.com.cn/option/quotes.html`).

* **Commodity options**: Option contracts with physical goods as the underlying assets. They follow the commodity option quotes displayed on the *Sina Finance → Options → Commodity Options* page (link: `https://stock.finance.sina.com.cn/futures/view/optionsDP.php`).

* **T-shaped quotation**: In a T-shaped quotation table, the middle column is the strike price. Using the strike price as the axis, the left side lists call option quotes and the right side lists put option quotes.

* **Categorized quotation**: In a categorized quotation table, each row represents the quotation for one option contract.

* **Dividend adjustment**: For stock options, after the underlying asset distributes dividends, certain contract terms of the original option will be adjusted. Option contracts that have undergone dividend adjustment will add a dividend adjustment marker to the contract short name and strike price. “A” indicates one dividend adjustment.

### 1.4 File List
`main.py`: main module  
`widget.py`: widget module  
`k_line.py`: k_line module  
`solution.py`: solution module  
`LSTM.py`: LSTM module  
`crawler.py`: crawler module  
`logo.ico`: application icon  

## 2 Overall Design

### 2.1 Requirement Overview

Implement the B–S option pricing model and the warrant trading model based on it as described in Sections 2 and 3 of this document, and use them to provide information support for investors engaged in real options trading, assisting investors in making option trading decisions.

* For the most common option varieties on the market, the application can browse real-time market quotes. Investors can retrieve the required option quote information in a variety of ways and use the application to perform in-depth analysis.

* For a specific option contract, the application can efficiently calculate various indicators, clearly display detailed information, and draw charts such as intraday lines and candlestick (K-line) charts to reflect real-time price dynamics.

* For investors without clear targets, the application can use the value potential model to compute the value potential of each option contract, recommend suitable contracts, and provide decision support for option trading.

### 2.2 Operating Environment

The development environment of the application is Python 3.8 and TensorFlow 2.8.0. Other major libraries invoked include PyQt5, pyqtgraph, requests, sklearn, etc.

The runtime environment of the application is Windows XP and later versions of the operating system, with higher screen resolutions recommended.

### 2.3 Software Structure

Figure 1 Software structure diagram

![image](https://github.com/baoyunfan0101/OptionsTradingAssistant/blob/main/static/1.png)

The Options Trading Assistant software is divided into four parts: **Stock Options**, **Commodity Options**, **Contract Analysis**, and **Value Potential Ranking**. Among them, **Stock Options** include *Categorized Quotation* and *T-shaped Quotation*; **Commodity Options** include *T-shaped Quotation*, which display real-time quotation tables for the corresponding types of option contracts. **Contract Analysis** includes *Contract Details* and *K-line Data*; *Contract Details* display the basic information and calculated results of various metrics for a specific option contract, and *K-line Data* display intraday, daily, weekly, and monthly charts showing real-time trading conditions of a specific option contract. **Value Potential Ranking** calculates the value potential of each option contract according to the warrant trading model, and—based on investor filter conditions—provides a ranking table of option contracts that meet the criteria.

## 3 Module Design

### 3.1 Hierarchical Division

Table 1 Module hierarchical division

| Level | Module Name |
|------|-----------|
| **UI Layer** | main module, widget module, k_line module |
| **Logic Layer** | solution module, LSTM module |
| **Data Layer** | crawler module |

The application consists of a UI layer, a logic layer, and a data layer, as shown in Table 1. The UI layer handles the display of application windows and controls, as well as responses to events, and includes the three modules `main`, `widget`, and `k_line`. The logic layer accepts data requests from the UI layer, calls the data layer to obtain data, performs computations and processing, and returns the results to the UI layer; it includes the two modules `solution` and `LSTM`. The data layer collects the required data from the Internet and returns the data to the logic layer; it includes the single module `crawler`.

### 3.2 Call Relationships

Figure 2 Module call relationship diagram

![image](https://github.com/baoyunfan0101/OptionsTradingAssistant/blob/main/static/2.png)

The application includes six modules: `main`, `widget`, `solution`, `k_line`, `crawler`, and `LSTM`. The relationship between parent and child modules is that of caller and callee, as shown in Figure 2. Each module exists independently, and cross-calls between different modules are avoided to reduce coupling between modules.

### 3.3 main Module

Figure 3 Event loop of the main module

![image](https://github.com/baoyunfan0101/OptionsTradingAssistant/blob/main/static/3.png)

The `main` module primarily imports the `sys` and `PyQt5` libraries. The module defines the window class `main_window`. When executing the `main` module, a `QApplication` object is instantiated first, and the event loop begins, as shown in Figure 3. The main application window `main_window` is instantiated, and the `widget` module is called to initialize the window. Event parameters such as clicks, mouse position movement, and window size changes are passed to the `widget` module to update the window. The mapping from events to the functions invoked when the events occur is shown in Table 2.

Table 2 Event–function mapping

| Event                         | Corresponding Function   | Function Description            | Parameter   |
|:-----------------------------|:-------------------------|:-------------------------------|:-----------|
| Adjust window size           | resizeEvent              | Resize all related controls    | Window size |
| Right-click stock options categorized quotation table | tableWidget_1_menu | Pop up the corresponding menu | Mouse position |
| Right-click stock options T-shaped quotation table  | tableWidget_2_menu | Pop up the corresponding menu | Mouse position |
| Right-click commodity options T-shaped quotation table | tableWidget_3_menu | Pop up the corresponding menu | Mouse position |
| Right-click value potential ranking table       | tableWidget_rank_menu | Pop up the corresponding menu | Mouse position |

### 3.4 widget Module

The `widget` module primarily imports the `PyQt5` library. The module defines the `Ui_Form` class, which includes methods for initializing and updating the various controls in the window and is the main module for the user interaction interface. The `widget` module calls the `k_line` module to draw the charts required in the window and calls the `solution` module to obtain all the data needed for display.

The `widget` module realizes switching among the functional partitions and their sub-partitions mentioned in Section “2.3 Software Structure” above by instantiating a `QTabWidget` object. For each functional partition and its sub-partitions, a `QWidget` object is instantiated to represent it. Their correspondences are shown in Table 3.

Table 3 Partition objects ↔ functional partitions

| Partition Object | Corresponding Functional Partition | Parent |
|:-----------|:----------------------|:-------|
| tab_1      | Stock Options         | \     |
| tab_11     | Stock Options – Categorized Quotation | tab_1  |
| tab_12     | Stock Options – T-shaped Quotation    | tab_1  |
| tab_2      | Commodity Options     | \     |
| tab_21     | Commodity Options – T-shaped Quotation | tab_2  |
| tab_3      | Contract Analysis     | \     |
| tab_31     | Contract Analysis – Contract Details | tab_3  |
| tab_32     | Contract Analysis – K-line Data      | tab_3  |
| tab_hour   | Contract Analysis – K-line Data – Intraday | tab_32 |
| tab_d      | Contract Analysis – K-line Data – Daily    | tab_32 |
| tab_w      | Contract Analysis – K-line Data – Weekly   | tab_32 |
| tab_m      | Contract Analysis – K-line Data – Monthly  | tab_32 |
| tab_4      | Value Potential Ranking | \      |

The `widget` module displays data tables by instantiating `QTableWidget` objects. The table objects and their corresponding functions are shown in Table 4.

Table 4 Table objects ↔ functions

| Table Object      | Corresponding Function        | Parent |
|:-----------------|:------------------------------|:-------|
| tableWidget_1    | Stock options categorized quotation table | tab_11 |
| tableWidget_2    | Stock options T-shaped quotation table    | tab_12 |
| tableWidget_3    | Commodity options T-shaped quotation table | tab_21 |
| tableWidget_rank | Value potential ranking table             | tab_4  |

Other controls are not elaborated here. In the `Ui_Form` class, the function `update_{control_name}` updates the corresponding control; the function `load_{control_name}` loads the corresponding control for the first time; the function `show_{control_name}_menu` displays the menu for the corresponding control. These functions are connected as slots to the corresponding control signals to respond to interaction requests.

### 3.5 k_line Module

The `k_line` module primarily imports the `PyQt5` and `pyqtgraph` libraries and completes the drawing of various graphics required by the window. The module defines five graphics classes inherited from `GraphicsObject`: `candle_stick`, `volume`, `fold_line`, `volume_hour`, and `MACD_line`, which draw the basic candlestick (K-line) chart, trading volume bar chart, intraday line chart, intraday trading volume bar chart, and MACD indicator curve, respectively. It also defines five classes `k_line`, `v_bar`, `hour_line`, `fold_line`, and `MACD` to provide interfaces for external calls.

When calling the `k_line` module from the outside, charts are drawn by instantiating the five classes `k_line`, `v_bar`, `hour_line`, `fold_line`, and `MACD`. The functions of these five classes and the parameters of their constructors are shown in Table 5.

Table 5 Class names, functions, and parameters

| Class Name | Function                    | Param 1 | Meaning                 | Param 2 | Meaning            | Param 3 | Meaning            |
|:----------|:-----------------------------|:--------|:------------------------|:--------|:-------------------|:--------|:-------------------|
| k_line    | Draw the basic candlestick (K-line) chart | data    | Basic K-line data       | label_x | External x-axis label | label_y | External y-axis label |
| v_bar     | Draw the trading volume bar chart        | data    | Volume data             | \      | \                 | \      | \                 |
| hour_line | Draw the intraday line chart             | data    | Intraday line data      | label_x | External x-axis label | label_y | External y-axis label |
| fold_line | Draw the intraday trading volume bar chart | data  | Intraday volume data    | \      | \                 | \      | \                 |
| MACD      | Draw the MACD indicator curve            | data    | MACD indicator data     | \      | \                 | \      | \                 |

Among them, the constructors of `k_line` and `hour_line` require external x-axis and y-axis labels to implement the function of moving the labels with the mouse position and updating label contents. This function is detailed in Section “4.3 Contract Analysis” below.

### 3.6 solution Module

The `solution` module calls the `crawler` module and the `LSTM` module to obtain real-time option market data and model prediction results, respectively, completing data computation and integration, and providing all the data required by the `widget` module.

In the `solution` module, functions of the form `get_{control_name}` provide data for the corresponding controls. In the `widget` class, the corresponding functions are called to obtain the data required by the controls to load and update data.

### 3.7 LSTM Module

The `LSTM` module primarily imports libraries such as TensorFlow and scikit-learn, builds and trains an LSTM model, and applies the trained model to provide prediction results for the `solution` module. The sources of the datasets are shown in Table 6.

When the `LSTM` module is executed in the development environment, the module builds and trains LSTM models for all the stocks involved. The trained models and normalization parameters are saved in the files `{stock_code}.h5` and `{stock_code}_sc.pkl`. During application runtime, calling the function `get_VP` returns the prediction results of the model corresponding to the specified stock code; calling the function `get_all_VPs` returns the prediction results of all models.

Table 6 Stock data API parameter table

| API     | URL                                                                                                                                 | Parameter | Meaning             | Description                          |
|:--------|:------------------------------------------------------------------------------------------------------------------------------------|:---------|:--------------------|:-------------------------------------|
| Stock K-line | https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol={symbol}&datalen={datalen}&scale={scale}&ma={ma} | symbol   | Stock code          | Example: “sh510050” for SSE, 510050  |
|         |                                                                                                                                     | datalen  | Data length         | Range: [0, 1023]                     |
|         |                                                                                                                                     | scale    | Data interval (min) | Values: 5, 15, 30, 60                |
|         |                                                                                                                                     | ma       | Return moving averages or not | Default: Yes                 |

### 3.8 crawler Module

The `crawler` module primarily imports the `requests` library to collect real-time option market data. Stock option data come from the *Sina Finance → Options → Stock Options* page (link: `https://stock.finance.sina.com.cn/option/quotes.html`), and commodity option data come from the *Sina Finance → Options → Commodity Options* page (link: `https://stock.finance.sina.com.cn/futures/view/optionsDP.php`). The specific data APIs are shown in Table 7.

Table 7 Option data API parameter table

| API                                | URL                                                                                                                                                    | Parameter | Meaning                                    | Description                                                         |
|:-----------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|:----------|:-------------------------------------------|:--------------------------------------------------------------------|
| Contract codes (SSE & SZSE stock options) | https://hq.sinajs.cn/list={list}                                                                                                                       | list      | OP_{UP/DOWN}_{stock_code}{contract_month} | Example: “OP_UP_5100502306” 50ETF, call option, expires June 2023   |
| Contract codes (CFFEX stock options)      | http://stock.finance.sina.com.cn/futures/api/openapi.php/OptionService.getOptionData?type=futures&exchange=cffex&product={product}&pinzhong={pinzhong} | product   | {underlying type}                         | Underlying types: “io” CSI 300 index; “mo” CSI 1000 index; “ho” SSE 50 index |
|                                    |                                                                                                                                                        | pinzhong  | {underlying short name}{contract month}    | Example: “io2306” CSI 300 index, expires June 2023                  |
| Option contract detailed info      | https://hq.sinajs.cn/list={list}                                                                                                                       | list      | {option_type}_OP_{contract_code}          | Option types: “CON” (SSE/SZSE stock options); “P” (CFFEX stock options, commodity options) |
| Option contract analysis data      | https://hq.sinajs.cn/list={list}                                                                                                                       | list      | {option_type}_SO_{contract_code}          | Option types: “CON” (SSE/SZSE stock options); “P” (CFFEX stock options, commodity options) |
| Option daily K-line (SSE & SZSE stock options) | http://stock.finance.sina.com.cn/futures/api/jsonp_v2.php//StockOptionDaylineService.getSymbolInfo?symbol={symbol}                                   | symbol    | {contract code}                            | Obtained via the Contract codes (SSE & SZSE stock options) API      |
| Option daily K-line (CFFEX stock options & commodity options) | https://stock.finance.sina.com.cn/futures/api/jsonp.php//FutureOptionAllService.getOptionDayline?symbol={symbol}                                     | symbol    | {underlying type}{contract month}{Call/Put}{strike}({contract code}) | Example: “io2306C4000” CSI 300 index, expires June 2023, call, strike 4000 |
| Option intraday line (SSE & SZSE stock options) | https://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionDaylineService.getOptionMinline?symbol={symbol}                                 | symbol    | CON_OP_{contract_code}                     | Obtained via the Contract codes (SSE & SZSE stock options) API      |

## 4 User Guide

### 4.1 Stock Options

**(1) T-shaped Quotation**

After the software starts, it opens the Stock Options T-shaped Quotation interface by default. The table in the middle of the interface is the stock options T-shaped quotation, as shown in Figure 4. The middle of the table is the strike price; the left side shows the real-time quotes for call contracts at that strike, and the right side shows the real-time quotes for put contracts at that strike. In-the-money contracts have a red background; out-of-the-money contracts have a green background.

Investors can browse the corresponding option contracts by selecting different options in the three combo boxes at the top of the interface: “Exchange”, “Option Type”, and “Contract Month”. To the right of the combo boxes, the expiration date (remaining time) and the underlying asset for all displayed contracts are shown. When a different option is selected in a previous combo box, the options in the following combo boxes will change accordingly.

Figure 4 Stock Options T-shaped Quotation interface

![image](https://github.com/baoyunfan0101/OptionsTradingAssistant/blob/main/static/4.png)

When one row in the stock options T-shaped quotation table is selected, right-clicking will pop up a menu, as shown in Figure 5. Selecting “Refresh” updates the current T-shaped quotation table; selecting “Analyze Call Contract” navigates to the Contract Analysis interface and queries the call contract on the left side of the currently selected row; selecting “Analyze Put Contract” navigates to the Contract Analysis interface and queries the put contract on the right side of the currently selected row.

If multiple rows are selected at the same time, only the “Refresh” option will appear in the menu.

Figure 5 Stock options T-shaped quotation context menu

![image](https://github.com/baoyunfan0101/OptionsTradingAssistant/blob/main/static/5.png)

**(2) Categorized Quotation**

Click the “Categorized Quotation” tab at the top to open the Stock Options Categorized Quotation interface. The table in the middle of the interface is the categorized quotation, as shown in Figure 6. Investors can browse the corresponding option contracts by selecting different options in the “Exchange” combo box at the top of the interface.

Figure 6 Stock Options Categorized Quotation interface

![image](https://github.com/baoyunfan0101/OptionsTradingAssistant/blob/main/static/6.png)

When one row in the stock options categorized quotation table is selected, right-clicking will pop up a menu, as shown in Figure 7. Selecting “Refresh” updates the current categorized quotation table; selecting “Analyze Contract” navigates to the Contract Analysis interface and queries the contract corresponding to the currently selected row.

If multiple rows are selected at the same time, only the “Refresh” option will appear in the menu.

Figure 7 Stock options categorized quotation context menu

![image](https://github.com/baoyunfan0101/OptionsTradingAssistant/blob/main/static/7.png)

### 4.2 Commodity Options

Click the “Commodity Options” tab on the left to open the Commodity Options T-shaped Quotation interface. The table in the middle of the interface is the T-shaped quotation for commodity options, as shown in Figure 8. The middle of the table is the strike price; the left side shows the real-time quotes for call contracts at that strike, and the right side shows the real-time quotes for put contracts at that strike.

Investors can browse the corresponding option contracts by selecting different options in the two combo boxes at the top of the interface: “Option Type” and “Contract Month”. To the right of the combo boxes, the exchanges for all displayed contracts are shown. When a different option is selected in a previous combo box, the options in the following combo box will change accordingly.

Figure 8 Commodity Options T-shaped Quotation interface

![image](https://github.com/baoyunfan0101/OptionsTradingAssistant/blob/main/static/8.png)

When one row in the commodity options T-shaped quotation table is selected, right-clicking will pop up a menu, as shown in Figure 9. Selecting “Refresh” updates the current T-shaped quotation table; selecting “Analyze Call Contract” navigates to the Contract Analysis interface and queries the call contract on the left side of the currently selected row; selecting “Analyze Put Contract” navigates to the Contract Analysis interface and queries the put contract on the right side of the currently selected row.

If multiple rows are selected at the same time, only the “Refresh” option will appear in the menu.

Figure 9 Commodity options T-shaped quotation context menu

![image](https://github.com/baoyunfan0101/OptionsTradingAssistant/blob/main/static/9.png)

### 4.3 Contract Analysis

Click the “Contract Analysis” tab on the left to open the Contract Analysis interface. Enter the contract code to be queried in the “Contract Code” input box at the top, and click the “Query” button to the right of the input box to view the corresponding data in the *Contract Details* and *K-line Data* sections.

If you navigated to the Contract Analysis interface via a context menu, the corresponding contract code will be entered and queried by default. If the input contract code is empty or incorrect, a red prompt will be displayed to the right of the “Query” button, as shown in Figure 10.

Figure 10 Contract Analysis interface

![image](https://github.com/baoyunfan0101/OptionsTradingAssistant/blob/main/static/10.png)

**(1) Contract Details**

If you are not currently on the Contract Details page, click the “Contract Details” tab at the top to switch. The Contract Details page is divided into three parts: “Basic Information”, “Value Analysis”, and “Risk Analysis”, which list the contract details, as shown in Figure 11.

Figure 11 Contract Details interface

![image](https://github.com/baoyunfan0101/OptionsTradingAssistant/blob/main/static/11.png)

**(2) K-line Data**

If you are not currently on the K-line Data page, click the “K-line Data” tab at the top to switch. Investors can switch among Intraday, Daily, Weekly, and Monthly pages by clicking the “Intraday”, “Daily”, “Weekly”, and “Monthly” tabs at the top of the K-line Data section to view the corresponding charts.

On the K-line Data Intraday page, the top chart is the intraday price line, and the bottom chart is the intraday trading volume, as shown in Figure 12.

Figure 12 K-line Data – Intraday page

![image](https://github.com/baoyunfan0101/OptionsTradingAssistant/blob/main/static/12.png)

On the K-line Data Daily page, the top chart is the daily candlestick chart, the middle chart is the trading volume, and the bottom chart is the MACD indicator curve, as shown in Figure 13. The Weekly and Monthly pages are similar to the Daily page and are therefore not described again here.

Figure 13 K-line Data – Daily page

![image](https://github.com/baoyunfan0101/OptionsTradingAssistant/blob/main/static/13.png)

When the mouse moves over the Intraday line, Daily K-line, Weekly K-line, or Monthly K-line charts, a crosshair is displayed centered at the mouse position, and the x-axis and y-axis of the chart display the coordinates of the current mouse position, as shown in Figures 14 and 15.

Figure 14 K-line Data – Intraday page

![image](https://github.com/baoyunfan0101/OptionsTradingAssistant/blob/main/static/14.png)

Figure 15 K-line Data – Intraday page

![image](https://github.com/baoyunfan0101/OptionsTradingAssistant/blob/main/static/15.png)

### 4.4 Value Potential Ranking

Click the “Value Potential Ranking” tab on the left to open the Value Potential Ranking interface. The table in the middle of the interface is the value potential ranking, as shown in Figure 16. If the trade type is *Buy Options*, the table is sorted in descending order of value potential; if the trade type is *Sell Options*, the table is sorted in ascending order of value potential.

Investors can filter the contracts in the value potential ranking by modifying five filter conditions at the top of the interface: the three spin boxes “Minimum Bid Size”, “Minimum Ask Size”, and “Minimum Volume”, the “Trade Type” radio buttons, and the “Trading Preference” slider. After clicking the “Filter” button, the value potential ranking will show only the option contracts that meet the conditions.

Bid size, ask size, and volume correspond to the minimum values of “Minimum Bid Size”, “Minimum Ask Size”, and “Minimum Volume”, respectively. “Trade Type” affects the sorting of value potential. “Trading Preference” corresponds to the weights mentioned in Sections “3.2 Value Potential of Warrant Contracts” and “3.5 Analysis of the Value Potential Model” above: *short-term* represents a preference for hedging and closing positions, while *long-term* represents a preference for exercising warrants. The position of the slider affects the calculation results of value potential.

Figure 16 K-line Data – Intraday page

![image](https://github.com/baoyunfan0101/OptionsTradingAssistant/blob/main/static/16.png)

When one row in the value potential ranking table is selected, right-clicking will pop up a menu, as shown in Figure 17. Selecting “Refresh” updates the current value potential ranking table; selecting “Analyze Contract” navigates to the Contract Analysis interface and queries the contract corresponding to the currently selected row.

If multiple rows are selected at the same time, only the “Refresh” option will appear in the menu.

Figure 17 K-line Data – Intraday page

![image](https://github.com/baoyunfan0101/OptionsTradingAssistant/blob/main/static/17.png)
