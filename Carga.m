%%Rutina de Carga
clc, clear all, close all
%Def de contenedores
normal_a = {};
extrah_a = {};
murmur_a = {};
normal_b = {};
extrah_b = {};
murmur_b = {};

%Set_a
name_a = 'set_a';
a = dir(name_a);
carp = a(4).name;
carp = fullfile(name_a, carp);
a = dir(carp);
for i=4:size(a,1)
    act_n = fullfile(carp, a(i).name);
    act_s = dir(act_n);
    for j=3:size(act_s,1)
        file_n = fullfile(act_n, act_s(j).name);
        bin = strsplit(act_s(j).name,'_');
        [sample_a, freq_a] = audioread(file_n);
        new_a = {sample_a, freq_a};
        if strcmp(bin(1), 'extrahls')
            extrah_a{end+1} = new_a;
        elseif strcmp(bin(1),'murmur')
            murmur_a{end+1} = new_a;
        elseif strcmp(bin(1),'normal')
            normal_a{end+1} = new_a;    
        end
    end
end

% Set_b
name_b = 'set_b';
a = dir(name_b);
carp = a(4).name;
carp = fullfile(name_b, carp);
a = dir(carp);
for i=3:size(a,1)
    act_n = fullfile(carp, a(i).name);
    act_s = dir(act_n);
    for j=3:size(act_s,1)
        file_n = fullfile(act_n, act_s(j).name);
        bin = strsplit(act_s(j).name,'_');
        [sample_b, freq_b] = audioread(file_n);
        new_b = {sample_b, freq_b};
        if strcmp(bin(1), 'extrastole')
            extrah_b{end+1} = new_b;
        elseif strcmp(bin(1),'murmur')
            murmur_b{end+1} = new_b;
        elseif strcmp(bin(1),'normal')
            normal_b{end+1} = new_b;    
        end
    end
end

%% Wavelet
signal = normal_a{2};
[ t, ftest, m ] = wavelet(signal{1}, signal{2});
figure
imagesc(t,ftest,abs(m))
axis xy
colormap(jet(256))