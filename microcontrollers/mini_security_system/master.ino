#include <LiquidCrystal_I2C.h>
#include <Keypad.h>

const byte rows = 4; 
const byte cols = 4;
const byte password_length = 5;
byte password_index = 0;
byte trail_counter = 0;
const char correct_password[password_length + 1] = "ABC85";
char entered_password[password_length + 1];


const char hexa_keys[rows][cols] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

byte row_pins[rows] = {9, 8, 7, 6}; 
byte col_pins[cols] = {5, 4, 3, 2}; 

Keypad password_keypad = Keypad(makeKeymap(hexa_keys), row_pins, col_pins, rows, cols); 
LiquidCrystal_I2C lcd(0x21, 16, 2);

void setup(){
  Serial.begin(9600);
  lcd.backlight();
  lcd.init();
  lcd.setCursor(0,0);
  lcd.print("Enter Password:");
}

void loop(){
  char pressed_key;
  while (password_index < password_length){
    pressed_key = password_keypad.getKey();
    if(pressed_key){
      entered_password[password_index] = pressed_key;
      lcd.setCursor(password_index, 1);
      lcd.print('*');
      password_index++;
    }
  }
  if (!strcmp(entered_password, correct_password)){
    Serial.println("OK");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Access Granted");
    delay(5000);
    lcd.setCursor(0,0);
 	lcd.print("Enter Password: ");
  	password_index = 0;
  } else {
    trail_counter++;
    if (trail_counter >= 3){
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Access Denied");
      delay(5000);
      lcd.clear();
      lcd.print("Try Again");
      delay(2000);
      lcd.clear();
      lcd.print("Enter Password:");
      password_index = 0;
    }
  }
}
