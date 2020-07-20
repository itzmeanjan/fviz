# fviz

![banner](./ss/banner.png)

Facebook Data Visualizer - made with &lt;3

**Released v0.4.0 on PyPI**

## vision

I was interested in understanding my facebook activities overtime. Also I had a knack in checking how much data I'm giving facebook. So, I thought of analysing exported facebook data and understanding what's it saying. 

Later on I thought of making this tool a portable and easy installable one. So that anyone which some simple installation skills can use this tool and generate various plots, and understand their own activity on facebook overtime. 

This tool does strictly run on user's machine. It doesn't talk to any remote machine, so you can use it while feeding it your exported facebook data. 

## usage

- Make sure you've Python ( >=3.7 ) installed
- Also install pip using your OS specific package manager

```bash
$ sudo apt-get install python3-pip
```

- Now you're good to go and install **fviz**

```bash
$ python3 -m pip install fviz -U
```

- And voila !!!
- *fviz* is installed at `$HOME/.local/bin`. Add this path to `$PATH` env variable. For so, open `~/.bashrc` and append following line at very bottom. This will make *fviz* available for invokation from any place in your system.

```bash
export PATH="$PATH:$HOME/.local/bin"
```

- I'm assuming you've already requestsed facebook for exporting your facebook data, and downloaded so. Time to pass that *.zip* file to *fviz* and get results.

```bash
$ fviz facebook-username.zip sink plots
```

- `sink` is the directory where this *.zip* to be extracted. And `plots` is the directory where generated plots to be placed. You can set them as you will.


## visualisation

All these plots to be generated when you invoke *fviz* with proper params.
- Likes and Reactions
    - [Facebook Likes & Reactions by You](./docs/reactionsByYou.md)
    - [Top 10 Facebook profiles, whose posts were mostly reacted by You](./docs/top10ProfilesWithMostlyReactedPostsByYou.md)
    - [Detailed Facebook Likes & Reactions HeatMap](./docs/detailedReactionsHeatMap.md)
    - [Weekly Accumulated Facebook Likes & Reactions HeatMap](./docs/weeklyAccumulatedReactionsHeatMap.md)
    - [Top 3 Facebook profiles, whose posts were mostly liked & reacted by YOU, _per month_](./docs/top3ProfilesWithMonthlyMostReactedPosts.md)
    - [Accumulated Facebook likes and reactions mapped onto each minute of a Day](./docs/accumulatedAcivityInEachMinuteOfDay.md)


**This section will keep getting populated !!!**
