
String gamemode = "desktop";
int bx, by, board_w, board_h;
int sheight, swidth;
final int startingDiskNum = 3;
int counter=0;

final int GRAY = 1, SILVER = 2, GOLD = 3;
final String[] colors = {"gray", "silver", "gold"};

Board board;
Handler handler;
Game game;
Scoreboard scoreboard;
PVector m = new PVector();

Player emptyPlayer;
Disk   emptyDisk;
Button emptyButton;
Aim    emptyAim;

final int maxplayers = 4;
final float maxalpha = 255;
boolean mouseBlock;

ArrayList<Button> removeFromExe, addToExe, addToBottomExe, buttonsToHide; // buttonsToHide: Hide below the black strip of Board - see at Board: setBoard

/////////////////////////////////////////////////////////////////////////////

void setup() {
  fullScreen();
  //size(1334, 934);
  surface.setResizable(true);
  board_w = board_h = height-5;
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
  Button button = new Button();
  for (int i = handler.executable.size(); i-- > 0;){
    button = handler.executable.get(i);
    if (button.isOver() && button.activated){
      button.pressed = true;
      break;
    }
  }
  //if (gamemode!="desktop") mouseBlock = true;
  //if (!handler.gameStarted || counter>8) return;
  //m.set(mouseX, mouseY);
  //m.set(board.c_to_boardc(m));
  //game.disks.add(new Disk(m.x, m.y, GRAY));
  //++counter;
}

void mousePressed() {
  //if (gamemode!="desktop") mouseBlock = false;
  
}
///////////////////////////////////////////////////////////////////////////

class Timer {
  long starttime;

  void start() { starttime = millis(); }
  long state() { return millis()-starttime; }
  void reset(float with) { starttime = millis()-(int)(state()%with); }
}
