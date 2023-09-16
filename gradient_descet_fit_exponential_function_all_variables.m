close all
clear all
clc


%c = [a;
%     b;
%     Tau;]


%define true valus
a = 40;
b = 2;
Tau = 10;
c = 0; %IMPORTANT: the variable c is not considered here, because the point of Gradient Descent is 
%already fully explained and I dont wanna waste more time in this.

%define support
t = (-10:1:5*Tau)';
t_plot = (t(1):0.01:t(end))';

%define function
y = @(x) a - b*exp(-x/Tau);

% create measurement values by adding some noise and evalutating it at
% less points
d = y(t) + 0.5*randn(size(y(t)));

% create measurement values by adding some noise and evalutating it at
% less points
d_all{1} = round(2*y(t))/2;
d_all{2} = y(t) + 0.5*randn(size(t));

for jj = 1:2
    d =  d_all{jj};



    %define cost function
    J = @(a) sum((d - (a - b*exp(-t/T))).^2); %initial cost function
    L = @(a) log(J(a) + 10); %modified cost function with better numerical properties

    df_da   = @(a,b,Tau) -(sum(2*(-a + b*exp(-t/Tau) + d)))/(sum( (-a + b*exp(-t/Tau) + d).^2 ) + 10);
    df_db   = @(a,b,Tau) sum(2*exp(-t/Tau).*(exp(-t/Tau)*b + d - a))/(sum((exp(-t/Tau*b + d - a))) + 10);
    df_dTau = @(a,b,Tau) sum(2*b*t.*exp(-t/Tau).*(b*exp(-t/Tau) + d - a))/(sum(Tau^2 * (b*exp(-t/Tau) + d - a).^2) + 10*Tau^2);

    grad_L = @(a,b,Tau) [df_da(a,b,Tau); df_db(a,b,Tau); df_dTau(a,b,Tau)];

    %start the gradient descent
    c = [30; 1; 5]; %initial values
    gamma = 0.05;

    for ii = 1:100000
        c = c - gamma*grad_L(c(1), c(2), c(3));
    end
    c
    y_est = c(1) - c(2)*exp(-t_plot/c(3));

    %plot both
    figure
    %     plot(t_plot, y(t_plot), 'DisplayName', 'True')
        hold on
        plot(t, d, 'o', 'DisplayName', 'measurements')
        plot(t_plot, y_est, '-', 'DisplayName', 'fitted exponential')
        grid on
        legend('Location','southeast')
        xlabel("x")
        ylabel("y")


        saveas(gcf, "Figures/fitted_function_" + num2str(jj) + ".png")
end




    
    
