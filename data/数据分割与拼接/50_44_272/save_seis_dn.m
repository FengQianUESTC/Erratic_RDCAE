clc;
clear;
close all;
is_real=1;           
finest=2;           
alpha=1.0;          
niter=10;
fid=fopen('real.bin','r');
ori=fread(fid,[800,220],'float');






dn=yc_scale(ori,2);
[n1,n2]=size(dn);
figure;imagesc([dn]);colormap(seis);caxis([-0.5,0.5]);
save('seis_dn.mat','dn','-v7.3')