% Define constants
theta_min = 0;     % Minimum angle in radians
theta_max = deg2rad(130);   % Maximum angle in radians
t_span = 0:0.01:10; % Time span for simulation
initial_theta = 0;  % Initial angle (standing position)
initial_theta_dot = 0; % Initial angular velocity
initial_state = [initial_theta; initial_theta_dot]; % Initial state vector

% Start the timer
startTime = tic;

persistent startTime;

% Simulation parameters
options = odeset('RelTol', 1e-6, 'AbsTol', 1e-6);

% Simulate knee movement
[t, state] = ode45(@knee_movement, t_span, initial_state, options);

% Stop the timer and display elapsed time
elapsed_time = toc;
disp(['Elapsed time for simulation: ', num2str(elapsed_time), ' seconds']);

% Plot position, velocity, and acceleration graphs
theta = state(:, 1);
theta_dot = state(:, 2);
theta_ddot = gradient(theta_dot, t);

figure;
subplot(3,1,1);
plot(t, rad2deg(theta));
title('Knee Position');
xlabel('Time (s)');
ylabel('Position (degrees)');

subplot(3,1,2);
plot(t, rad2deg(theta_dot));
title('Knee Velocity');
xlabel('Time (s)');
ylabel('Velocity (degrees/s)');

subplot(3,1,3);
plot(t, rad2deg(theta_ddot));
title('Knee Acceleration');
xlabel('Time (s)');
ylabel('Acceleration (degrees/s^2)');

% Send movement commands via USB to Raspberry Pi
% Connect to the serial port
portModule = serialport('COM1', 'BaudRate', 115200);  % Replace 'COM1' with your actual port name

% Flush the port to receive the latest transmission
portModule.flush("input");

% User input control loop
while true
    % Prompt user for input
    target_angle = input('Enter target knee angle (0-130 degrees): ');

    % Check if input is within valid range
    if target_angle < 0 || target_angle > 130
        disp('Invalid input! Angle must be between 0 and 130 degrees.');
    else
        break; % Exit loop if input is valid
    end
end

% Send the target angle command to Raspberry Pi
portModule.write(num2str(target_angle), "char");

% Wait for acknowledgment from Raspberry Pi
acknowledgment = portModule.readline();
disp(acknowledgment); % Display acknowledgment message (optional)

% Close the connection
portModule.delete();
clear portModule;

% Define the function for knee movement dynamics
function dydt = knee_movement(t, state)
    % System parameters (You may need to adjust these parameters)
    k = 10; % Spring constant
    b = 0.5; % Damping coefficient
    
    % Extract state variables
    theta = state(1);
    theta_dot = state(2);
    
    % Define system dynamics
    theta_desired = sin(t); % Desired knee angle (you can define your own desired motion profile)
    u = -k * (theta - theta_desired) - b * theta_dot; % Control input
    
    % Define the equations of motion
    dtheta_dt = theta_dot;
    dtheta_dot_dt = u;
    
    % Pack the derivatives into a column vector
    dydt = [dtheta_dt; dtheta_dot_dt];
end
