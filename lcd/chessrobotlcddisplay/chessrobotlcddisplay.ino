#include <LiquidCrystal.h>

// Initialize the library with the numbers of the interface pins
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

// Define the pins for the buttons
const int buttonPin1 = 3;
const int buttonPin2 = 4;
const int buttonPin3 = 5;

// global variables
int difficulty = 5;
bool gameStarted = false;
bool lcdGameStarted = false;
bool playerTurn = true; // value only local to arduino
bool serialSent = false;
bool serialReceived = false;
bool playerTurnEnded = false; // value is what is sent and received from pi
bool robotTurnEnded = true; // value is what is sent and recevied from pi
bool abortGame;
bool validMove = false;
bool gameOver;
bool winner; // 0 white, 1 black
bool error = false;

/*
Send to Serial Monitor:
  difficulty
  gameStarted
  playerTurnEnded
  abortGame

Sent from Pi: 
  robotTurnEnded
  gameOver
  validMove
  error
*/

void centerText(String text) {
  int textLength = text.length();
  int spaces = (16 - textLength) / 2; // Calculate the number of spaces needed to center
  clearRow(0);
  lcd.setCursor(spaces, 0); // Set cursor to the calculated position on the first line
  lcd.print(text);
}

// clears specified row
void clearRow(int row){
  lcd.setCursor(0, row);

  for(int i = 0; i < 16; i++){
    lcd.print(" ");
  }
  lcd.setCursor(0, row);
}

// reset back to default settings
void reset(){
  lcdGameStarted = false;
  gameStarted = false;
  playerTurn = true;
  serialSent = false;
  serialReceived = false;
  abortGame = false;
  gameOver = false;
  playerTurnEnded = false;
  robotTurnEnded = false;
  error = false;
}

void setup() {
  // Set up the LCD's number of columns and rows
  lcd.begin(16, 2);

  // initial display and variables
  centerText("KINGS GAMBIT 2.0");
  lcd.setCursor(0, 1);
  lcd.print("-");
  lcd.setCursor(7, 1);
  lcd.print(difficulty);
  lcd.setCursor(15, 1);
  lcd.print("+");
  int difficulty = 5;
  bool gameStarted = false;
  bool lcdGameStarted = false;
  bool playerTurn = true; // value only local to arduino, decides which player moves first
  bool serialSent = false;
  bool serialReceived = false;
  bool playerTurnEnded = false; // value is what is sent and received from pi
  bool robotTurnEnded = true; // value is what is sent and recevied from pi
  bool abortGame = false;
  bool validMove = false;
  bool gameOver = false;

  // Serial
  Serial.begin(9600);

  // Set up the button pins as inputs
  pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);
  pinMode(buttonPin3, INPUT);
}

