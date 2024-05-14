function [qd, qdp, qddp] = Trajectory_generator(t, t_0, t_f)
    % Trajectory_generator - Generates desired joint trajectory for the knee orthosis
    %   t: Current simulation time
    %   t_0: Start time of the trajectory
    %   t_f: End time of the trajectory
    
    % Define the polynomial coefficients directly based on the start and end times
    T = [1 t_0 t_0^2 t_0^3 t_0^4 t_0^5;
         1 t_f t_f^2 t_f^3 t_f^4 t_f^5;
         0 1 2*t_0 3*t_0^2 4*t_0^3 5*t_0^4;
         0 1 2*t_f 3*t_f^2 4*t_f^3 5*t_f^4;
         0 0 2 6*t_0 12*t_0^2 20*t_0^3;
         0 0 2 6*t_f 12*t_f^2 20*t_f^3];

    % Define the desired joint positions at start and end times
    x = [0; 130*pi/180; 0; 0; 0; 0];

    % Solve for coefficients using the backslash operator
    a = T \ x;

    % Evaluate the trajectory at the current time
    qd = polyval(a(end:-1:1), t);
    qdp = polyval(polyder(a(end:-1:1)), t);
    qddp = polyval(polyder(polyder(a(end:-1:1))), t);
end

% Given time range
t_0 = 0;
t_f = 5;
t = linspace(t_0, t_f, 100); % Adjust the number of points as needed

% Call the trajectory generator function to get trajectory values, velocities, and accelerations
[qd, qdp, qddp] = Trajectory_generator(t, t_0, t_f);

% Evaluate the trajectory at each time point
pos = qd;
vel = qdp;
acc = qddp;
