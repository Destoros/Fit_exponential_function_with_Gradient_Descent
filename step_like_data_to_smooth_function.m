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

%define support
Ts = 0.001;
t = (-10:Ts:5*Tau)';

%define function
y = @(x) a - b*exp(-x/Tau);

% create measurement values by adding some noise and evalutating it at
% less points
d = round(2*y(t))/2;


    
%design a LP filter

% rng default
% 
% Fs = 1000;
% t = linspace(0,1,Fs);
% d = cos(2*pi*100*t)+0.5*randn(size(t));

fg = 0.000001; %
Fs = 1/Ts;
Wn = (2/Fs)*fg;
b = fir1(2000,Wn,'low',hamming(2001));

[h,f] = freqz(b,1,[],Fs);
plot(f,mag2db(abs(h)))
xlabel('Frequency (Hz)')
ylabel('Magnitude (dB)')
grid

z = filter(b,1,d);

figure
    plot(t,d, 'DisplayName', 'Measurements d')
    hold on
    plot(t,z, 'DisplayName', 'filtered signal')
    xlabel t
    ylabel measurements
    grid on
    legend
    






    
    
