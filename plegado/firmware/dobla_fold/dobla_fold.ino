/*
 * Dobla — firmware ESP32 para tabla de plegado motorizada
 *
 * Ciclo: pliegue izq → der → inferior → volcado a canasta → home
 *
 * Serial 115200:
 *   FOLD | HOME | STATUS | HELP
 */

#include <ESP32Servo.h>

// ---- Pines ----
static const int PIN_SERVO_L = 18;
static const int PIN_SERVO_R = 19;
static const int PIN_SERVO_B = 21;
static const int PIN_SERVO_TIP = 22;
static const int PIN_BUTTON = 23;  // a GND, INPUT_PULLUP
static const int PIN_LED = 25;

// ---- Ángulos (calibrar en tu mecánica) ----
static int ANGLE_L_OPEN = 20;
static int ANGLE_L_CLOSED = 110;
static int ANGLE_R_OPEN = 160;
static int ANGLE_R_CLOSED = 70;
static int ANGLE_B_OPEN = 20;
static int ANGLE_B_CLOSED = 120;
static int ANGLE_TIP_HOME = 30;
static int ANGLE_TIP_DUMP = 100;

// ---- Tiempos (ms) ----
static const int DELAY_BETWEEN_FOLDS = 450;
static const int DELAY_HOLD_FOLDED = 350;
static const int DELAY_TIP = 900;
static const int DELAY_SETTLE = 400;
static const int MOVE_STEP_MS = 12;
static const int DEBOUNCE_MS = 40;

Servo servoL;
Servo servoR;
Servo servoB;
Servo servoTip;

bool busy = false;
int posL, posR, posB, posTip;

void setLed(bool on) { digitalWrite(PIN_LED, on ? HIGH : LOW); }

void moveServo(Servo &s, int &current, int target) {
  if (current == target) return;
  int step = (target > current) ? 1 : -1;
  while (current != target) {
    current += step;
    s.write(current);
    delay(MOVE_STEP_MS);
  }
}

void goHome() {
  moveServo(servoTip, posTip, ANGLE_TIP_HOME);
  delay(DELAY_SETTLE);
  moveServo(servoB, posB, ANGLE_B_OPEN);
  moveServo(servoL, posL, ANGLE_L_OPEN);
  moveServo(servoR, posR, ANGLE_R_OPEN);
}

void runFoldCycle() {
  if (busy) {
    Serial.println(F("BUSY"));
    return;
  }
  busy = true;
  setLed(true);
  Serial.println(F("FOLD_START"));

  // 1) Pliegues
  moveServo(servoL, posL, ANGLE_L_CLOSED);
  delay(DELAY_BETWEEN_FOLDS);
  moveServo(servoR, posR, ANGLE_R_CLOSED);
  delay(DELAY_BETWEEN_FOLDS);
  moveServo(servoB, posB, ANGLE_B_CLOSED);
  delay(DELAY_HOLD_FOLDED);

  // 2) Volcar a canasta
  moveServo(servoTip, posTip, ANGLE_TIP_DUMP);
  delay(DELAY_TIP);

  // 3) Volver
  goHome();

  Serial.println(F("FOLD_DONE"));
  setLed(false);
  busy = false;
}

void printStatus() {
  Serial.print(F("STATUS busy="));
  Serial.print(busy ? F("1") : F("0"));
  Serial.print(F(" L="));
  Serial.print(posL);
  Serial.print(F(" R="));
  Serial.print(posR);
  Serial.print(F(" B="));
  Serial.print(posB);
  Serial.print(F(" TIP="));
  Serial.println(posTip);
}

void printHelp() {
  Serial.println(F("Dobla ESP32 — comandos: FOLD HOME STATUS HELP"));
}

String readLine() {
  static String buf;
  while (Serial.available()) {
    char c = (char)Serial.read();
    if (c == '\n' || c == '\r') {
      String out = buf;
      buf = "";
      out.trim();
      if (out.length()) return out;
    } else if (buf.length() < 64) {
      buf += c;
    }
  }
  return "";
}

bool buttonPressed() {
  static int lastStable = HIGH;
  static int lastRead = HIGH;
  static unsigned long lastChange = 0;

  int reading = digitalRead(PIN_BUTTON);
  if (reading != lastRead) {
    lastChange = millis();
    lastRead = reading;
  }
  if ((millis() - lastChange) > DEBOUNCE_MS) {
    if (reading != lastStable) {
      lastStable = reading;
      if (lastStable == LOW) return true;  // flanco a pressed
    }
  }
  return false;
}

void setup() {
  Serial.begin(115200);
  delay(200);

  pinMode(PIN_BUTTON, INPUT_PULLUP);
  pinMode(PIN_LED, OUTPUT);
  setLed(false);

  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);

  servoL.setPeriodHertz(50);
  servoR.setPeriodHertz(50);
  servoB.setPeriodHertz(50);
  servoTip.setPeriodHertz(50);

  servoL.attach(PIN_SERVO_L, 500, 2400);
  servoR.attach(PIN_SERVO_R, 500, 2400);
  servoB.attach(PIN_SERVO_B, 500, 2400);
  servoTip.attach(PIN_SERVO_TIP, 500, 2400);

  posL = ANGLE_L_OPEN;
  posR = ANGLE_R_OPEN;
  posB = ANGLE_B_OPEN;
  posTip = ANGLE_TIP_HOME;

  servoL.write(posL);
  servoR.write(posR);
  servoB.write(posB);
  servoTip.write(posTip);

  Serial.println(F("DOBLA_READY"));
  printHelp();
}

void loop() {
  if (buttonPressed()) {
    runFoldCycle();
  }

  String cmd = readLine();
  if (cmd.length()) {
    cmd.toUpperCase();
    if (cmd == "FOLD") {
      runFoldCycle();
    } else if (cmd == "HOME") {
      if (!busy) {
        setLed(true);
        goHome();
        setLed(false);
        Serial.println(F("HOME_DONE"));
      } else {
        Serial.println(F("BUSY"));
      }
    } else if (cmd == "STATUS") {
      printStatus();
    } else if (cmd == "HELP") {
      printHelp();
    } else {
      Serial.print(F("UNKNOWN "));
      Serial.println(cmd);
    }
  }
}
