close all
clear all
clc


a = 40;
b = 2;
T = 10;
c = 0

%define support
t = (-10:1:5*T)';
t_plot = (t(1):0.01:t(end))';

%define function
y = @(x) a - b*exp(-x/T);

% create measurement values by adding some noise and evalutating it at
% less points
d = y(t) + 0*randn(size(y(t)));

N = length(t);
a = 1/N*(sum(d) + b*sum(exp(-(t-c)/T)))%analytic formual to find a

%plot both
figure
    plot(t, d, 'o', 'DisplayName', 'measurements d')
    hold on
    plot(t_plot, y(t_plot), 'DisplayName', 'fitted exponential')
    grid on
    legend('Location', 'southeast')
    xlabel("x")
    ylabel("y")
    
    
    saveas(gcf, "Figures/introduction_plot.png")
    

    
%define the cost function
J = @(a) sum((d - (a - b*exp(-t/T))).^2);

%altered cost function -> ERROR: This is function does have the same
%minima but it way more sensitive to noise
K = @(a) sum(log((d - (a - b*exp(-t/T))).^2));

%vary a to get the cost function
grad_J = @(a) sum(-2*(d + b*exp(-t/T) - a));


%plot the cost function and its gradient
da = 0.05; %da is required for the numerical gradient
a = 30:da:50;

figure
    plot(a,J(a), 'DisplayName', 'cost function J')
    grid on
    xlabel('a')
    ylabel('cost function J')
    
    saveas(gcf, "Figures/cost_function_J.png")
    
figure
    plot(a,J(a)+10, 'DisplayName', 'cost function J')
    grid on
    xlabel('a')
    ylabel('cost function J')
        ylim([0, 100])
    
    saveas(gcf, "Figures/cost_function_Jp10.png")
    
    
figure
    plot(a,J(a), 'DisplayName', 'cost function J')
    hold on
    plot(a, grad_J(a), 'DisplayName', 'dJ/da')
    grid on
    xlabel('a')
    ylabel('cost function J')
    legend
    
    saveas(gcf, "Figures/grad_J.png")


%%
    
%find the optimal a using gradient descent
a_search(1) = 30; %start a
gamma = 0.014;
%because this is an exponential function, it can easily happen that
%gradient descent never converges, because of the huge values ->
%Soltion: use the ln of the cost function do decrease the range 
for ii = 2:7
    a_search(ii) = a_search(ii-1) - gamma*grad_J(a_search(ii-1));
end
a_search

figure
    plot(a,J(a), 'DisplayName', 'cost function J')
    hold on
    plot(a, grad_J(a), 'DisplayName', 'dJ/da')
    plot(a_search, J(a_search), '-o', 'DisplayName', 'Gradient Descent search path')
    grid on
    xlabel('a')
    ylabel('cost function J')
    legend
    
    saveas(gcf, "Figures/grad_descent_big_gamma.png")
    
%%
a_search = []
%find the optimal a using gradient descent
a_search(1) = 30; %start a
gamma = 0.002;
%because this is an exponential function, it can easily happen that
%gradient descent never converges, because of the huge values ->
%Soltion: use the ln of the cost function do decrease the range 
for ii = 2:8
    a_search(ii) = a_search(ii-1) - gamma*grad_J(a_search(ii-1));
end
a_search

figure
    plot(a,J(a), 'DisplayName', 'cost function J')
    hold on
    plot(a, grad_J(a), 'DisplayName', 'dJ/da')
    plot(a_search, J(a_search), '-o', 'DisplayName', 'Gradient Descent search path')
    grid on
    xlabel('a')
    ylabel('cost function J')
    legend
    
    saveas(gcf, "Figures/grad_descent_small_gamma.png")
    
%%
a_search = []
%find the optimal a using gradient descent
a_search(1) = 30; %start a
gamma = 0.018;
%because this is an exponential function, it can easily happen that
%gradient descent never converges, because of the huge values ->
%Soltion: use the ln of the cost function do decrease the range 
for ii = 2:8
    a_search(ii) = a_search(ii-1) - gamma*grad_J(a_search(ii-1));
end
a_search

figure
    plot(a,J(a), 'DisplayName', 'cost function J')
    hold on
    plot(a, grad_J(a), 'DisplayName', 'dJ/da')
    plot(a_search, J(a_search), '-o', 'DisplayName', 'Gradient Descent search path')
    grid on
    xlabel('a')
    ylabel('cost function J')
    legend
    
    saveas(gcf, "Figures/grad_descent_too_big_gamma.png")
    
    

    
%%
a_search = []
%find the optimal a using gradient descent
a_search(1) = 30; %start a
gamma = 2;
%because this is an exponential function, it can easily happen that
%gradient descent never converges, because of the huge values ->
%Soltion: use the ln of the cost function do decrease the range 
for ii = 2:15
    a_search(ii) = a_search(ii-1) - gamma*grad_J(a_search(ii-1))/(norm(grad_J(a_search(ii-1))));
end
a_search

figure
    plot(a,J(a), 'DisplayName', 'cost function J')
    hold on
    plot(a, grad_J(a), 'DisplayName', 'dJ/da')
    plot(a_search, J(a_search), '-o', 'DisplayName', 'Gradient Descent search path')
    grid minor
    xlabel('a')
    ylabel('cost function J')
    legend
    
    saveas(gcf, "Figures/grad_descent_normalized_step_size.png")








%% modified cost function with better stability for gradient descent

L = @(a) log(J(a));
grad_L = @(a) -(sum(2*(-a + b*exp(-t/T) + d)))/(sum( (-a + b*exp(-t/T) + d).^2 ) + 10);

figure
    plot(a,L(a), 'DisplayName', 'cost function L')
    hold on
%     plot(a_plot, grad_L(a_plot), 'DisplayName', 'analytical gradient of J')
    plot(a(1:end-1), diff(L(a))/da, 'DisplayName', 'analytical gradient of J')
    grid on
    xlabel a
    ylabel('cost function L')
    legend('cost function L', 'analytical gradient of L')
    
    
    saveas(gcf, "Figures/cost_function_L.png")
    
%% modified cost function with better stability for gradient descent

L = @(a) log(J(a) + 10);
grad_L = @(a) -(sum(2*(-a + b*exp(-t/T) + d)))/(sum( (-a + b*exp(-t/T) + d).^2 ) + 10);

figure
    plot(a,L(a), 'DisplayName', 'cost function K')
    hold on
%     plot(a_plot, grad_L(a_plot), 'DisplayName', 'analytical gradient of J')
    plot(a(1:end-1), diff(L(a))/da, 'DisplayName', 'analytical gradient of K')
    grid on
    xlabel a
    ylabel('cost function K')
    legend('cost function K', 'analytical gradient of K')
    
    
    saveas(gcf, "Figures/cost_function_K.png")
    
%now optimize the cost function L, which still shares the same optima
%a J but has better numerical qualities

%find the optimal a using gradient descent
a_search = -10; %start a
gamma = 0.5;
%because this is an exponential function, it can easily happen that
%gradient descent never converges, because of the huge values ->
%Soltion: use the ln of the cost function do decrease the range 
iter_max = 10000;
for ii = 1:iter_max 
    a_search = a_search - gamma*grad_L(a_search);
    if (iter_max - ii) < 1000
        gamma = 0.1;
    end
end

a_search




    
    
