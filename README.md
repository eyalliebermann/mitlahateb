# Voluntizer / mitlahateb

## Participation
### Installing the development environment ( MacOs )
 Follow the installation guide [here]((http://www.pyladies.com/blog/Get-Your-Mac-Ready-for-Python-Programming/)
 
 Install python 2.7:
 ```
 $ brew install python
 ```
  
 Install pip:
 ```
 $ curl -O http://python-distribute.org/distribute_setup.py
 $ python distribute_setup.py
 $ curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
 $ python get-pip.py
 ```
  
 Install virutalenv
 ```
 $ pip install virtualenv
 ```
 
 Install virtualenvwrapper
 ```
 $ sudo pip install virtualenvwrapper
 ```
 
 Configure your terminal to use the virtual environment script. Assuming you're using iTerm with zsh sheel. Add the follwoing line to you ~/.zshrc file
 ```
 #python virtualenv setup
 export WORKON_HOME=~/.virtualenvs
 export PROJECT_HOME=$HOME/dev
 source /usr/local/bin/virtualenvwrapper.sh
 ```
 Install postgres sql server
 ```
 $ brew install postgresql
 ```
 Migrate your local database to the latrst schema 
 ```
 ```
 
 Start the database service
 ```
 pg_ctl -D /usr/local/var/postgres -l logfile start
 ```
 
 
