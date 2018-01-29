function [ t, ftest, m ] = wavelet( signal, s_SRate )
%WAVELET 

%%Input signal
x= signal;
fmin= 20; fmax=660; df= 5; %Se definen las frecuencias en las que se va a evaluar
ftest= fmin:df:fmax; %Frecuencias donde se va a buscar
nper= 10; %Num periodos
sigma= (1./ftest)*nper/2; %Sigma de la ventana
time= linspace(0,numel(x)/s_SRate,numel(x)); %Se define el tiempo
t= linspace(ceil(-time(end)/2),time(end)/2, length(x));%ceil(-time(end)/2):1/s_SRate:time(end)/2;
m= zeros(numel(ftest),numel(t));
for a= 1:numel(ftest)
    vent= exp(-0.5*t.^2/sigma(a)^2); %Se define la ventana
    stest= exp(-2*pi*ftest(a)*t*1i).*vent; %Defino la señal "patron"
    m(a,:)=conv(x,stest,'same'); %Se realiza la convolución
end

end

