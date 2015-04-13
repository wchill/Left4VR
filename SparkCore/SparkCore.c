TCPClient client;
byte server[] = { 192, 168, 137, 1 };
long t;
bool connected;
int prevFlex1;
int prevFlex2;
int threshold = 3250;
int threshold2 = 3450;

void setup()
{
    // Make sure your Serial Terminal app is closed before powering your Core
    Serial.begin(9600);
    pinMode(A0, INPUT_PULLDOWN);
    pinMode(A1, INPUT_PULLDOWN);
    pinMode(D0, OUTPUT);
    pinMode(D1, OUTPUT);
    digitalWrite(D0, HIGH);
    digitalWrite(D1, HIGH);
    SPARK_WLAN_Loop();
    setIP(ipString);

    Serial.println("connecting...");

    if (client.connect(server, 8000))
    {
        Serial.println("connected");
        connected = true;
    }
    else
    {
        Serial.println("connection failed");
        connected = false;
    }
    t = millis();
    prevFlex1 = 3800;
    prevFlex2 = 3800;
}

void loop()
{
    if(connected) {
        if (client.available())
        {
            char c = client.read();
            Serial.print(c);
        }

        if(t - millis() > 10) {
            int flex1 = analogRead(A0);
            int flex2 = analogRead(A1);
            //Serial.print(flex1, DEC);
            //Serial.print(" ");
            //Serial.println(flex2, DEC);

            if(flex1 < threshold && prevFlex1 > threshold) {
                client.println("G11");
                Serial.print("G11 ");
                Serial.println(flex1, DEC);
            } else if(flex1 > threshold && prevFlex1 < threshold) {
                client.println("G10");
                Serial.print("G10 ");
                Serial.println(flex1, DEC);
            }
            if(flex2 < threshold2 && prevFlex2 > threshold2) {
                client.println("G21");
                Serial.print("G21 ");
                Serial.println(flex2, DEC);
            } else if(flex2 > threshold2 && prevFlex2 < threshold2) {
                client.println("G20");
                Serial.print("G20 ");
                Serial.println(flex2, DEC);
            }
            prevFlex1 = flex1;
            prevFlex2 = flex2;

            /*
            add other fingers if needed
            int flex3 = analogRead(A2);
            int flex4 = analogRead(A3);
            int flex5 = analogRead(A4);
            int pad1 = digitalRead(D0);
            int pad2 = digitalRead(D1);
            int pad3 = digitalRead(D2);
            int pad4 = digitalRead(D3);
            */
            t = millis();
        }

        if (!client.connected())
        {
            Serial.println();
            Serial.println("disconnecting.");
            client.stop();
            connected = false;
            //for(;;);
        }
    } else {
        Serial.println("failure");
    }
}