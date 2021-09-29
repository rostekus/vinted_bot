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

### Executing program

* How to run the program
* Step-by-step bullets
```
python3 app.py
```


## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)
