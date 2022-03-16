Due to changes of the source code of vinted website, bot lost it's functionallity :(

# Vinted Bot
The bot was created for founding clothes on popular site for selling clothes vinted.com. If you want to save money, it is good idea to not to buy one clothing from user as you the price of shipping stays the same no matter how many clothes you are buying. Unfortunately it takes much more time to check if the user has more then just one piece of clothing mathing you. 

## Features
  :large_blue_circle: **Find user with matching you clothes**  
  :large_blue_circle: **Specify size, number of clothes and brands**  
  :large_blue_circle: **Saving to sqlite3 database or csv file**  
  :large_blue_circle: **Sending cvs file to your email**


### Installing

You can just run docker or install requarments 
Dependencies of the core modules are listed in requirements.txt
```
pip3 install requirements.txt
```
and then run
```
python3 setup.py
```
The config.ini will be created. If you want to change credentials just run again setup.py or modify config file. It is also posible by using flags.

Example:

* Step-by-step bullets

```
python3 app.py --url https://www.vinted.pl/... --brands zara,hm --price 15
```



## Authors

Contributors names and contact info

Rostyslav Mosorov 
[rmosorov@icloud.com](rmosorov@icloud.com)

## License
MIT License

Copyright (c) [2021] [Rostyslav Mosorov]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
