clc;clear;close all;

is_real=1;           % Type of the transform(0: complex-valued curvelets,1: real-valued curvelets)
finest=2;            % Chooses one of two possibilities for the coefficients at the finest level(1: curvelets,2: wavelets)
alpha=1.0;           % ������׼���alpha����ֵ��1.2���ҽ�Ϊ���룩

niter=10;

fid=fopen('real.bin','r');
ori=fread(fid,[800,220],'float');

dn=yc_scale(ori,2);
[n1,n2]=size(dn);
figure;imagesc([dn]);colormap(seis);caxis([-0.5,0.5]);title('dn,ԭͼ');

s_cplot(dn)
% figure;
% imagesc(dn)
xlabel('Trace') 
ylabel('Time(s)') 
set (gcf,'Position',[50,50,375,490])
set(gca, 'Position', [.13 .04 .5 .85]); % OuterPosition

xlen=floor(linspace(0,220,6));
set(gca,'XTick', xlen);
set(gca,'xticklabel',roundn(linspace(0,220,6),0));

ylen=floor(linspace(0,800,7));%���ȷ�Ϊ4��
set(gca,'YTick', ylen);
ykedu=roundn(linspace(0,1.6,7),-1);
set(gca,'yticklabel',ykedu);