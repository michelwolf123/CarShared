
#ifndef ARDUINOAUTO2
#define ARDUINOAUTO2

class arduinoauto2 {
public:
	arduinoauto2();
	~arduinoauto2();
	bool getdata(); //store recieved string in member variables mmotor, mstriring
	int controll();  //daten von getdata aufteilen auf steuerungseinheiten (motor, lenkung) und controlldaten von motor und lenkung zurücksenden mit sendcontroll data 

private:
	char recData[7] = {}; //is this really nessecary store recieved data in char array, use this for getdata
	int mstiring = 0;
	int mmotor = 0;
	bool motor();
	bool stiring();
	bool sendcontrolldata();

};
#endif ARDUINOAUTO2