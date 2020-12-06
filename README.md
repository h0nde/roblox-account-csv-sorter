# roblox-account-csv-gen
Generates a CSV from a list of .ROBLOSECURITY cookies (set in combos.txt)

## Speed
With the default configuration of 500 threads, I personally was able to reach a peak of 20,000 checks-per-minute using fineproxy (us).

## Supported formats (per line)
- username:password:cookie
- cookie

## Output
The results are saved into `accounts.csv` in the following format:
- Id
- Name
- Password
- Robux
- Total Collectible RAP
- Total Collectible Value
- Premium Stipend
- Premium Expiry Date
- PIN Enabled
- Collectibles <Name (RAP, [VALUE] [PROJ])>
- .ROBLOSECURITY Cookie
