
// Windows
#ifdef _WIN64

	#include <iostream>
	#include <string>
	#include <fstream>
	#include <windows.h>


	using namespace std;
	////////////////////////////////////////////////////////////////////////
	int main(int argc, char* argv[])
	{
		if (argc != 3)
		{
			fprintf(stderr,"\nstart_factorio.exe (c) flameSla\n");
			fprintf(stderr,"\nUsage: start_factorio.exe argList affinity_mask\n");
			fprintf(stderr,"\nWhere:");
			fprintf(stderr,"\n  argList           - 'factorio.exe --benchmark \"save\" --benchmark-ticks 100 --disable-audio'");
			fprintf(stderr,"\n  affinity_mask     - 3 https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setprocessaffinitymask");
			fprintf(stderr,"\n");
			return -1;
		}

		string argList = argv[1]; 
		uint64_t affinity_mask = std::stoull( argv[2] );

		//cout << "argList = " << argList << endl;
		//cout << "start_factorio.exe - affinity_mask = " << affinity_mask << endl;
		
		SECURITY_ATTRIBUTES saAttr;
		HANDLE g_hChildStd_OUT_Rd = NULL;
		HANDLE g_hChildStd_OUT_Wr = NULL;

		saAttr.nLength = sizeof(SECURITY_ATTRIBUTES);
		saAttr.bInheritHandle = TRUE;
		saAttr.lpSecurityDescriptor = NULL;
		if ( !CreatePipe(&g_hChildStd_OUT_Rd, &g_hChildStd_OUT_Wr, &saAttr, 0) )
		{
			fprintf(stderr, "start_factorio.exe - ERROR - StdoutRd CreatePipe");
			return -1;
			
		}
		if ( !SetHandleInformation(g_hChildStd_OUT_Rd, HANDLE_FLAG_INHERIT, 0) )
		{
			fprintf(stderr, "start_factorio.exe - ERROR - Stdout SetHandleInformation");
			return -1;
		}

		// Create a child process that uses the previously created pipes for STDIN and STDOUT.
		PROCESS_INFORMATION piProcInfo;
		STARTUPINFOA siStartInfo;
		BOOL bSuccess = FALSE;
		ZeroMemory( &piProcInfo, sizeof(PROCESS_INFORMATION) );
		ZeroMemory( &siStartInfo, sizeof(STARTUPINFO) );
		siStartInfo.cb = sizeof(STARTUPINFO);
		siStartInfo.hStdError = g_hChildStd_OUT_Wr;
		siStartInfo.hStdOutput = g_hChildStd_OUT_Wr;
		siStartInfo.dwFlags |= STARTF_USESTDHANDLES;

		bSuccess = CreateProcessA( 	NULL, //lpApplicationName
									(char*)argList.c_str(), //lpCommandLine
									NULL, //lpProcessAttributes
									NULL, //lpThreadAttributes
									TRUE, //bInheritHandles
									HIGH_PRIORITY_CLASS, //dwCreationFlags
									NULL, //lpEnvironment
									NULL, //lpCurrentDirectory
									&siStartInfo, //lpStartupInfo
									&piProcInfo); //lpProcessInformation
		
		if ( ! bSuccess )
		{
			fprintf(stderr, "start_factorio.exe - ERROR - CreateProcess");
			CloseHandle(g_hChildStd_OUT_Wr);
			CloseHandle(g_hChildStd_OUT_Rd);
			return -1;
		}
		else
		{
			if( affinity_mask != 0)
				SetProcessAffinityMask( piProcInfo.hProcess, affinity_mask);
			
			CloseHandle(piProcInfo.hProcess);
			CloseHandle(piProcInfo.hThread);
			CloseHandle(g_hChildStd_OUT_Wr);
		}

		//ReadFromPipe()
		const size_t BUFSIZE = 4096;
		DWORD dwRead;
		CHAR chBuf[BUFSIZE];
		bSuccess = FALSE;

		ofstream outfile;
		outfile.open ("temp", ios::out | ios::binary | ios::trunc); 
		if (outfile.is_open())
		{
			while( true )
			{
				bSuccess = ReadFile( g_hChildStd_OUT_Rd, chBuf, BUFSIZE, &dwRead, NULL);
				if( ! bSuccess || dwRead == 0 ) break;

				outfile.write( chBuf, dwRead );
			}
			outfile.close();
		}

		return 0;
	}
#endif

// Linux
// write the code yourself
