#include"ArduinoAuto2.h"
#include<iostream>
#include<Windows.h>

using namespace std;

//variables for pipes, maybe better as member variables of arduinoauto2 class
//Local Variable Def
HANDLE hCreateFile;

//READFILE local Variable def
BOOL bReadFile;
DWORD dwNoBytesRead;
char szReadFileBuffer[1023];
DWORD dwReadFileBufferSize = sizeof(szReadFileBuffer);

//WriteFile Local Variable Def
BOOL bWriteFile;
DWORD dwNoBytesWrite;
char szWriteFileBuffer[1023] = "";
DWORD dwWriteFileBufferSize = sizeof(szWriteFileBuffer);


arduinoauto2::arduinoauto2() {
	cout << "\t\....NAMED PIPE Client...." << endl;

	//CreateFile for Pipe
	hCreateFile = CreateFile(
		L"\\\\.\\pipe\\MYNAMEDPIPE",
		GENERIC_READ | GENERIC_WRITE,
		0,
		NULL,
		OPEN_EXISTING,
		FILE_ATTRIBUTE_NORMAL,
		NULL);

	if (INVALID_HANDLE_VALUE == hCreateFile)
	{
		cout << "File Creation failed = " << GetLastError() << endl;
	}
	else
	{
		cout << "File Creation success" << endl;
	}
}

arduinoauto2::~arduinoauto2() {
	CloseHandle(hCreateFile);
	cout << "Handle for NamedPipe Client closed" << endl;
}

bool arduinoauto2::getdata() {

}

int arduinoauto2::controll() {
	//call motor or stiring fkt only if values have changed

	bool cdm = motor(); //cdm-controll data motor
	bool cds = stiring(); //controll data stiring

	bool scd = sendcontrolldata(/*tosent*/); //cdm and cds in one array for sending back to raspberry/carla
}

bool arduinoauto2::motor() {
	//in which case return false?
	if (mmotor < 100)
		cout << "rückwärts: "<<mmotor << endl;
	if (mmotor >= 100)
		cout << "vorwärts: "<<mmotor << endl;
	return true;
}

bool arduinoauto2::stiring() {
	cout << "lenkung: " << stiring << endl;
	return true;
}

bool arduinoauto2::sendcontrolldata() {

}