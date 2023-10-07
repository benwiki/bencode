
String gamemode = "destop";
int bx, by, board_w, board_h;
int sheight, swidth;

Board board;
Handler handler;
Game game;
Scoreboard scoreboard;

Player emptyPlayer;
Disk   emptyDisk;
Button emptyButton;
Aim    emptyAim;

int maxplayers = 4;
//int diskcounter = 0;
float maxalpha = 255;
boolean mouseBlock;

ArrayList<Button> removeFromExe, addToExe, addToBottomExe, buttonsToHide; // buttonsToHide: Hide below the black strip of Board - see at Board: setBoard

/////////////////////////////////////////////////////////////////////////////

void setup() {
  //fullScreen();
  size(1334, 934);
  //surface.setResizable(true);
  board_w = board_h = height-10;
  bx = by = 5;

  board       = new Board(bx, by, board_w, board_h);

  emptyPlayer = new Player();
  emptyDisk   = new Disk();
  emptyAim    = new Aim();
  emptyButton = new Button();

  handler     = new Handler();
  game        = new Game();
  scoreboard  = new Scoreboard();

  /*if (gamemode == "desktop") mouseBlock = false;
   else mouseBlock = true;*/
  removeFromExe = new ArrayList<Button>();
  addToBottomExe = new ArrayList<Button>();
  addToExe = new ArrayList<Button>();
  buttonsToHide = new ArrayList<Button>();
  
  textAlign(CENTER, CENTER);
}

///////////////////////////////////////////////////////////////////////////

void draw() {
  background(0);
  if (handler.basicGameOperationDone) board.update();
  handler.execute_all();
}

////////////////////////////////////////////////////////////////////////////

void mouseReleased() {
  for (Button button : handler.executable)
    if (button.isOver() && button.activated)
      button.pressed = true;
  //if (gamemode!="desktop") mouseBlock = true;
}

void mousePressed() {
  //if (gamemode!="desktop") mouseBlock = false;
}
///////////////////////////////////////////////////////////////////////////

class Timer {
  long starttime;

  void start() {
    starttime = millis();
  }

  long state() {
    return millis()-starttime;
  }
}
