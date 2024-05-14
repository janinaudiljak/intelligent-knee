% find serialports
sp=serialportfind

% Create a serial port object
portModule = serialport('COM1', 'BaudRate', 115200);  % Replace 'COM1' with your actual port name

% Flush the port to receive the latest transmission
portModule.flush("input");

% In this example, the remote unit is waiting for a 'm' character to start
% the communication (handshake)
% Write data to the serial port
portModule.write('m',"char");

% Read data from the serial port (Two options)
l = portModule.readline() % read a full ASCII line (you need to parse it)
% Parsing dubles separated by " " 
Vals = str2double(l.split(" "));

% Here we read exactly two doubles (check that the size of the data is the
% same in the host PC (matlab) and the remote system (arduino, Raspberry Pi)
l = portModule.read(2,"double") % read 2 doubles

% Close the connection
portModule.delete();

clear portModule
