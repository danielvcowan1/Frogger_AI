# Frogger AI

Application of Q Learning on a game of Frogger.

## Written In

Python 3.7.0

## How to Run

Run Qagent.py from command line
```
python ./Qagent.py
```

## Additional Info

When first running the program, please allow a few seconds for the qTable to load the about 1 million values.

### Line 60 and Lines 65-68 of Qagent.py
Line 60 calls qTableData.qTableData. This is the information gathered from a 3 hour training session.
Uncomment Line 60 to observe the partially trained frog go to work.
This Line is initially uncommented and ready to run as is.

Lines 65-68 are initially commented out. To watch a new-born frog learn, uncomment these lines and comment out Line 60.

### Lines 45-49 of constants.py
The reward values on these lines were modified from the original file. 
Using the constants.py provided in this repository is more in line of the qTable values already hard coded in Qagent.py
Running this program with the original constants will result in a running program but might cause the frog performance to degrade or behave undesirably.

### Performance

The program runs as expected without error.
The trained frog here has learned through approximately 3 hours of training and 6000 deaths.
The trained frog acheives 2 homes in a row regularly and 3 homes in a row on occassion.
The trained frog dodges cars with ease and makes it to the river nearly every attempt.
An untrained frog is noticably different after about 5-10 minutes of training in that it begins dodging cars regularly.

### State Representation

There are over 196K states enumerated. A single state is represented by an array self.stateArray of length 9. The 0th index of the array represents wether the frog is in the road (0), middle strip of safe area (1), or river (2). The remaining 8 indeces represent zones surrounding the frog (above left, directly above, above right, directly left, directly right, below left, directly below, below right).  These indeces are marked with a 0 if nothing is in that zone, a 1 if a car is in that zone, a 2 if a log or turtle is in that zone, and a 4 if a home is in that zone. Put simply, a state is the frog looking in its local area and observing what is there. 

The qTable is built with the ~196K states as the columns and 5 actions (up, down, left, right, stay) as the rows. The table is initialized with random values to encourage exploration and random movement at the beginning of the learnign process.

### Exploration vs Exploitation and Reward

The epsilon value used in random exploration is initially set to 0.8. After 250 deaths, this value increases by a factor of epsilon/100. After thousands of deaths, the frog becomes less and less adventurous and relies on previously gained knowlege. This is evidenced by observing the frog take the exact same path many times in a row after a few hours of training and only deviating from that path very rarely.  If I had more time, I would adjust the exploration function because the frog all but gives up on exploring after only getting 3 homes in a row. 

As mentioned above, I adjusted the reward values a lot and in different ways to see how it affected the frogs learning rate. I settled on the these values:

kDeathPenalty=float(-1.0)

kWinLevel=float(+10.0)

kHomeScore=float(+8.0)

kMidPoint=float(+3.0)

kDownMid=float(-3.0)

I adjusted the MidPoint reward to be higher because in the beginning I noticed my frog giving up and hiding in the corner instead of facing the traffic gauntlet after an hour or so of training. After this, I also needed to adjust the HomeScore up above 3 or the frog would have no interest in leaving the safe areas. I noticed that the frog learned to cross the road a lot fast once it acheived the MidPoint reward a few times. With MidPoint reward at the original 0.1, it took the frog about 40-45 minutes to be able to cross the road consistently. With the MidPoint reward set to 3 the frog was consistently crossing the road in the first 10 minutes. With more time, I would like to experiment more with reward adjustment. 
