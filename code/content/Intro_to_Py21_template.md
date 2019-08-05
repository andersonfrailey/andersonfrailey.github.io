# Intro to Py21
Blackjack has long been one of the most popular games you’ll find in a casino. Its simplicity makes it an easy option for beginners and the relatively modest house edge appeals to more seasoned gamblers. The game also has a strong history of detailed computational analysis. Ed Thorpe’s classic, _Beat the Dealer_, has been regarded as the gold standard in blackjack analysis since its publication in 1966. In it, Thorpe uses an IBM 704 to simulate games of blackjack, ultimately determining the best strategy for a player (now known as basic strategy). Inspired by Thorpe (and _The Perfect Bet_ by Adam Kucharski), I set out to create a modern blackjack simulator. The result is Py21.

## Usage
Py21 is a simple Python package that can simulate an arbitrary number of hands of blackjack.  It can be used to collect data on new strategies, compare the performance of multiple strategies, and much more. To get started, all you need to familiarize yourself with are the `Game` and `Player` objects.

Each simulation starts by initializing at least one instance of the `Player` class and a single instance of the `Game` class. Each `Player` instance starts with a bankroll and the option of providing custom functions for determining the player’s actions on a given hand. The purpose of these optional functions can be found in the Py21  [documentation](https://github.com/andersonfrailey/blackjack/blob/master/docs/index.md) .

```python
from py21 import Player, Game


player = Player(100, strategy_func=optional_strategy_function,
                wager_func=optional_wager_function,
                insurance_func=optional_insurance_function)
```

Once all of the players have been initiated, the `Game` object is initiated with a list of the players and an optional dictionary of rule changes to modify the exact parameters of the game being simulated. I’ll go into more detail on how to modify the rules later in this post.

```python
game = Game([player], rules=optional_rules_dict)
```

Once the Game object is initiated, you can simulate as many hands as you want.

```python
game.simulate(1000000)
```

Py21 collects data for each hand that you simulate including the action the player takes (hit, stand, etc.), the result of that action, the count, the dealer’s up card, and wager. A full list of of the data collected can be found [here](https://github.com/andersonfrailey/blackjack/blob/master/docs/data.md). You can use this data to measure how various strategies perform and create visualizations. Py21 comes with a two built in functions for creating Altair plots. These can be imported from the Py21 `utils` module.

The first creates a simple bar chart that compares outcomes between different players. This is useful for if you want a high level comparison of the outcomes of different strategies.

```python
from py21 import Player, Game
from py21.utils import outcome_bars
from py21.strategies import hit_to_seventeen

player = Player(1000)
player2 = Player(1000, strategy_func=hit_to_seventeen)
game = Game([player, player2])
game.simulate(1000)

outcome = outcome_bars([player.history, player2.history],
                       name=["Basic Strategy", "Hit to 17"])
```
<div id="vis"></div>
{{ outcomebars }}

The second creates a heat map showing the percentage of times a given outcome occurs, grouped by the player’s total and the dealer’s up card. The heat map can be made for

```python
from py21 import Player, Game
from py21.utils import result_heatmap

player = Player(1000)
game = Game([player])
game.simulate(1000)

heatmap = result_heatmap(player.history, result="win",
                         title="Winning Pct")
```
<div id="vis"></div>
{{ heatmap }}

## Flexibility
Like Thorpe, my main motivation was evaluating how various strategies performed. Building a basic simulator is simple enough, but I wanted to make mine as flexible as possible. Rather than hard coding parameters and strategies, I built Py21 so that it would be extremely straightforward to tweak the rules of the game and each player’s strategy for deciding whether to hit or stand, how to wager, and even when to take insurance.

### Customizing Player Actions

To customize player behavior, the user can specify three functions when creating an instance of the player class that control the player’s actions.  First, is the action a player takes given their total and what the dealer is showing, the second is how much the player will wager, and the third is if and when the player takes insurance. Each of these functions gets called during the simulations and takes the same arguments. Details on what these arguments are and what the functions are expected to return, see the [documentation](https://github.com/andersonfrailey/blackjack/blob/master/docs/index.md#creating-custom-functions).

As a default, Py21 plays with basic strategy, always bets the minimum, and never takes insurance. There are some additional functions in the `strategies` module of Py21 that can be used as alternative values if you do not wish to write your own, but want to use something other than basic strategy.

```python
from py21 import Player, game
from py21.strategies import hit_to_seventeen


player = Player(1000, strategy_func=hit_to_seventeen)
```

### Modifying the Rules

As mentioned earlier, Py21 users can modify the rules of the game their simulations are run under. To do so, they need only specify a dictionary that pairs the rule they wish to change with its new value. For example, here is how you change the number of decks used from the default value of eight to six:

```python
new_rules = {
 "num_decks": 6
}
game = Game([player], rules=new_rules)
```

Internally, Py21 will take this dictionary and update each parameter it contains accordingly. This is handled using a package called ParamTools.

## Using ParamTools
To make changing the rules of the game easy, I enlisted a package called  [ParamTools](https://paramtools.org/) . ParamTools is a Python library centered around handling parameter processing and validation for computational models. With ParamTools, I was able to set the basic rules of the game as defaults and provide a simple method for changing them to run simulations under different conditions all while validating any user input.

Take as an example the number of decks used in a game. Using a simple JSON format, I can set the default value for this parameter (`num_decks`) to 8, and set minimum and maximum values used for input validation:

```
"num_decks": {
  "title": "Number of decks the game will be played with",
  "description": "Number of decks used in the game.",
  "notes": "",
  "section_1": "Game",
  "section_2": "Deck",
  "type": "int",
  "number_dims": 0,
  "value": [{"value": 8}],
  "validators": {
      "range": {
          "min": 1,
          "max": 9e+99
      }
  }
}
```

The user can then create their own custom rules using the format discussed above. Note that this is a rather verbose example of parameter setting. ParamTools allows you to slim this down if you would like.

A major advantage of using ParamTools is that if a user were to try and pass an invalid modification to the rules — such as setting the number of decks to zero — ParamTools will catch this and throw and error so I do not need to write my own code for input validation.

## Closing Thoughts
In short, Py21 is a basic package for running blackjack simulations. It is flexible enough to be tailored for each users needs, while still being powerful enough to run a million simulations in around a minute<sup>1</sup>. At this stage, Py21 is stable and I do not foresee any major changes to its core. Future development will focus on adding new features such as additional graphing capabilities, strategies, and greater data collection. I’m also open to any requests from users.

You can install Py21 using `pip install py21`, or by downloading the source code from [GitHub](https://github.com/andersonfrailey/blackjack).

##### _Footnotes_

<sup>1</sup> The exact amount of time needed to run your simulations depends on how complex your strategies and the number of players involved in the game.  I was able to run a million hands in around a minute with one player using basic strategy.

