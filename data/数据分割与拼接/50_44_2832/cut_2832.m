clc;clear;close all;
is_real=1;           
finest=2;           
alpha=1.0;          
niter=10;
fid=fopen('real.bin','r');
ori=fread(fid,[800,220],'float');
dn=yc_scale(ori,2);

figure;
imagesc([dn]);
colormap(seis);
caxis([-0.5,0.5]);
%% 每块取50*50的大小，每次往右移25位置，每次往下移25位置
data=zeros(50,44,2832);
p=1;
for i=1:50:751
    for j=1:1:177
            data(:,:,p)=dn(i:i+49,j:j+43);
            pingan=dn(i:i+49,j:j+43);
            p=p+1;
            
        
    end
%     s_cplot(ceshi,{'limits',-val,val},{'colormap','gray'});title('Zero-offset VSP data');
end


save('seis_dn_chongdie_50_44_2832_12_29.mat','data','-v7.3')
% s_cplot(ping,{'limits',-val,val},{'colormap','gray'});title('fuyuan');