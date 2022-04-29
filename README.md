# openx-tasks

## Requierments
#### To use scripts install packages listed in requirements.txt 

## Task1 - Suppy Chain

### Usage

##### Download supply-chain.py file. Then import it as an python module to your script.

### Documentation

#### To check if a domain is direct or indirect seller use `is_seller_indirect()` function. It takes one argument which is `seller_domain: str`. It returns `True` if seller is indirect, otherwise it returns `False`. Note that it works only for openx sellers.

#### Example usage

```
from supply-chain import is_seller_indirect()

print(is_seller_indirect('google.com'))
```

#### To check what is maximum depth of supply chain use `max_supply_chain_depth()` it takes one argument which is `domain: str`. It returns given domain maximum supply depth as `int`. 

#### Note that!
- Function use recursion so for domains with large amount of sellers it might execute for very long time
- Maximum recursion depth in python is 1000 so if depth of supply chain exceeds that, it wont be returned. Only the exception about exceeding maximum recursion depth. 
- Some domains do not publish their sellers. If that is the case with some seller of given domain. Calculating the depth will be stopped at it for that branch and program will switch to next one. Because of that returned value migth be lowered. 

#### Example usage

```
from supply-chain import max_supply_chain_depth()

print(max_supply_chain_depth('openx.com'))
```

## Task 2 

### Usage

##### Download find-available-spot.py file. Then execute it from the command line as a python script, providing arguments listed below. Script will print the closest possible date and time to start activity. 

- -c <calendars> : relative path to folder with calendars 
- -d <duration-in-minutes> : duration of activity in minutes
- -m <minimum-people> : minimum people required for the activity

#### Example

```console
python3 find-available-slot.py --calendars /calendars --duration-in-minutes 30 --minumum-people 2
```
#### Note that!
  - Script assumes correctness of data provided in calendars.






