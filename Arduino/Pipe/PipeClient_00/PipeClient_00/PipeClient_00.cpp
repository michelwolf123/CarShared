// PipeClient_00.cpp : Diese Datei enthält die Funktion "main". Hier beginnt und endet die Ausführung des Programms.
//
#include <Windows.h>
#include <iostream>
#include <array>
using namespace std;

int FEmntsInArray(char arr[])
{
	bool flag = TRUE;
	int i = 0;
	while (flag == TRUE)
	{

		if (arr[i] == 0)
		{
			flag = FALSE;
		}
		i++;
	}
	return i - 1;
}

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
DWORD dwWriteFileBufferSize = FEmntsInArray(szWriteFileBuffer);


void motor()
{
	szWriteFileBuffer[0] = szReadFileBuffer[1];
	dwWriteFileBufferSize = FEmntsInArray(szWriteFileBuffer);
	cout << "writefilebuffersize" << dwWriteFileBufferSize << endl;
	cout << szWriteFileBuffer[0] << endl;
	bWriteFile = WriteFile(
		hCreateFile,
		szWriteFileBuffer,
		dwWriteFileBufferSize,
		&dwNoBytesWrite,
		NULL);
	if (bWriteFile == FALSE)
	{
		cout << "WriteFile failed = " << GetLastError() << endl;
	}
}

void brake()
{

}

void steering()
{

}

void parseInput()
{
	//parseing read data
	if (szReadFileBuffer[0] == 'm')
	{
		cout << "m" << endl;
		cout << szReadFileBuffer[1] << endl;
		motor();
	}
	if (szReadFileBuffer[0] == 'b')
	{
		cout << "b" << endl;
		brake();
	}
	if (szReadFileBuffer[0] == 'l')
	{
		cout << "l" << endl;
		steering();
	}
	if (szReadFileBuffer[0] == 'r')
	{
		cout << "r" << endl;
	}
}




int main()
{
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
	

	BOOL mainLoop = TRUE;
	
	while (mainLoop)
	{
		//ReadFile
		bReadFile = ReadFile(
			hCreateFile,
			szReadFileBuffer,
			dwReadFileBufferSize,
			&dwNoBytesRead,
			NULL);

		if (bReadFile == TRUE)
		{
			parseInput();
		}
		else
		{
			cout << "reading failed" << endl;
		}

	}

	CloseHandle(hCreateFile);
	system("PAUSE");
	return 0;

	/*
	cout << "\t\....NAMED PIPE Client...." << endl;

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
	char szWriteFileBuffer[1023] = "Hello from named pipe Client";
	DWORD dwWriteFileBufferSize = FEmntsInArray(szWriteFileBuffer);
	cout << "dwWriteFileBufferSize: " << dwWriteFileBufferSize << endl;
	
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
	cout << "File Creation success" << endl;

	BOOL queueFlag = TRUE;
	int i = 0;
	while (queueFlag)
	{
		//ReadFile
		bReadFile = ReadFile(
			hCreateFile,
			szReadFileBuffer,
			dwReadFileBufferSize,
			&dwNoBytesRead,
			NULL);

		if (bReadFile == FALSE)
		{
			cout << "ReadFile failed" << GetLastError() << endl;
		}
		else
		{
			cout << "ReadFile success, " << dwNoBytesRead << " charakters read" << endl;
			cout << "Data Reading from Server ----> " << szReadFileBuffer[dwNoBytesRead - 1] << endl;
		}
		cout << "NoBytesRead: " << dwNoBytesRead << endl;
		if (i == 9)
		{
			queueFlag = FALSE;
		}
		i++;
	}
	
	cout << "reading finished, all messages send" << endl;
	
	//WriteFile operation
	bWriteFile = WriteFile(
		hCreateFile,
		szWriteFileBuffer,
		dwWriteFileBufferSize,
		&dwNoBytesWrite,
		NULL);
	if (bWriteFile == FALSE)
	{
		cout << "WriteFile failed = " << GetLastError() << endl;
	}
	else
	{
		cout << "WriteFile Success" << endl;
	}

	CloseHandle(hCreateFile);
	system("PAUSE");
	return 0;
	*/
}

// Programm ausführen: STRG+F5 oder "Debuggen" > Menü "Ohne Debuggen starten"
// Programm debuggen: F5 oder "Debuggen" > Menü "Debuggen starten"

// Tipps für den Einstieg: 
//   1. Verwenden Sie das Projektmappen-Explorer-Fenster zum Hinzufügen/Verwalten von Dateien.
//   2. Verwenden Sie das Team Explorer-Fenster zum Herstellen einer Verbindung mit der Quellcodeverwaltung.
//   3. Verwenden Sie das Ausgabefenster, um die Buildausgabe und andere Nachrichten anzuzeigen.
//   4. Verwenden Sie das Fenster "Fehlerliste", um Fehler anzuzeigen.
//   5. Wechseln Sie zu "Projekt" > "Neues Element hinzufügen", um neue Codedateien zu erstellen, bzw. zu "Projekt" > "Vorhandenes Element hinzufügen", um dem Projekt vorhandene Codedateien hinzuzufügen.
//   6. Um dieses Projekt später erneut zu öffnen, wechseln Sie zu "Datei" > "Öffnen" > "Projekt", und wählen Sie die SLN-Datei aus.
