"""
Code for creating plots found in 'Introduction to Py21'
"""
import random
from py21 import Game, Player
from py21.utils import result_heatmap, outcome_bars
from py21.strategies import hit_to_seventeen
from embedplots import add_plots
from pathlib import Path


CUR_PATH = Path(__file__).resolve().parent
random.seed(409)

bankroll = 1000000
# create first player
player = Player(bankroll)
# first game
game = Game([player])
rounds = 1000000
game.simulate(rounds)

# create heatmap
heat = result_heatmap(player.history, result="win",
                      title="Winning Pct")
heat_path = Path(CUR_PATH, "heatmap.html")
heat.save("heatmap.html")
heat.save("../images/heatmap.json")

# second game
player = Player(bankroll)
player2 = Player(bankroll, strategy_func=hit_to_seventeen)

game2 = Game([player, player2])
game2.simulate(rounds)
# create outcome bar graph
outcome = outcome_bars([player.history, player2.history],
                       name=["Basic Strategy", "Hit to 17"])
outcome_path = Path(CUR_PATH, "outcome.html")
outcome.save("outcome.html")

# add graphs to markdownfiles
template = Path(CUR_PATH, "content", "Intro_to_Py21_template.md")
pathout = Path(CUR_PATH, "..", "_mdcontent", "intro_to_py21.md")
plots = {
    "heatmap": heat_path,
    "outcomebars": outcome_path
}
add_plots(pathout, template, plots, altair=True)

# remove HTML files
heat_path.unlink()
outcome_path.unlink()
