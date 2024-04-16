#include <LiquidCrystal.h>

// Initialize the library with the numbers of the interface pins
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

// Define the pins for the buttons
const int buttonPin1 = 3;
const int buttonPin2 = 4;
const int buttonPin3 = 5;

// global variables
int Page = 1;
int difficulty = 5;
bool gameStarted = false;
bool playerTurn = true; // value only local to arduino
bool serialSent = false;
bool serialReceived = false;
bool playerTurnEnded = false; // value is what is sent and received from pi
bool robotTurnEnded = true; // value is what is sent and recevied from pi
bool abortGame;
bool validMove = false;

/* 
Send to Serial Monitor:
  difficulty
  gameStarted
  playerTurnEnded
  abortGame

Sent from Pi:
  validMove
  robotTurnEnded
  gameOver
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
  if(!gameStarted){
    centerText("KINGS GAMBIT 2.0");
    lcd.setCursor(0, 1);
    lcd.print("-");
    lcd.setCursor(7, 1);
    lcd.print(difficulty);
    lcd.setCursor(15, 1);
    lcd.print("+");
  }
  // Decrease difficulty
  if(!gameStarted && buttonState1 == HIGH){
    if(difficulty > 1) difficulty--;
    clearRow(0);
    centerText("Difficulty");
    lcd.setCursor(7, 1);
    lcd.print(difficulty);
    delay(500);
    centerText("KINGS GAMBIT 2.0");
  }

  // Start Game
  if(!gameStarted && buttonState2 == HIGH){
    lcd.clear();
    centerText("Game Started");
    gameStarted = true;

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
  if(!gameStarted && buttonState3 == HIGH){
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
  if(gameStarted && playerTurn){
    clearRow(0);
    centerText("YOUR TURN");
    lcd.setCursor(0, 1);
    lcd.print("ABORT");
    lcd.setCursor(13, 1);
    lcd.print("END");

  }
  // Robot's Turn
  if(gameStarted && !playerTurn){
    clearRow(0);
    centerText("ROBOT TURN");
    lcd.setCursor(0, 1);
    lcd.print("ABORT");
    lcd.setCursor(13, 1);
    lcd.print("END");
  }

  // ABORT GAME
  if(gameStarted && buttonState1 == HIGH){
    // send to Pi that game has ended
    playerTurn = false;
    abortGame = true;
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
  if(gameStarted && buttonState2 == HIGH){

  }

  // END TURN
  if(gameStarted && playerTurn && buttonState3 == HIGH){
    // indicate that player turn has ended
    playerTurnEnded = true;

    // send over information over serial
    Serial.print(difficulty);
    Serial.print(",");
    Serial.print(gameStarted);
    Serial.print(",");
    Serial.print(playerTurnEnded);
    Serial.print(",");
    Serial.print(abortGame);
    Serial.println();
  }

  // OUTPUTS FROM PI

  // Waiting for PI output after player ends turn
  if(serialSent && playerTurnEnded){
    // check if any data is sent from pi
    if(Serial.available() > 0){
      String data = Serial.readStringUntil('\n');

      // parse data into variables
      serialReceived = true;
      serialSent = false;
    }
  }

  // Waiting for PI output after robot makes move
  if(serialSent && !playerTurnEnded){
    // check if any data is sent from pi
    if(Serial.available() > 0){
      String data = Serial.readStringUntil('\n');
      
      // parse data into variables
      serialReceived = true;
      serialSent = false;
    }
  }

  // ABORT GAME: pi successfully reads and sends back aborting the game
  if(abortGame){ // TODO: change conditional based on pi output
    // set to default menu settings
    abortGame = false;
    gameStarted = false;
    difficulty = 5;
    
    // display
    clearRow(0); 
    clearRow(1);
    centerText("GAME ABORTED");
    delay(2000);
  }

  // MOVE NOT VALID: output lcd not valid move and 
  if(gameStarted && playerTurnEnded && serialReceived && !validMove){
    clearRow(0);
    clearRow(1);

    // player goes again
    playerTurn = true;
    robotTurnEnded = false;
    serialReceived = false;

    centerText("INVALID MOVE");
    delay(1000);
  }
  
  // MOVE VALID: player's turn is over and game continues
  if(gameStarted && playerTurnEnded && serialReceived && validMove){
    clearRow(0);
    clearRow(1);
    
    // robot's turn
    validMove = false;
    playerTurn = false;
    serialReceived = false;

    centerText("VALID MOVE");
    delay(1000);
  }

  // ROBOT TURN ENDS:
  if(gameStarted && serialReceived && robotTurnEnded){
    playerTurn = true;
    robotTurnEnded = false;
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