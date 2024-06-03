function Tau_k = Tau_k(q, qd, qdp, Kp, Kd)
    % Tau_k - PD controller for controlling the knee orthosis
    %   q: Current joint position
    %   qd: Desired joint position
    %   qdp: Desired joint velocity
    %   Kp: Proportional gain
    %   Kd: Derivative gain
    
    % Error calculation
    e = qd - q;
    ed = qdp;

    % PD controller
    Tau_k = Kp * e + Kd * ed;
end
