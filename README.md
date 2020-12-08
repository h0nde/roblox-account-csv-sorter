# roblox-account-csv-gen
Python >=3.8 CSV generator for Roblox accounts.

## Speed
With the default configuration of 500 threads, I personally was able to reach a peak of 15,000 checks-per-minute using fineproxy (us).

## find.txt
To find accounts with specific items, you can create a file called `find.txt` and place your list of asset IDs in it (seperated by line).
Discovered items will pop up in the `Found Items` row.

## Temporary bans
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
- PIN Enabled
- Above 13
- Found Items [<Name (AssetID)>, ..]
- Inventory Count (hats only)
- Collectibles [<Name (RAP, [VALUE] [PROJ])>, ..]
- .ROBLOSECURITY Cookie
