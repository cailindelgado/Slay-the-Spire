# Slay the Spire
This was the second assignment from CSSE1001 - Introduction to Software engineering.
---
## Introduction - From provided task sheet
Slay the Spire is a rogue-like deck building card game in which a player must build a deck of cards, which
they use during encounters with monsters. In Assignment 2, you will create an object-oriented text-based game inspired by (though heavily simplified and
altered from) Slay the Spire.


You are required to implement a collection of classes and methods as specified in Section 5 of this document.
Your program’s output must match the expected output exactly; minor differences in output (such as whitespace
or casing) will cause tests to fail, resulting in zero marks for those tests. Any changes to this document will be
listed in a changelog on Blackboard.

## Game Description - From provided task sheet
At the beginning of the game, the user selects a player character; different player characters have different
advantanges and disadvantages, such as starting with higher HP or a better deck of cards. The user then selects
a game file, which specifies the encounters that they will play. After this, gameplay can begin.


During gameplay, the player users a deck of cards to work through a series of encounters with monsters. Each
encounter involves between one and three monsters, which the player must battle in parallel over a series of
turns. At the start of each turn the user draws 5 cards at random from their deck into their hand. Each card
costs between 0 and 3 energy point to play. The user may play as many cards as they like from their hand
during their turn provided they still have the energy points required to play the requested cards. The user opts
to end their turn when they are finished playing cards, at which point the monsters in the encounter each take
an action (which may affect the player’s HP or other stats, or the monster’s own stats). When a card is played
it is immediately sent to the player’s discard pile. At the end of a turn, all cards in the players hand (regardless
of whether they were played that turn) are sent to the discard pile. Cards in the discard pile cannot be drawn until the entire deck has been drawn, at which point the deck is replenished with all the cards from the discard
pile. An encounter ends when either the player has killed all monsters (reduced their HP to 0) or when the
monsters have killed the player (reduced the player’s HP to 0). If the player wins an encounter, an encounter
win message is printed and the next encounter begins. If no more encounters remain, the game terminates with
a game win message, and if the player loses an encounter, the program terminates with a loss message.
