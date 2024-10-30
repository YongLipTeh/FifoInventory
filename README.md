<div align="center">

![Picture](https://github.com/user-attachments/assets/8c3d0db8-0311-4ee6-98a9-3adad5cedab1)

Track the ins and outs of inventories, outputs sales revenue, cost of good sold and gross profit.

</div>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### Author: YongLip Teh

## Dependencies:
* tkinter (built in)
* attrs (version 24.2.0)
* tkcalendar (version 1.6.1)
* tkinter_tooltip (version 3.1.0)

## Environment
For all OS users, in your terminal, go to your directory, within your python environment.
```sh
python -m venv my_env
```
Activate the environment, for Linux/macOS users:

```sh
source my_env/bin/activate
```
for Windows users:
```bat
my_env\Scripts\activate.bat
```

Download all dependencies within the environment.
```sh
pip install -r requirements.txt
```
## Ways to run the program
1. Compile it with **python** script and use it directly.
2. **Recommended**: Run the executable file.

## Worked Example
Here's a simple accounting problem to demonstrate how to use the program.

[Tony Bell's accounting workbook](https://www.accountingworkbook.com/)

| Date | Explanation | Units | Cost/Price ($) |
| :-- | :---: | :---: | ---: |
| May 1 | Beginning Inventory | 20 | 3.00 |
| May 5 | Purchase | 5 | 3.25 |
| May 13 | Sale | 22 | 10.00 |
| May 20 | Purchase | 7 | 3.55 |
| May 24 | Purchase | 5 | 3.70 |
| May 31 | Sale | 13 | 10.00 |

1. Prepare the inventory records using the FIFO method.
2. Using FIFO method compute Sales, Cost of Goods Sold and Gross Profit.
### Quick Calculation
```math
\text{Sales} = (22 \times \$10.00) + (13 \times \$10.00) = \$350.00
```
```math
\text{COGS} = (20 \times \$3.00) + (2 \times \$3.25) + (7 \times 3.55) + (3 \times \$3.70) = \$112.20
```
```math
\text{Gross Profit} = \text{Sales} - \text{COGS} = \$237.40
```
```math
\text{Gross Margin (\%)} = 67.94\%
```
### Leftover inventories at the end of the month
| Date | Explanation | Units | Cost/Price ($) |
| :-- | :---: | :---: | ---: |
| May 31 | Purchases | 2 | 3.70 |
## How to run the program (must be edited)

### Windows
For Windows users, run the setup file and it will be installed onto you system. Run the *.exe* file directly.

### MacOS
Download the *.dmg* file from the release page, mount it and open the drive. After that, move the main_fifo file into your Applications folder.

### Ubuntu (Debian)
Download the *.deb* file from the release page. You may run the installation file directly. Otherwise, you may install it through the command line.
```sh
cd ~Downloads
```
Run the file with the following command.
```sh
sudo dpkg -i fifoInventory.deb
```


### Linux
As for linux users, go to the directory, in most cases, it is

1. Download the tar file from the release page.
2. Open a terminal, go to the folder where your download has been saved. In most cases,
```sh
cd ~/Downloads
```
3. Extract the contents of the dowloaded folder with the following command.
```sh
tar xzf fifo_inventory.tar.gz
```
Remember to add sudo to the following commands.

4. Move the uncompressed fifo folder to /opt:
``` sh
mv fifo /opt
```
5. Create a symlink to the fifo executable:
```sh
ln -s /opt/fifo /usr/bin/fifoinventory
```
6. Move the desktop file to your applications folder:
```sh
mv fifo.desktop /usr/share/applications
```


## How to use the program
After running the program, you will see three major columns
1. date (in ISO format)
2. quantity
3. unit price/cost ($)

These are three fields you need to fill in. For each purchases and sales, you will receive a unique sequential id, recorded in the no. column. By default the date will be set to the current date.

## Choosing date, quantity and unit price
For the date column, click the dropdown and choose a suitable date.

After inputting the information into the fields, press <kbd>Enter</kbd> or click the<kbd>Purchase</kbd> button to update the list.

The same inputting method can be done for Sales.


![2024-10-29_10-37](https://github.com/user-attachments/assets/7b79dfd3-006f-4c54-a4f4-8cec233aa5a7)


### Warning
The date is for comparison purpose only, only the relative dates matter. If you input two transactions with the same purchase dates, the unique id will distinguish which came first. 

However, one purchase and one sales on the same day is ambiguous to the program. By default, the program assumes that purchases came first. 

To change the order of purchase and sale, please set the date to a later date. The absolute date does not matter during calculation.
### Clear
Press the <kbd>clear</kbd> button to clear the whole list. The index will not be resetted.


## Calculate
After inputting all the information, press <kbd>Calculate</kbd> to calculate the Cost of Goods Sold and Sales Revenue. The remaining inventories will be shown in Inventory row.

![2024-10-29_12-00](https://github.com/user-attachments/assets/32aac23e-32f1-44af-884a-a8631a5dad4d)

### Calculation Error
If you try to sell more stuff than your inventory has, it will raise a Calculation error with a pop-up window. Just press <kbd>Ok</kbd> and retype again.

![2024-10-29_12-08](https://github.com/user-attachments/assets/66f17471-5734-4da2-90ba-c63d3939db34)

### Light/Dark Mode
You may choose dark mode or light mode with the light/dark toggle depending on your preference.

## Using the code directly
Inside the main function, create an object for every transaction. Here is the example from before.
```python
p0 = Purchases("2024-05-01", 20, 3)
p1 = Purchases("2024-05-05", 5, 3.25)
p2 = Purchases("2024-05-20", 7, 3.55)
p3 = Purchases("2024-05-24", 5, 3.70)
s1 = Sales("2024-05-13", 22, 10.00)
s2 = Sales("2024-05-31", 13, 10.00)
```
Create a list to store all the purchases and a list to store all the sales. Create an Inventory object as input these lists as its parameters.
```python
i1 = Inventory([p0, p1, p2, p3], [s1, s2])
```
```python
print(f"{i1.cogs()=:.2f}")
print(f"{i1.sales_revenue()=:.2f}")
print(f"{i1.leftover_inventory()=}")
```
You should get these outputs:
```sh
i1.cogs()=112.20
i1.sales_revenue()=350.00
i1.leftover_inventory()=
[Purchases(
	date_iso		= datetime.date(2024, 5, 24), 
	quantity		= 2, 
	unit_price		= 3.7, 
	classification	= 'purchases', 
	index			= 3
)]
```
Besides this file, you may also compile the main file and run the program through tkinter program.
## Tests

Basic tests have been made with the program to ensure consistent result. However, most of the tests are done on the source code through the unittest module.

### Unit  Tests
Basic unit testing has been made to make sure these inputs are correct.
* Correct conversion of string into datetime objects.
* Correct sorting of orders according to date and indexes.
* Raising error when sale is more than inventory left.
* Correct result for sales revenue and cost of goods sold. (easily verifiable)
* Raising errors for impossible dates due to leap years.
* Correctly sort the orders when the dates are the same (by using indexes to distinguish them.)

These tests are all I can think of during code testing. 

If you can find some edge cases that give the wrong result or raise an error, please submit issues through this repository.

## Credits
I would like to thank Mr. Tony Bell for his educational videos in accounting and workbooks. He is my inspiration for this accounting project.

## How to extend the code?
Due to complication issue, I purposefully design the code to be as simple as possible, but the lack of time limits the inventories to be inserted at a different day. Here are ways you can extend the code.
* Change the inventory method to **LIFO** method. (It will involve sorting the orders in reverse.)
* The **weighted average** method.
* The ability to read from and write to csv for larger files and swifter input.
* Faster looping?

## Contribution

This is just a small project of mine, but I appreciate your help if you are willing to spend the time to make this project better.

The source code is mainly written in **attrs**, and it has been made extremely readable and easy to maintain, all classes and functions have their types defined properly.


