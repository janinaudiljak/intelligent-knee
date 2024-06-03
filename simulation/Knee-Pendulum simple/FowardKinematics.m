function X = FowardKinematics(q)
    % Forward kinematics for a leg with a single knee joint
    %   q: Joint angle at the knee (in radians)
    
    % Length of the upper leg (hip to knee)
    l1 = 0.6; % 60 cm
    
    % Length of the lower leg (knee to ankle)
    l2 = 0.5; % 50 cm
    
    % Offset (assuming ankle to end effector)
    l3 = 0.2; % Assuming no offset
    
    % Transformation from the world to the hip(w) to knee(0), where hip is the 
    % world frame and the knee (0) frame
    T_w_0 = [cos(q) sin(q) 0  l1 * cos(q);
             -sin(q) cos(q) 0  -l1 * sin(q);
             0       0      1  0;
             0       0      0  1];

    % Transformation from the world to the hip(w) to knee(0)
    % Rotation in z-axis
    T_0_1 = [1 0 0 0;
             0 1 0 l2;
             0 0 1 0;
             0 0 0 1];

    % Transformation from the ankle to the end effector
    T_1_e = [1 0 0 0;
             0 1 0 l3;
             0 0 1 0;
             0 0 0 1];

    % Overall transformation from world to end effector
    T_w_e = T_w_0 * T_0_1 * T_1_e;

    X = T_w_e(1:3, 4); % Extract position from transformation matrix
end