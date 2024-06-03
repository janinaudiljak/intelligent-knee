function Simulation(desired_angle)
%Simulation(qd) ex. Simulation(1.745) aprox 100grader 0 - 2.26893 (130)

% Define simulation parameters
t_0 = 0;
t_f = 5;
min_angle = 0;  % Minimum joint angle (0 radians)
max_angle = deg2rad(130);  % Maximum joint angle (130 degrees converted to radians)
Kp = 1; % Proportional gain
Kd = 0.1; % Derivative gain

% Find serialports
sp = serialportlist;

% Create a serial port object
portModule = serialport('COM1', 115200);  % Replace 'COM1' with your actual port name

% Flush the port to receive the latest transmission
flush(portModule);

% In this example, the remote unit is waiting for a 'm' character to start
% the communication (handshake)
% Write data to the serial port
write(portModule, 'm', 'char');

% Start the timer before the main simulation loop
startTime = tic;

% Main simulation loop
while true

      % Prompt user for desired joint angle
    qd = input('Enter desired joint angle (in radians): ');

    % Check if desired joint angle is within the specified range
    if qd < min_angle || qd > max_angle
        disp('Error: Desired joint angle is out of range.');
        continue;  % Skip the rest of the loop iteration and prompt user again
    end

    % Get current simulation time
    elapsedTime = toc(startTime);
    
    % Read data from the serial port
    % Parsing doubles separated by " " 
    l = readline(portModule);
    position = str2double(strsplit(l, " "));

    % Limit knee joint angle within desired range
    position = max(min(position, max_angle), min_angle);

    % Compute forward kinematics to get end effector position
    end_effector_position = FowardKinematics(position);
    
    % Update simulation based on received data, current time, and end effector position
    updateSimulation(position, velocity, acceleration, elapsedTime, end_effector_position);

    % Pause to synchronize with real-time clock
    pause(0.1); % Adjust this value as needed
    
    % Check for termination condition (e.g., user input)
    % Terminate the loop when needed
    if elapsedTime >= simulation_duration
        break;
    end
end
% Close the connection
fclose(portModule);

clear portModule

% Initialize variables for data logging
data = struct('t', [], 'q', [], 'qd', [], 'qdp', [], 'qddp', [], 'Tau', []);

% Main simulation loop
for t = t_0:0.01:t_f
    % Generate desired trajectory
    [qd, qdp, qddp] = Trajectory_generator(t, t_0, t_f);
    
    % Get current joint position from Raspberry Pi
    q = GetCurrentPositionFromRaspberryPi('COM1'); % Adjust port name
    
    % Calculate control torque using PD controller
    Tau = Tau_k(q, qd, qdp, Kp, Kd);
    
    % Log data
    data.t(end+1) = t;
    data.q(end+1) = q;
    data.qd(end+1) = qd;
    data.qdp(end+1) = qdp;
    data.qddp(end+1) = qddp;
    data.Tau(end+1) = Tau;
    
    % Plot data
    % Code for plotting position, velocity, and acceleration
end

% Plotting code
% Plot position, velocity, and acceleration from data structure
figure;

subplot(3,1,1);
plot(data.t, data.q, 'b-', 'LineWidth', 1.5);
hold on;
plot(data.t, data.qd, 'r--', 'LineWidth', 1.5);
title('Position vs Time');
xlabel('Time (s)');
ylabel('Position');
legend('Actual Position', 'Desired Position');

subplot(3,1,2);
plot(data.t, data.qdp, 'g-', 'LineWidth', 1.5);
title('Velocity vs Time');
xlabel('Time (s)');
ylabel('Velocity');

subplot(3,1,3);
plot(data.t, data.qddp, 'm-', 'LineWidth', 1.5);
title('Acceleration vs Time');
xlabel('Time (s)');
ylabel('Acceleration');

sgtitle('Joint Dynamics');





