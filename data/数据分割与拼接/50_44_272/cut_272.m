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
data=zeros(50,44,272);
p=1;
for i=1:50:751
    for j=1:11:177
            data(:,:,p)=dn(i:i+49,j:j+43);
            pingan=dn(i:i+49,j:j+43);
            p=p+1;
            
%             figure;
%             imagesc([pingan]);
%             colormap(seis);
%             caxis([-0.5,0.5]);
        
    end
%     s_cplot(ceshi,{'limits',-val,val},{'colormap','gray'});title('Zero-offset VSP data');
end

ping=zeros(800,220);
horizontal =50;
vertical =44;
len=11;




datapin=data(:,:,30);
for k=1:16
    
    ping(((k-1)*horizontal+1):k*horizontal,0*len+1:1*len)=data(:,1:11,(k-1)*17+1);
    ping(((k-1)*horizontal+1):k*horizontal,1*len+1:2*len)=0.5* (data(:,12:22,(k-1)*17+1)+data(:,1:11,(k-1)*17+2));
    ping(((k-1)*horizontal+1):k*horizontal,2*len+1:3*len)=(data(:,23:33,(k-1)*17+1)+data(:,12:22,(k-1)*17+2)+data(:,1:11,(k-1)*17+3))/3;
    ping(((k-1)*horizontal+1):k*horizontal,3*len+1:4*len)=0.25* (data(:,34:44,(k-1)*17+1)+data(:,23:33,(k-1)*17+2)+data(:,12:22,(k-1)*17+3)+data(:,1:11,(k-1)*17+4));
    
    ping(((k-1)*horizontal+1):k*horizontal,4*len+1:5*len)=0.25* (data(:,34:44,(k-1)*17+2)+data(:,23:33,(k-1)*17+3)+data(:,12:22,(k-1)*17+4)+data(:,1:11,(k-1)*17+5));
    ping(((k-1)*horizontal+1):k*horizontal,5*len+1:6*len)=0.25* (data(:,34:44,(k-1)*17+3)+data(:,23:33,(k-1)*17+4)+data(:,12:22,(k-1)*17+5)+data(:,1:11,(k-1)*17+6));
    ping(((k-1)*horizontal+1):k*horizontal,6*len+1:7*len)=0.25* (data(:,34:44,(k-1)*17+4)+data(:,23:33,(k-1)*17+5)+data(:,12:22,(k-1)*17+6)+data(:,1:11,(k-1)*17+7));
    ping(((k-1)*horizontal+1):k*horizontal,7*len+1:8*len)=0.25* (data(:,34:44,(k-1)*17+5)+data(:,23:33,(k-1)*17+6)+data(:,12:22,(k-1)*17+7)+data(:,1:11,(k-1)*17+8));
    
    ping(((k-1)*horizontal+1):k*horizontal,8*len+1:9*len)=0.25* (data(:,34:44,(k-1)*17+6)+data(:,23:33,(k-1)*17+7)+data(:,12:22,(k-1)*17+8)+data(:,1:11,(k-1)*17+9));
    ping(((k-1)*horizontal+1):k*horizontal,9*len+1:10*len)=0.25* (data(:,34:44,(k-1)*17+7)+data(:,23:33,(k-1)*17+8)+data(:,12:22,(k-1)*17+9)+data(:,1:11,(k-1)*17+10));
    ping(((k-1)*horizontal+1):k*horizontal,10*len+1:11*len)=0.25* (data(:,34:44,(k-1)*17+8)+data(:,23:33,(k-1)*17+9)+data(:,12:22,(k-1)*17+10)+data(:,1:11,(k-1)*17+11));
    ping(((k-1)*horizontal+1):k*horizontal,11*len+1:12*len)=0.25* (data(:,34:44,(k-1)*17+9)+data(:,23:33,(k-1)*17+10)+data(:,12:22,(k-1)*17+11)+data(:,1:11,(k-1)*17+12));
    
    ping(((k-1)*horizontal+1):k*horizontal,12*len+1:13*len)=0.25* (data(:,34:44,(k-1)*17+10)+data(:,23:33,(k-1)*17+11)+data(:,12:22,(k-1)*17+12)+data(:,1:11,(k-1)*17+13));
    ping(((k-1)*horizontal+1):k*horizontal,13*len+1:14*len)=0.25* (data(:,34:44,(k-1)*17+11)+data(:,23:33,(k-1)*17+12)+data(:,12:22,(k-1)*17+13)+data(:,1:11,(k-1)*17+14));
    ping(((k-1)*horizontal+1):k*horizontal,14*len+1:15*len)=0.25* (data(:,34:44,(k-1)*17+12)+data(:,23:33,(k-1)*17+13)+data(:,12:22,(k-1)*17+14)+data(:,1:11,(k-1)*17+15));
    ping(((k-1)*horizontal+1):k*horizontal,15*len+1:16*len)=0.25* (data(:,34:44,(k-1)*17+13)+data(:,23:33,(k-1)*17+14)+data(:,12:22,(k-1)*17+15)+data(:,1:11,(k-1)*17+16));
    
    
    
    ping(((k-1)*horizontal+1):k*horizontal,16*len+1:17*len)=0.25* (data(:,34:44,(k-1)*17+14)+data(:,23:33,(k-1)*17+15)+data(:,12:22,(k-1)*17+16)+data(:,1:11,(k-1)*17+17));
    ping(((k-1)*horizontal+1):k*horizontal,17*len+1:18*len)=(data(:,34:44,(k-1)*17+15)+data(:,23:33,(k-1)*17+16)+data(:,12:22,(k-1)*17+17))/3;
    ping(((k-1)*horizontal+1):k*horizontal,18*len+1:19*len)=0.5* (data(:,34:44,(k-1)*17+16)+data(:,23:33,(k-1)*17+17));
    ping(((k-1)*horizontal+1):k*horizontal,19*len+1:20*len)=data(:,34:44,(k-1)*17+17);
end
figure;
imagesc([ping]);
colormap(seis);
caxis([-0.5,0.5]);
x=ping-dn;
x_min=min(min(x))
x_max=max(max(x))
% 
save('seis_dn_chongdie_50_44_272_12_29.mat','data','-v7.3')
% s_cplot(ping,{'limits',-val,val},{'colormap','gray'});title('fuyuan');