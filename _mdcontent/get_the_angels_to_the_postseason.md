# Can We Get the 2022 Angels to the Postseason?

To date, the best thing about the Angels' year has been their City Connect jerseys.
Despite having two of the best players in baseball in Mike Trout and Shohei Ohtani,
they are 10.5 games out of the Wild Card race, and 20.5 in the division. In an
effort to see if their season was truly lost, I set out to find a series of trades
that would give them at least a 50% chance of making the postseason according
to Satchel, my MLB projections model.

I gave myself two constraints on the trades I could make. First, Ohtani and Trout
could not be traded. Second, I could only make trades that were approved in the
[Baseball Trade Values Trade Simulator](https://www.baseballtradevalues.com/trade-simulator/).
All trade values mentioned in the rest of this article were taken from the trade
simulator.

Trying to determine which teams consider themselves sellers at the deadline
and which front offices are willing to give up major league talent for prospects
is beyond the scope of this project, though I did initially attempt to trade primarily with
teams out of the playoff races. However, I eventually reached a point where I needed to trade
with teams that were ahead of the Angels in the Wild Card (Seattle
and Tampa Bay) both to make the Angels better and to make the competition worse.
As a result, some of the trades got a little ridiculous.
Additionally, I had to rely a lot on adding cash to make deals happen. This was partially
because the trade simulator has a cap on the number of players that can be included
in a trade, and partially because I simply ran out of high value players in the
Angels' system to trade.
With that in mind, here are the six deals I made.


## Trade 1: Washington Nationals

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: center;">
      <th>Angels Get</th>
      <th>Nationals Get</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1B Josh Bell</td>
      <td>2B Michael Stephanic</td>
    </tr>
    <tr>
      <td></td>
      <td>3B Jonathan Villar</td>
    </tr>
    <tr>
      <td></td>
      <td>3B Werner Blakely (Low-A - #21 Prospect)</td>
    </tr>
  </tbody>
</table>

The goal of this first trade was to upgrade the bat at first base. Bell brings
a 148 wRC+ to the lineup, compared to Jared Walsh's 93. Additionally, Walsh has
a fairly high trade value, so I assumed I would have to move him at some point
to shore up other weaknesses in the roster, leaving space in the lineup for Bell.

I was able to successfully construct a trade for Juan Soto that involved the Angels
taking on Stephen Strasburg's contract and sending over many of their top prospects.
However, I needed those prospect to make other deals, so I decided against making it.

This trade added a couple of wins to the projected total, leaving plenty
more work to be done.

![Trade 1 results](../images/trade1_win_dist_angels.png)

## Trade 2: Chicago Cubs

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: center;">
      <th>Angels Get</th>
      <th>Cubs Get</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>C Willson Contreras</td>
      <td>C Max Stassi</td>
    </tr>
    <tr>
      <td>2B Nico Hoerner</td>
      <td>RP Jose Quijada</td>
    </tr>
    <tr>
      <td></td>
      <td>SS Arol Vera (Low-A - #2 Prospect)</td>
    </tr>
    <tr>
      <td></td>
      <td>SP Ky Bush (AA - #4 Prospect)</td>
    </tr>
    <tr>
      <td></td>
      <td>SP Mason Erla (AA - #22 Prospect)</td>
    </tr>
    <tr>
      <td></td>
      <td>$4 Million</td>
    </tr>
  </tbody>
</table>

This is the first of many trades where I threw some money in to fill the gap in
value. Contreras is an obvious upgrade at catcher and very likely to be available, while
Hoerner fills the gap at second left by the Stephanic trade. I did have to give
up a couple of highly ranked prospect to complete the deal, but given the singular goal
of getting the Angels to the postseason this year, it was worth it.

![Trade 2 results](../images/trade2_win_dist_angels.png)

## Trade 3: Cincinnati Reds

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: center;">
      <th>Angels Get</th>
      <th>Reds Get</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SP Louis Castillo</td>
      <td>1B Jarded Walsh</td>
    </tr>
    <tr>
      <td>2B Mike Moustakas</td>
      <td>OF Jordyn Adams (AA - #6 prospect)</td>
    </tr>
    <tr>
      <td>OF Nick Senzel</td>
      <td>C Edgar Quero (Low A - #8 prospect)</td>
    </tr>
  </tbody>
</table>

This trade was interesting, because it basically boiled down to being willing to
eat Moustakas' massive contract and barely replacement level play in order to land
Castillo and Senzel. Moustakas' -27.6 trade value offset most of Castillo's 41.2
value, making it possible to put together a solid prospect package for a needed
starter.

![Trade 3 results](../images/trade3_win_dist_angels.png)

## Trade 4: Seattle Mariners

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: center;">
      <th>Angels Get</th>
      <th>Mariners Get</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>OF Julio Rodriguez</td>
      <td>OF Brandon Marsh</td>
    </tr>
    <tr>
      <td>SP Robbie Ray</td>
      <td>SP Patrick Sandoval</td>
    </tr>
    <tr>
      <td></td>
      <td>SS Denzer Guzman (High-A - #5 prospect)</td>
    </tr>
    <tr>
      <td></td>
      <td>SS Jeremiah Jackson (AA - #7 prospect)</td>
    </tr>
    <tr>
      <td></td>
      <td>$10 Million</td>
    </tr>
  </tbody>
</table>

As mentioned earlier, I quickly realized that given talent constraints both on the
market and in the Angels' system, I needed to make some trades that would weaken
teams ahead of the Angels, even if they were a bit ridiculous. This
is one of those ridiculous trades. There is no real chance Seattle actually trades Julio
Rodriguez. However, based
on trade values, it is theoretically possible. I once again had to take on a player
with highly negative trade value in Robbie Ray to make the trade happen. Add in the #5
and #7 prospects in the Angels' system according to MLB.com, and what amounts to
a $10 million bribe to not win this year, and you have a deal.

Compared to the three previous trades, the marginal effect on playoff odds is
huge because it significantly weakens the Mariners lineup.

![Trade 4 results](../images/trade4_win_dist_angels.png)

## Trade 5: Tampa Bay Rays

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: center;">
      <th>Angels Get</th>
      <th>Rays Get</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>RP Pete Fairbanks</td>
      <td>RP Austin Warren</td>
    </tr>
    <tr>
      <td>RP J.P. Feyereisen</td>
      <td>RP Andrew Wantz</td>
    </tr>
    <tr>
      <td>OF Kevin Kiermair</td>
      <td>OF Jo Adell</td>
    </tr>
    <tr>
      <td></td>
      <td>OF Orlando Martinez (AA)</td>
    </tr>
    <tr>
      <td></td>
      <td>$7 Million</td>
    </tr>
  </tbody>
</table>

Trade number five served two purposes. First, it weakened a competitor. Second,
it added some depth to a bullpen that, according to Baseball-Reference's
[Wins Above Average positional table](https://www.baseball-reference.com/leagues/majors/2022.shtml#all_team_output), is the third worst in the majors. Trading Jo Adell also
frees up room on the roster for the other outfielders I picked up. The $7 million
in cash is another bribe for the Rays to throw in the towel on this season.

![Trade 5 results](../images/trade5_win_dist_angels.png)

## Trade 6: Seattle Mariners

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: center;">
      <th>Angels Get</th>
      <th>Mariners Get</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SP Logan Gilbert</td>
      <td>OF Taylor Ward</td>
    </tr>
    <tr>
      <td>SS J.P. Crawford</td>
      <td>SS Luis Rengifo</td>
    </tr>
    <tr>
      <td>2B Adam Frazier</td>
      <td>SP José Suarez</td>
    </tr>
    <tr>
      <td>3B Eugenio Suárez</td>
      <td>1B David MacKinnon</td>
    </tr>
    <tr>
      <td></td>
      <td>INF Andrew Velazquez</td>
    </tr>
    <tr>
      <td></td>
      <td>SP Janson Junk (AAA - #10 Prospect)</td>
    </tr>
    <tr>
      <td></td>
      <td>$10 Million</td>
    </tr>
  </tbody>
</table>

In the final trade, I steal from the Mariners again. This trade was interesting
because Eugenio Suárez has a -13.6 trade value despite putting together a solid
season so far. This offset some value coming from Crawford and Gilbert (40.6 and
54.5, respectively) while giving me a replacement for Villar at third and taking
a bat away from a team ahead in the standings.

The marginal impact of this trade was huge. Turns out when you take three starters
and a key piece of the rotation from one team and give it to a division rival,
they don't perform well over the rest of the season.


## Final Lineup

After all of that, here is the new starting lineup and rotation for the Angels:

![New Lineup](../images/realisticlineup_angels.png)

With Frazier, Moustakas, and Kiermair on the bench.

I do not claim this is the only, or event the best, way to get the Angels to the
postseason. But with this team, the Angels project to go 47-23 in the final 70
games of the year, increasing the probability they make the postseason to 52.43%.

![Final Projections](../images/real_win_dist_angels.png)

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>Team</th>
      <th>Wins to Date</th>
      <th>Losses to Date</th>
      <th>Wins RoS</th>
      <th>Losses RoS</th>
      <th>Projected Wins</th>
      <th>Projected Losses</th>
      <th>Make Playoffs (%)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>LAA</td>
      <td>39</td>
      <td>53</td>
      <td>47</td>
      <td>23</td>
      <td>86</td>
      <td>76</td>
      <td>52.43</td>
    </tr>
  </tbody>
</table>

## Takeaways

What have we learned? It is technically not impossible for the Angels to make
the postseason this year. All they need to do is trade nine of their top 25
prospects and send $31 million to other teams to make it happen. This would of
course require a few GMs losing their mind and accepting trades that
would alienate the fan base and almost certainly cost them their jobs. So, unfortunately
for Angels fans, they will probably need to wait a bit longer to see October
baseball.

## Other Simulations

For fun, I also simulated what would happen if the Angels swapped their starting
lineup with the AL All Stars, and what
would happen if they swapped their entire roster for the current MLB WAR leaders
in each position (again only keeping Trout and Ohtani in both cases).
Unsurprisingly, they become World Series favorites in both
scenarios and project to dominate the second half.

### All Stars Simulation

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: center;">
      <th>Angels</th>
      <th>All Stars</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Jared Walsh</td>
      <td>Vladimir Guerrero (TOR)</td>
    </tr>
    <tr>
      <td>Michael Stefanic</td>
      <td>Andres Gimenez (CLE)</td>
    </tr>
    <tr>
      <td>Jonathan Villar</td>
      <td>Rafael Devers (BOS)</td>
    </tr>
    <tr>
      <td>Luis Rengifo</td>
      <td>Tim Anderson (CHW)</td>
    </tr>
    <tr>
      <td>Brandon Marsh</td>
      <td>Aaron Judge (NYY)</td>
    </tr>
    <tr>
      <td>Taylor Ward</td>
      <td>Giancarlo Stanton (NYY)</td>
    </tr>
    <tr>
      <td>Max Stassi</td>
      <td>Alejandro Kirk (TOR)</td>
    </tr>
  </tbody>
</table>



With all the All Star position players, the Angels would have the starting
lineup and pitching staff below.

![All Star Lineup](../images/allstarlineup_angels.png)

A team full of All Stars wins. A lot. If this were to happen,
the Angels would immediately become World Series favorites and be about as certain
to make the postseason as possible.I haven't been able to find the highest second-half winning
percentages in MLB history, but it seems like a safe bet that the .742 rate this
team is projected for would be near the top of that list.

![All Star Wins Distribution](../images/allstar_win_dist_angels.png)

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: center;">
      <th>Team</th>
      <th>Wins to Date</th>
      <th>Losses to Date</th>
      <th>Wins RoS</th>
      <th>Losses RoS</th>
      <th>Projected Wins</th>
      <th>Projected Losses</th>
      <th>Make Playoffs (%)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>LAA</td>
      <td>39</td>
      <td>53</td>
      <td>52</td>
      <td>18</td>
      <td>91</td>
      <td>71</td>
      <td>78.74</td>
    </tr>
  </tbody>
</table>

### WAR Leaders Simulation

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: center;">
      <th>Angels</th>
      <th>WAR Leader</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Jared Walsh</td>
      <td>Paul Goldschmidt (STL)</td>
    </tr>
    <tr>
      <td>Michael Stefanic</td>
      <td>Tommy Edman (STL)</td>
    </tr>
    <tr>
      <td>Jonathan Villar</td>
      <td>Nolan Arenado (STL)</td>
    </tr>
    <tr>
      <td>Luis Rengifo</td>
      <td>Dansby Swanson (ATL)</td>
    </tr>
    <tr>
      <td>Brandon Marsh</td>
      <td>Yordan Alvarez (HOU)</td>
    </tr>
    <tr>
      <td>Taylor Ward</td>
      <td>Aaron Judge (NYY)</td>
    </tr>
    <tr>
      <td>Max Stassi</td>
      <td>Alejandro Kirk (TOR)</td>
    </tr>
    <tr>
      <td>Reid Detmers</td>
      <td>Sandy Alcantara (MIA)</td>
    </tr>
    <tr>
      <td>Patrick Sandoval</td>
      <td>Carlos Rodon (SFG)</td>
    </tr>
    <tr>
      <td>Jose Suarez</td>
      <td>Kevin Gausman (TOR)</td>
    </tr>
    <tr>
      <td>Noah Syndergaard</td>
      <td>Aaron Nola (PHI)</td>
    </tr>
    <tr>
      <td>Raisel Iglesias</td>
      <td>Ryan Helsley (STL)</td>
    </tr>
    <tr>
      <td>Ryan Tepera</td>
      <td>Edwin Diaz (NYM)</td>
    </tr>
    <tr>
      <td>Aaron Loup</td>
      <td>Michael King (NYY)</td>
    </tr>
    <tr>
      <td>Jose Quijada</td>
      <td>Devin Williams (MIL)</td>
    </tr>
    <tr>
      <td>Austin Warren</td>
      <td>A.j. Minter (ATL)</td>
    </tr>
    <tr>
      <td>Andrew Wantz</td>
      <td>Clay Holmes (NYY)</td>
    </tr>
    <tr>
      <td>Jose Marte</td>
      <td>Reynaldo Lopez (CHW)</td>
    </tr>
    <tr>
      <td>Jaime Barria</td>
      <td>Taylor Rogers (SDP)</td>
    </tr>
    <tr>
      <td>Elvis Peguero</td>
      <td>Anthony Bass (MIA)</td>
    </tr>
  </tbody>
</table>



Giving the Angels all the MLB WAR leaders at every position (including the pitching
staff) makes them a juggernaut.

![WAR Leaders Lineup](../images/warlineup_angels.png)

Not only would this make them a lock to get into the postseason, but it would
actually make them a 97 win team thanks to a 58-12 second half. That winning
percentage over a full season would be the highest ever, amounting to 134 wins.

![WAR wins distribution](../images/war_win_dist_angels.png)

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: center;">
      <th>Team</th>
      <th>Wins to Date</th>
      <th>Losses to Date</th>
      <th>Wins RoS</th>
      <th>Losses RoS</th>
      <th>Projected Wins</th>
      <th>Projected Losses</th>
      <th>Make Playoffs (%)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>LAA</td>
      <td>39</td>
      <td>53</td>
      <td>58</td>
      <td>12</td>
      <td>97</td>
      <td>65</td>
      <td>97.65</td>
    </tr>
  </tbody>
</table>