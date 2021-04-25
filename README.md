# Introduction 
In development generalize scraper

# Getting Started
1.	Installation process
    - Install [pipenv](https://pipenv-fork.readthedocs.io/en/latest/install.html)
    - Then from the root folder run pipenv install
    - After dependencies are installed run pipenv shell to activate virtual env.
<!-- 2.	Software dependencies
3.	Latest releases
4.	API references -->

# How to build config.json
See the examples given in ```jobs/``` to build a custom config.json file.
- We can select the elements we want to scrape using following selections:
    - **css** : The CSS selectors. Example -
    ```javascript
    [{
        "name":"likes",
        "selection":"css",
        "search":["span#likes", "p#likes"], // Can specify multiple selectors the one that matches will be considered.
        "first":true, // The first occurence that encountered
        "attribute":"text" // Attribute to get value from
    }]
    /*
        OUTPUT:
        [{
            "likes":"37",

        }]
    */
    ```
    - **xpath** : The Xpath of an element. Example -
    ```javascript
    [{
        "name":"keywords",
        "selection":"xpath",
        "search":["//span[@id='keywords']", "//p[@id='keywords']"], // Can specify multiple selectors the one that matches will be considered.
        "first":false, // The first occurence that encountered
        "attribute":"text" // Attribute to get value from
    }]
    /*
        OUTPUT:
        [{
            "keywords":["Battle Ropes",
                        "Kettlebells",
                        "BOSU",
                        "Dumbbells",
                        "Jump Ropes",
                        "Medicine Balls",
                        "Plyometric Boxes",
                        "Resistance Bands"],

        }]
    */
    ```
    - **regex** : Extracts the element from the pattern. Example -
    ```javascript
    [
        {
            "name":"data",
            "selection":"regex",
            "search":["<script>window.__PRELOADED_STATE__ = (.*);</script>"]
        }
    ]
    /*
        OUTPUT:
        [{
            "data":"{\"address\":\"23 avenue fake street\", \"phoneNumber\":\"+1 (000-000-0000)\"}"
        }]

        Which later can be converted into python dicionary by json **load** and using **eval** method
    */
    ```
    - **find** : Find element using python's [Format String Syntax](https://docs.python.org/3/library/string.html#format-string-syntax) In raw html document. Example - 
    ```javascript
    [
        {
            "name":"phone",
            "selection":"find",
            "search":["\"phoneNumber\":\"{}\""],
            "first":true,
            "attribute":"text"
        }
    ]
    /*
    [{
        "phone":"+1 (000-000-0000)"
    }]
    */

    ```
    - **tables** : Extract all tables for a given html. Example - 
    ```javascript
    [{
        "name":"info_tables",
        "selection":"tables"
    }]

    /*
    Ex URL : https://gympricelist.com/title-boxing-club-prices/

    Output:
        [
            {
                "info_tables": [
            [
                {
                    "Service": "MONTHLY",
                    "Cost": "MONTHLY"
                },
                {
                    "Service": "SINGLE",
                    "Cost": "SINGLE"
                },
                {
                    "Service": "Initiation Fee",
                    "Cost": "$149.49"
                },
                {
                    "Service": "Monthly Fee",
                    "Cost": "$79.49"
                },
                {
                    "Service": "Cancellation Fee",
                    "Cost": "$0.00"
                },
                {
                    "Service": "TWO ADULTS  (adsbygoogle = window.adsbygoogle || []).push({});",
                    "Cost": "TWO ADULTS  (adsbygoogle = window.adsbygoogle || []).push({});"
                },
                {
                    "Service": "Initiation Fee",
                    "Cost": "$299.49"
                },
                {
                    "Service": "Monthly Fee",
                    "Cost": "$149.49"
                },
                {
                    "Service": "Cancellation Fee",
                    "Cost": "$0.00"
                },
                {
                    "Service": "Yearly",
                    "Cost": "Yearly"
                },
                {
                    "Service": "SINGLE",
                    "Cost": "SINGLE"
                },
                {
                    "Service": "Initiation Fee",
                    "Cost": "$99.49"
                },
                {
                    "Service": "Annual Fee",
                    "Cost": "$719.49"
                },
                {
                    "Service": "Cancellation Fee",
                    "Cost": "$0.00"
                },
                {
                    "Service": "TWO ADULTS",
                    "Cost": "TWO ADULTS"
                },
                {
                    "Service": "Initiation Fee",
                    "Cost": "$199.49"
                },
                {
                    "Service": "Annual Fee",
                    "Cost": "$1439.49"
                },
                {
                    "Service": "Cancellation Fee",
                    "Cost": "$0.00"
                }
            ],
            [
                {
                    "0": "Days",
                    "1": "Hours"
                },
                {
                    "0": "Monday",
                    "1": "8AM–5PM"
                },
                {
                    "0": "Tuesday",
                    "1": "8AM–5PM"
                },
                {
                    "0": "Wednesday",
                    "1": "8AM–5PM"
                },
                {
                    "0": "Thursday",
                    "1": "8AM–5PM"
                },
                {
                    "0": "Friday",
                    "1": "8AM–5PM"
                },
                {
                    "0": "Saturday",
                    "1": "Closed"
                },
                {
                    "0": "Sunday",
                    "1": "Closed"
                }
            ]
        ]
            }
        ]
    */
    ```
    - **recursive** : To iterate over a nested HTML structure recursively. Example - 
    ```javascript
    [{
        
        "name": "amenities",
        "selection": "recursive",
        "rules": {
            "data(#amenities > div > div)": [
                {
                    "name": "h2",
                    "services(ul)": [
                        "li"
                    ]
                }
            ]
        }
    
    }]

    /*  
        Ex URL:https://www.anytimefitness.com/gyms/2863/roseville-ca-95661/
        
        Output: 
        [{
            "amenities": {
            "data": [
                {
                    "name": "Gym Amenities",
                    "services": [
                        "24-Hour Access",
                        "24-Hour Security",
                        "Convenient Parking",
                        "Worldwide Club Access",
                        "Private Restrooms",
                        "Private Showers",
                        "Tanning",
                        "HDTVs",
                        "Health Plan Discounts",
                        "Wellness Programs",
                        "Free Classes"
                    ]
                },
                {
                    "name": "Cardio",
                    "services": [
                        "Treadmills",
                        "Elliptical Cross-trainers",
                        "Spin Bikes",
                        "Cardio TVs",
                        "Exercise Cycles",
                        "Rowing Machines",
                        "Stair Climbers"
                    ]
                },
                {
                    "name": "Strength/Free Weights",
                    "services": [
                        "Free Weights",
                        "Squat Racks",
                        "Plate Loaded",
                        "Circuit/Selectorized",
                        "Dumbbells",
                        "Barbells"
                    ]
                },
                {
                    "name": "Functional Training",
                    "services": [
                        "Battle Ropes",
                        "Kettlebells",
                        "TRX",
                        "BOSU",
                        "Dumbbells",
                        "Jump Ropes",
                        "Medicine Balls",
                        "Plyometric Boxes",
                        "Resistance Bands"
                    ]
                },
                {
                    "name": "Training and Coaching Services",
                    "services": [
                        "Personal Training",
                        "Specialized Classes",
                        "Small Group Training",
                        "Virtual Studio Classes",
                        "Fitness Assessment"
                    ]
                }
            ]
        }
        }]

    */
    ```
## Methods on attributes:
- href
```javascript
{
        "name":"website",
        "selection":"css",
        "search":["my selection"],
        "first":true,
        "attribute":"href",
        "extract_from_href":"?url" // Extract Query Parameter, here url
    }
```
- text
```javascript
{
        "name":"total_reviews",
        "selection":"css",
        "search":["my selection"],
        "first":true,
        "attribute":"text",
        "extract_from_text":"-?\\d+\\.?\\d*" // Extract from text, here number
    }
```

# How to Run
Write the custom class in ```example.py``` (see examples) inherit the Crawl class and run ```ExampleClass.run()```

# Roadmap
- Add functionality to render HTML(with proxy). By simply putting 
```python
render=True
``` 

- Designing API.
- Integrating Celery.
- Dynamic Celery Workflow for registered Jobs. Using YAML file. Example
```yaml
example.MyWorkflow:
  tasks:
    - Google
    - GROUP_1:
        type: group
        tasks:
          - Yelp
          - BBB
          - Manta
```

<!-- # Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore) -->