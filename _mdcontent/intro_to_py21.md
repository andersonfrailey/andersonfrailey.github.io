# Intro to Py21
---

Blackjack has long been one of the most popular games you’ll find in a casino. Its simplicity makes it an easy option for beginners and the relatively modest house edge appeals to more seasoned gamblers. The game also has a strong history of detailed computational analysis. Ed Thorpe’s classic, _Beat the Dealer_, has been regarded as the gold standard in blackjack analysis since its publication in 1966. In it, Thorpe uses an IBM 704 to simulate games of blackjack, ultimately determining the best strategy for a player (now known as basic strategy). Inspired by Thorpe (and _[The Perfect Bet](https://www.basicbooks.com/titles/adam-kucharski/the-perfect-bet/9781541697232/)_ by Adam Kucharski), I set out to create a modern blackjack simulator. The result is Py21.

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
<div id="vis2"></div>
<script type="text/javascript">
    var spec2 = {"config": {"view": {"width": 400, "height": 300}}, "data": {"name": "data-7a90f3f915121b64addabd343a801130"}, "mark": "bar", "encoding": {"color": {"type": "ordinal", "field": "game", "legend": null}, "column": {"type": "ordinal", "field": "result", "title": "Result"}, "tooltip": [{"type": "quantitative", "field": "pct", "title": "Pct"}], "x": {"type": "nominal", "axis": {"labelAngle": -45}, "field": "game", "sort": ["Win", "Loss", "Push"], "title": null}, "y": {"type": "quantitative", "field": "pct"}}, "width": 100, "$schema": "https://vega.github.io/schema/vega-lite/v2.6.0.json", "datasets": {"data-7a90f3f915121b64addabd343a801130": [{"game": "Basic Strategy", "order": 1, "pct": 0.427, "result": "Win"}, {"game": "Basic Strategy", "order": 2, "pct": 0.487, "result": "Loss"}, {"game": "Basic Strategy", "order": 3, "pct": 0.086, "result": "Push"}, {"game": "Hit to 17", "order": 1, "pct": 0.407, "result": "Win"}, {"game": "Hit to 17", "order": 2, "pct": 0.494, "result": "Loss"}, {"game": "Hit to 17", "order": 3, "pct": 0.098, "result": "Push"}]}};
    var embed_opt2 = {"mode": "vega-lite"};

    function showError(el, error){
        el.innerHTML = ('<div class="error">'
                        + '<p>JavaScript Error: ' + error.message + '</p>'
                        + "<p>This usually means there's a typo in your chart spec2ification. "
                        + "See the javascript console for the full traceback.</p>"
                        + '</div>');
        throw error;
    }
    const el2 = document.getElementById('vis2');
    vegaEmbed("#vis2", spec2, embed_opt2)
      .catch(error => showError(el, error));
  </script>

The second creates a heat map showing the percentage of times a given outcome (win, loss, or push) occurs, grouped by the player’s total and the dealer’s up card.

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
<div id="vis1"></div>
<script type="text/javascript">
    var spec1 = {"config": {"view": {"width": 400, "height": 300}}, "data": {"name": "data-9b3cbbfa30ccaa81896c42e82468f24a"}, "mark": {"type": "rect", "binSpacing": 1}, "encoding": {"color": {"type": "quantitative", "field": "win", "legend": {"title": "Win Probability", "values": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]}}, "tooltip": [{"type": "quantitative", "field": "dealer_up", "title": "Dealer Up Card"}, {"type": "quantitative", "field": "total", "title": "Player Total"}, {"type": "quantitative", "field": "win", "title": "Win Probability"}], "x": {"type": "ordinal", "axis": {"labelAngle": 0, "orient": "top"}, "field": "dealer_up", "title": "Dealer Up Card"}, "y": {"type": "ordinal", "field": "total", "sort": {"op": "mean", "order": "descending"}, "title": "Player Total"}}, "height": 500, "title": "Winning Pct", "width": 500, "$schema": "https://vega.github.io/schema/vega-lite/v2.6.0.json", "datasets": {"data-9b3cbbfa30ccaa81896c42e82468f24a": [{"total": 21, "dealer_up": 11, "win": 0.966, "loss": 0.0, "push": 0.034}, {"total": 21, "dealer_up": 10, "win": 0.978, "loss": 0.0, "push": 0.022}, {"total": 21, "dealer_up": 9, "win": 0.967, "loss": 0.0, "push": 0.033}, {"total": 21, "dealer_up": 8, "win": 0.957, "loss": 0.0, "push": 0.043}, {"total": 21, "dealer_up": 7, "win": 0.957, "loss": 0.0, "push": 0.043}, {"total": 21, "dealer_up": 6, "win": 0.968, "loss": 0.0, "push": 0.032}, {"total": 21, "dealer_up": 5, "win": 0.965, "loss": 0.0, "push": 0.035}, {"total": 21, "dealer_up": 4, "win": 0.964, "loss": 0.0, "push": 0.036}, {"total": 21, "dealer_up": 3, "win": 0.951, "loss": 0.0, "push": 0.049}, {"total": 21, "dealer_up": 2, "win": 0.95, "loss": 0.0, "push": 0.05}, {"total": 20, "dealer_up": 6, "win": 0.8, "loss": 0.097, "push": 0.103}, {"total": 20, "dealer_up": 2, "win": 0.753, "loss": 0.122, "push": 0.125}, {"total": 20, "dealer_up": 3, "win": 0.765, "loss": 0.114, "push": 0.121}, {"total": 20, "dealer_up": 4, "win": 0.773, "loss": 0.106, "push": 0.121}, {"total": 20, "dealer_up": 5, "win": 0.782, "loss": 0.108, "push": 0.11}, {"total": 20, "dealer_up": 10, "win": 0.59, "loss": 0.039, "push": 0.371}, {"total": 20, "dealer_up": 7, "win": 0.849, "loss": 0.07, "push": 0.081}, {"total": 20, "dealer_up": 8, "win": 0.861, "loss": 0.068, "push": 0.071}, {"total": 20, "dealer_up": 9, "win": 0.816, "loss": 0.058, "push": 0.126}, {"total": 20, "dealer_up": 11, "win": 0.794, "loss": 0.046, "push": 0.16}, {"total": 19, "dealer_up": 6, "win": 0.699, "loss": 0.197, "push": 0.105}, {"total": 19, "dealer_up": 2, "win": 0.637, "loss": 0.24, "push": 0.123}, {"total": 19, "dealer_up": 3, "win": 0.637, "loss": 0.242, "push": 0.122}, {"total": 19, "dealer_up": 4, "win": 0.661, "loss": 0.222, "push": 0.117}, {"total": 19, "dealer_up": 5, "win": 0.659, "loss": 0.22, "push": 0.121}, {"total": 19, "dealer_up": 7, "win": 0.768, "loss": 0.151, "push": 0.081}, {"total": 19, "dealer_up": 9, "win": 0.465, "loss": 0.179, "push": 0.355}, {"total": 19, "dealer_up": 10, "win": 0.475, "loss": 0.406, "push": 0.119}, {"total": 19, "dealer_up": 11, "win": 0.629, "loss": 0.211, "push": 0.16}, {"total": 19, "dealer_up": 8, "win": 0.728, "loss": 0.137, "push": 0.135}, {"total": 18, "dealer_up": 4, "win": 0.514, "loss": 0.359, "push": 0.127}, {"total": 18, "dealer_up": 6, "win": 0.592, "loss": 0.302, "push": 0.106}, {"total": 18, "dealer_up": 2, "win": 0.491, "loss": 0.366, "push": 0.143}, {"total": 18, "dealer_up": 3, "win": 0.513, "loss": 0.355, "push": 0.132}, {"total": 18, "dealer_up": 5, "win": 0.542, "loss": 0.343, "push": 0.115}, {"total": 18, "dealer_up": 7, "win": 0.638, "loss": 0.23, "push": 0.132}, {"total": 18, "dealer_up": 8, "win": 0.375, "loss": 0.267, "push": 0.358}, {"total": 18, "dealer_up": 9, "win": 0.346, "loss": 0.533, "push": 0.12}, {"total": 18, "dealer_up": 10, "win": 0.348, "loss": 0.532, "push": 0.12}, {"total": 18, "dealer_up": 11, "win": 0.463, "loss": 0.379, "push": 0.157}, {"total": 17, "dealer_up": 7, "win": 0.26, "loss": 0.368, "push": 0.372}, {"total": 17, "dealer_up": 3, "win": 0.365, "loss": 0.5, "push": 0.135}, {"total": 17, "dealer_up": 4, "win": 0.39, "loss": 0.47, "push": 0.14}, {"total": 17, "dealer_up": 5, "win": 0.422, "loss": 0.457, "push": 0.121}, {"total": 17, "dealer_up": 6, "win": 0.418, "loss": 0.416, "push": 0.166}, {"total": 17, "dealer_up": 2, "win": 0.356, "loss": 0.504, "push": 0.14}, {"total": 17, "dealer_up": 8, "win": 0.24, "loss": 0.63, "push": 0.131}, {"total": 17, "dealer_up": 9, "win": 0.228, "loss": 0.649, "push": 0.123}, {"total": 17, "dealer_up": 10, "win": 0.227, "loss": 0.65, "push": 0.122}, {"total": 17, "dealer_up": 11, "win": 0.307, "loss": 0.528, "push": 0.164}, {"total": 16, "dealer_up": 11, "win": 0.297, "loss": 0.703, "push": 0.0}, {"total": 16, "dealer_up": 10, "win": 0.208, "loss": 0.792, "push": 0.0}, {"total": 16, "dealer_up": 8, "win": 0.243, "loss": 0.757, "push": 0.0}, {"total": 16, "dealer_up": 7, "win": 0.241, "loss": 0.759, "push": 0.0}, {"total": 16, "dealer_up": 6, "win": 0.425, "loss": 0.575, "push": 0.0}, {"total": 16, "dealer_up": 5, "win": 0.425, "loss": 0.575, "push": 0.0}, {"total": 16, "dealer_up": 4, "win": 0.401, "loss": 0.599, "push": 0.0}, {"total": 16, "dealer_up": 3, "win": 0.38, "loss": 0.62, "push": 0.0}, {"total": 16, "dealer_up": 2, "win": 0.351, "loss": 0.649, "push": 0.0}, {"total": 16, "dealer_up": 9, "win": 0.22, "loss": 0.78, "push": 0.0}, {"total": 15, "dealer_up": 9, "win": 0.226, "loss": 0.774, "push": 0.0}, {"total": 15, "dealer_up": 6, "win": 0.424, "loss": 0.576, "push": 0.0}, {"total": 15, "dealer_up": 3, "win": 0.375, "loss": 0.625, "push": 0.0}, {"total": 15, "dealer_up": 4, "win": 0.396, "loss": 0.604, "push": 0.0}, {"total": 15, "dealer_up": 5, "win": 0.42, "loss": 0.58, "push": 0.0}, {"total": 15, "dealer_up": 11, "win": 0.283, "loss": 0.717, "push": 0.0}, {"total": 15, "dealer_up": 7, "win": 0.26, "loss": 0.74, "push": 0.0}, {"total": 15, "dealer_up": 8, "win": 0.262, "loss": 0.738, "push": 0.0}, {"total": 15, "dealer_up": 10, "win": 0.256, "loss": 0.744, "push": 0.0}, {"total": 15, "dealer_up": 2, "win": 0.352, "loss": 0.648, "push": 0.0}, {"total": 14, "dealer_up": 3, "win": 0.377, "loss": 0.623, "push": 0.0}, {"total": 14, "dealer_up": 4, "win": 0.39, "loss": 0.61, "push": 0.0}, {"total": 14, "dealer_up": 2, "win": 0.36, "loss": 0.64, "push": 0.0}, {"total": 14, "dealer_up": 7, "win": 0.246, "loss": 0.754, "push": 0.0}, {"total": 14, "dealer_up": 5, "win": 0.423, "loss": 0.577, "push": 0.0}, {"total": 14, "dealer_up": 6, "win": 0.426, "loss": 0.574, "push": 0.0}, {"total": 14, "dealer_up": 9, "win": 0.228, "loss": 0.772, "push": 0.0}, {"total": 14, "dealer_up": 10, "win": 0.239, "loss": 0.761, "push": 0.0}, {"total": 14, "dealer_up": 11, "win": 0.282, "loss": 0.718, "push": 0.0}, {"total": 14, "dealer_up": 8, "win": 0.27, "loss": 0.73, "push": 0.0}, {"total": 13, "dealer_up": 4, "win": 0.406, "loss": 0.594, "push": 0.0}, {"total": 13, "dealer_up": 6, "win": 0.424, "loss": 0.576, "push": 0.0}, {"total": 13, "dealer_up": 2, "win": 0.352, "loss": 0.648, "push": 0.0}, {"total": 13, "dealer_up": 3, "win": 0.374, "loss": 0.626, "push": 0.0}, {"total": 13, "dealer_up": 5, "win": 0.417, "loss": 0.583, "push": 0.0}, {"total": 13, "dealer_up": 7, "win": 0.263, "loss": 0.737, "push": 0.0}, {"total": 13, "dealer_up": 8, "win": 0.245, "loss": 0.755, "push": 0.0}, {"total": 13, "dealer_up": 9, "win": 0.211, "loss": 0.789, "push": 0.0}, {"total": 13, "dealer_up": 10, "win": 0.246, "loss": 0.754, "push": 0.0}, {"total": 13, "dealer_up": 11, "win": 0.299, "loss": 0.701, "push": 0.0}, {"total": 12, "dealer_up": 7, "win": 0.315, "loss": 0.685, "push": 0.0}, {"total": 12, "dealer_up": 3, "win": 0.396, "loss": 0.604, "push": 0.0}, {"total": 12, "dealer_up": 4, "win": 0.388, "loss": 0.612, "push": 0.0}, {"total": 12, "dealer_up": 5, "win": 0.423, "loss": 0.577, "push": 0.0}, {"total": 12, "dealer_up": 6, "win": 0.412, "loss": 0.588, "push": 0.0}, {"total": 12, "dealer_up": 2, "win": 0.332, "loss": 0.668, "push": 0.0}, {"total": 12, "dealer_up": 8, "win": 0.231, "loss": 0.769, "push": 0.0}, {"total": 12, "dealer_up": 9, "win": 0.221, "loss": 0.779, "push": 0.0}, {"total": 12, "dealer_up": 10, "win": 0.223, "loss": 0.777, "push": 0.0}, {"total": 12, "dealer_up": 11, "win": 0.327, "loss": 0.673, "push": 0.0}, {"total": 11, "dealer_up": 5, "win": 0.399, "loss": 0.601, "push": 0.0}, {"total": 11, "dealer_up": 4, "win": 0.4, "loss": 0.6, "push": 0.0}, {"total": 11, "dealer_up": 6, "win": 0.481, "loss": 0.519, "push": 0.0}, {"total": 11, "dealer_up": 3, "win": 0.373, "loss": 0.627, "push": 0.0}]}};
    var embed_opt1 = {"mode": "vega-lite"};

    function showError(el, error){
        el.innerHTML = ('<div class="error">'
                        + '<p>JavaScript Error: ' + error.message + '</p>'
                        + "<p>This usually means there's a typo in your chart spec1ification. "
                        + "See the javascript console for the full traceback.</p>"
                        + '</div>');
        throw error;
    }
    const el1 = document.getElementById('vis1');
    vegaEmbed("#vis1", spec1, embed_opt1)
      .catch(error => showError(el, error));
  </script>

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
To make changing the rules of the game easy, I enlisted a package called  [ParamTools](https://paramtools.org/) . ParamTools is a Python library centered around handling parameter processing and validation for computational models. With ParamTools, I was able to set the basic rules of the game as defaults and provide a simple method for changing them to run simulations under different conditions, all while validating any user input.

Take as an example the number of decks used in a game. Using a simple JSON format, I can set the default value for this parameter (`num_decks`) to 8, and set minimum and maximum values used for input validation:

```json
"num_decks": {
    "title": "Number of decks the game will be played with",
    "description": "Number of decks used in the game.",
    "section_1": "Game",
    "section_2": "Deck",
    "type": "int",
    "value": 8,
    "validators": {
        "range": {
            "min": 1,
            "max": 9e+99
        }
    }
}
```

The user can then customize these rules using the format discussed above. Note that this is a rather verbose example of parameter setting. ParamTools allows you to slim this down if you would like.

A major advantage of using ParamTools is that if a user were to try and pass an invalid modification to the rules — such as setting the number of decks to zero — ParamTools will catch this and throw and error so I do not need to write my own code for input validation.

## Closing Thoughts
In short, Py21 is a basic package for running blackjack simulations. It is flexible enough to be tailored for each users needs, while still being powerful enough to run a million simulations in around a minute<sup>1</sup>. At this stage, Py21 is stable and I do not foresee any major changes to its core. Future development will focus on adding new features such as additional graphing capabilities, strategies, and greater data collection. I’m also open to any requests from users.

You can install Py21 using `pip install py21`, or by downloading the source code from [GitHub](https://github.com/andersonfrailey/blackjack).

##### <u>_Footnotes_</u>

<sup>1</sup> The exact amount of time needed to run your simulations depends on how complex your strategies and the number of players involved in the game.  I was able to run a million hands in around a minute with one player using basic strategy.