void loop() {
  int buttonState1 = digitalRead(buttonPin1);
  int buttonState2 = digitalRead(buttonPin2);
  int buttonState3 = digitalRead(buttonPin3);

  // BEFORE GAME START
  if(!lcdGameStarted){
    centerText("KINGS GAMBIT 2.0");
    lcd.setCursor(0, 1);
    lcd.print("-");
    lcd.setCursor(7, 1);
    lcd.print(difficulty);
    lcd.setCursor(15, 1);
    lcd.print("+");
  }
  // Decrease difficulty
  if(!lcdGameStarted && buttonState1 == HIGH){
    if(difficulty > 1) difficulty--;
    clearRow(0);
    centerText("Difficulty");
    lcd.setCursor(7, 1);
    lcd.print(difficulty);
    if(difficulty == 9){
      lcd.setCursor(8, 1);
      lcd.print(" ");
    }
    delay(500);
    centerText("KINGS GAMBIT 2.0");
  }

  // Start Game
  if(!lcdGameStarted && buttonState2 == HIGH){
    lcd.clear();
    centerText("Game Started");
    gameStarted = true;
    lcdGameStarted = true;

    // send over information to pi over serial
    Serial.print(difficulty);
    Serial.print(",");
    Serial.print(gameStarted);
    Serial.print(",");
    Serial.print(playerTurnEnded);
    Serial.print(",");
    Serial.print(abortGame);
    Serial.println();
    delay(500);
  }

  // Increase Difficulty
  if(!lcdGameStarted && buttonState3 == HIGH){
    if(difficulty < 10) difficulty++;
    clearRow(0);
    centerText("Difficulty");
    lcd.setCursor(7, 1);  
    lcd.print(difficulty);
    delay(500);
    centerText("KINGS GAMBIT 2.0");
  }

  // AFTER GAME START: should loop as opponent's or player's turn, dependent on what's received from serial, like which player moves first
  // Player's Turn
  if(lcdGameStarted && playerTurn){
    gameStarted = false;
    clearRow(0);
    centerText("YOUR TURN");
    lcd.setCursor(0, 1);
    lcd.print("ABORT");
    lcd.setCursor(13, 1);
    lcd.print("END");

  }
  // Robot's Turn
  if(lcdGameStarted && !playerTurn){
    gameStarted = false;
    clearRow(0);
    centerText("ROBOT TURN");
    lcd.setCursor(0, 1);
    lcd.print("ABORT");
    lcd.setCursor(13, 1);
    lcd.print("END");
  }

  // ABORT GAME
  if(lcdGameStarted && buttonState1 == HIGH){
    // send to Pi that game has ended
    abortGame = true;
    serialSent = true;

    Serial.print(difficulty);
    Serial.print(",");
    Serial.print(gameStarted);
    Serial.print(",");
    Serial.print(playerTurnEnded);
    Serial.print(",");
    Serial.print(abortGame);
    Serial.println();
    delay(500);
  }

  // Change Difficulty Mid Game (OPTIONAL)
  if(lcdGameStarted && buttonState2 == HIGH){

  }

  // END TURN
  if(lcdGameStarted && playerTurn && buttonState3 == HIGH){
    // indicate that player turn has ended
    playerTurnEnded = true;
    serialSent = true;

    // send over information over serial
    Serial.print(difficulty);
    Serial.print(",");
    Serial.print(gameStarted);
    Serial.print(",");
    Serial.print(playerTurnEnded);
    Serial.print(",");
    Serial.print(abortGame);
    Serial.println();
    delay(1000);
  }

  // OUTPUTS FROM PI

  // Waiting for PI output after PLAYER ends turn
  if(serialSent && playerTurnEnded){
    // display that serial was sent
    clearRow(0);
    clearRow(1);
    // lcd.setCursor(0, 1);
    // lcd.print("ABORT");
    centerText("LOADING");

    // wait until serial is populated of robot's turn
    while(!Serial.available()){
      // buttonState1 = digitalRead(buttonPin1);
      // // abort the game
      // if(buttonState1 == HIGH){
      //   abortGame = true;
      //   serialSent = true;

      //   Serial.print(difficulty);
      //   Serial.print(",");
      //   Serial.print(gameStarted);
      //   Serial.print(",");
      //   Serial.print(playerTurnEnded);
      //   Serial.print(",");
      //   Serial.print(abortGame);
      //   Serial.println();
      //   delay(500);
      //   break;
      // }
    }
    // if abort game, break
    if(!abortGame){
      // check if any data is sent from pi
      Serial.flush();
      String data;
      while(Serial.available() > 0){  
        data = Serial.readStringUntil('\n');
      }
        // parse data into variables
        validMove = data.substring(4, 5).toInt();
        gameOver = data.substring(2, 3).toInt();
        error = data.substring(6, 7).toInt();
    }
    // update serial status
    serialReceived = true;
    serialSent = false;
  }

  // THIS TECHNICALLY NEVER RUNS: Waiting for PI output after robot makes move
  if(serialSent && !playerTurnEnded){
    // display that serial was sent
    clearRow(0);
    clearRow(1);
    centerText("ANALYZING");

    // wait until serial is populated of robot's turn
    while(!Serial.available()){
      // buttonState1 = digitalRead(buttonPin1);
      // // abort the game
      // if(buttonState1 == HIGH){
      //   abortGame = true;
      //   serialSent = true;

      //   Serial.print(difficulty);
      //   Serial.print(",");
      //   Serial.print(gameStarted);
      //   Serial.print(",");
      //   Serial.print(playerTurnEnded);
      //   Serial.print(",");
      //   Serial.print(abortGame);
      //   Serial.println();
      //   delay(500);
      //   break;
      // }
    }

    // check if any data is sent from pi
    Serial.flush();
    String data;
    while(Serial.available() > 0){
      data = Serial.readStringUntil('\n');
    } 
      // parse data into variables
      robotTurnEnded = data.substring(0, 1).toInt();
      gameOver = data.substring(2, 3).toInt();

      // update serial status
      serialReceived = true;
      serialSent = false;
      delay(500);
  }

  // ERROR: if picture or other error is bad, restart player's turn
  if(error){
    // display
    clearRow(0);
    clearRow(1);
    centerText("SYSTEM ERROR");

    // restart to player's turn
    playerTurn = true;
    serialReceived = false;
    validMove = false;
    gameOver = false;
    error = false;
    delay(1000);
  }

  // ABORT GAME FROM SERIAL: pi successfully reads and sends back aborting the game
  if(abortGame && serialReceived){
    // display
    clearRow(0); 
    clearRow(1);
    centerText("GAME ABORTED");
    abortGame = false;
    delay(2000);

    // set to default menu settings
    reset();
  }

  // MOVE NOT VALID FROM SERIAL: output lcd not valid move and 
  if(lcdGameStarted && playerTurnEnded && serialReceived && !validMove){
    clearRow(0);
    clearRow(1);

    // player goes again
    playerTurn = true;
    robotTurnEnded = false;
    serialReceived = false;

    centerText("INVALID MOVE");
    delay(1000);
  }
  
  // MOVE VALID FROM SERIAL: player's turn is over and game continues
  if(lcdGameStarted && playerTurnEnded && serialReceived && validMove){
    clearRow(0);
    clearRow(1);
    
    // player goes since robot has already done their turn
    validMove = false;
    playerTurn = true;
    serialReceived = false;

    centerText("VALID MOVE");
    delay(1000);
  }

  // ROBOT TURN ENDS FROM SERIAL:
  if(lcdGameStarted && serialReceived && robotTurnEnded){
    centerText("ROBOT TURN END");
    playerTurn = true;
    robotTurnEnded = false;
    serialReceived = false;
    delay(1000);
  }

  // GAME OVER
  if(gameOver && serialReceived){
    if(winner == 0) centerText("WHITE WINS");
    else centerText("BLACK WINS");
    serialReceived = false;
    delay(1000);
    reset();
  }

  // if (Page == 1){
  //   centerText("KINGS GAMBIT 2.0");

  //   lcd.setCursor(0, 1);
  //   lcd.print("START");

  //   lcd.setCursor(7,1);
  //   lcd.print("L:");
  //   if (difficulty < 10){
  //     lcd.blink();
  //     lcd.print(0);
  //     lcd.print(difficulty);
  //   } else{
  //     lcd.print(difficulty);
  //   }

  //   lcd.setCursor(13, 1);
  //   lcd.print("SET");

  //   if (buttonState1 == HIGH){
  //     Page = 2;
  //     lcd.clear();
  //     delay (400);
  //   }
  //   if (buttonState3 == HIGH){
  //     Page = 3;
  //     delay (200);
  //     lcd.clear();
  //     delay (400);
  //   }
  // }

  // if (Page == 2){
  //   centerText("Game Started");
  // }

  // if (Page == 3){
  //   delay (100);
  //   lcd.setCursor(4, 0);
  //   lcd.print("Level:");

  //   if (difficulty < 10){
  //     lcd.blink();
  //     lcd.print(0);
  //     lcd.print(difficulty);
  //   } else{
  //     lcd.print(difficulty);
  //   }
    
  //   lcd.setCursor(0, 1);
  //   lcd.print("LVL+");

  //   lcd.setCursor(6, 1);
  //   lcd.print("HOME");

  //   lcd.setCursor(12, 1);
  //   lcd.print("LVL-");

  //   if (buttonState1 == HIGH){
  //     if (difficulty < 10){
  //       difficulty = difficulty + 1;
  //       delay (300);
  //     }
  //   }
  //   if (buttonState3 == HIGH){
  //     if (difficulty > 1){
  //       difficulty = difficulty - 1;
  //       delay (300);

  //     }
  //   }
  //   if (buttonState2 == HIGH){
  //     Page = 1;
  //     lcd.clear();
  //     delay(300);
  //   }
  // }
}