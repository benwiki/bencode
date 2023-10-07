
/*/////////////////////////////
*****POSSIBLE IMPROVEMENTS*****
1. Ha nem tud sehova lépni -> placeaimet kap, megy a zöldre
/*/


/*///////////////////////
*****DEBUGGING NOTES*****
a pushout button működése nem jó
/*/

/*/////////////////////////
*****IMPROVEMENTS MADE*****
~2020.12.19-20.
Elintéztem a disc_countereket, meg a sarcolást kezdtem el
Indicator már nem indul el ha kitolsz valamit.

~2020.12.18.
Mükszik az indicatoros cucc-ság - majdnem tökéletesen hülyebiztos - játék előtt még lehet szerepe

~2020.12.17-18.
Mükszik a graveyard

~2020.11.08.
Minden bound cucc visszaállítása, de majd csináld már meg normálisan!

~2020.07.22-23.
Yeah, graveyard. I fixed some bugs... I continued to work with it... yeah.

~2020.07.21-22.
Ducked things up around "graveyard"...
Need to finish it.
Also made empty objects, so I don't give so much work to the java garbage collector

~2020.07.14-15.
Created "Indicator" class to show the next player, and the possible clickable disks/players
It isn't ready yet...

~2020.07.13.
Finished the work with the "playerstate" button
Rearranged a couple of things around the Handler and Game class

~2020.07.12.
Started to make the "playerstate" button (in Scoreboard) to show who's the current player, and whether it has taken it's move.

~2020.07.08.
Created "Sign" class, to manage signs easier in "Button" class

~ ...
added "Scoreboard" and "Score" class to manage scoreboard easier

/*/

/*************************************************************************************************************************************************************************************
 *  Game developed by Benke Hargitai
 *  A Desktop representation of the existing "Repello" board game
 * 
 *  How the script functions:
 *
 *  - the "Handler" class is responsible for all the main action of the game, it's where the EN[szálak összefutnak]
 *    - the "executable" array is responsible for the buttons to be visible and active
 *      + in that, we check, whether a button is pressed, if that happens, we determine the type of the button,
 *      + that was pressed, and run the commands associated with that type ("check_command" function)
 *    - the "exetute_all" function is responsible for handling the "executable", and the adding & removing arrays ("removeFromExe", "addToExe", "addToBottomExe"),
 *      handling the gamestarter button, and also running the game itself ("check_game" function gets called here)
 *    - "check_game" function
 *      + there are "events" - there is definitely a more professional way to do this, but now it works so:
 *        the events (clearExecutable, gameWillStart, basicGameOperationDone, gameStarted) are there for managing the actions
 *
 *  - the "Game" class is responsible for all the stuff required for the actual game itself. The disks, players and the "scoreboard" communicate through this class.
 *    - "check_cursor" function: 
 *        + sets the disk or player under your cursor smaller - in order to make the color circles visible underneath. 
 *        + Also manages the "placeaim", which is required for placing the players on the board.
 *    - "find_goals" function: 
 *        + sets Aims for the player that the user clicked on - when it's a new turn.
 *    - "find_tensioned_goals" fuction:
 *        + sets Aims for the disk or player that the user clicked on - when the actual player has done it's step, and tensions were created
 *    - "has_tensions" function:
 *        + returns true if any tension appears to be on the board - false otherwise
 *    - "set_scoreboard" function:
 *        + sets up the scoreboard
 *    - "leave_disk" function:
 *        + leaves a disk behind the player who's taking a step
 *    - "set_pushout_button", "delete_pushout_button", "push_out" functions:
 *        + they manage the button with that you can push out a button or a player
 *
 *  - the "Board" class is responsible for handling the stuff happening with the board. More important things:
 *    - buttons in "buttonsToHide" array gets executed here in order to hide them under a black stripe (the scoreboard's place)
 *
 *  - the "Scoreboard" class is responsible for managing the disks the players gathered.
 *
 *  The other classes are just items of the game (Button (Sign), Aim, Player, Disk)
 *  Explore them yourself
 **********************************************************************************************************************************************************************/
