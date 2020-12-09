# roblox-account-csv-gen
Tool for organizing and filtering lists of Roblox accounts.

## Requirements
Python 3.8 or later

## Usage
- Fill proxies.txt with your list of proxies
- Fill combos.txt with your list of cookies (or user:pass:cookies)
- Run csvgen.sh, upon completion open `accounts.csv` with your software of choice

## Speed
With the default configuration of 500 threads, I personally was able to reach a peak of 13,000 checks-per-minute using fineproxy (us) (as of 2020-12-09).

## Item finder
To find accounts with specific items, you can create a file called `find.txt` and place your list of asset IDs in it (seperated by line).
Discovered items will pop up in the `Found Items` row.

## Account reactivation
The tool will automatically attempt to reactivate banned accounts, where it is possible to do so.

## Supported formats (per line)
- username:password:cookie
- cookie

## Output
The results are saved into `accounts.csv` in the following format:
- Id
- Name
- Password
- Robux Balance
- Credit Balance
- Total Group Funds (transferrable only)
- Total Collectible RAP
- Total Collectible Value
- Premium Stipend
- Premium Expiry Date
- Email Status (VERIFIED|UNVERIFIED|NO EMAIL)
- PIN Enabled
- Above 13
- Found Items [<Name (ID)>, ..]
- Inventory Count (heads, hats, accessories, gears, faces)
- Collectibles [<Name (RAP, [VALUE] [PROJ])>, ..]
- .ROBLOSECURITY Cookie
