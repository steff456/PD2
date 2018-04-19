load('Signal2.mat')
v_values=Signal2.value;
x=1:length(v_values);
%pk = los picos [y]
%lk = los picos [x]
%prominence = altura
[pk, lk, width, prominence]=findpeaks(v_values);%,'MinPeakDistance', 40);
% min(pk(lk(1):lk(2))) %BASE
lk_high=lk(prominence>0.1);
lk_down=lk(prominence<0.1);
if lk_down(1)<lk_high(1)
    n_minInit=min(v_values(lk_down(1):lk_high(1)));
    x_start = x(min(v_values(lk_down(1):lk_high(1)))==v_values);
else 
    n_minInit=min(v_values(lk_high(1):lk_down(1)));
end
b = x(min(v_values(lk_down(2):lk_high(2)))==v_values);
n_areaLong=trapz(v_values(n_minInit:x(min(v_values(lk_high(1):lk_down(1))))));
n_areaShort=trapz(v_values(min(v_values(lk_high(1):lk_down(1))):min(v_values(lk_down(1):lk_high(2)))));
% pk_new=pk(prominence<1.2);
% lk_new=lk(prominence<1.2);
% figure, plot(1:length(v_values),v_values,lk_new, pk_new, 'o' )
% x=([1:length(v_values)]/75)';
% figure, plot(x,v_values,lk_new/75, pk_new, 'o' )
% % lk_time=lk_new/75;
% % n_mean=mean(lk_time(2:39)-lk_time(1:38));
% % n_std=std(lk_time(2:39)-lk_time(1:38));
% % v_diference=(lk_time(2:end)-lk_time(1:end-1));
% % n_up=n_mean+n_std;
% % n_down=n_mean-n_std;
% % v_pos=find(and(v_diference<=n_up,v_diference>=n_down));
% % p=1;
% % % for k=2:length(v_pos)
% % %     if v_pos(k)-v_pos(k-1)==1
% % %         lk_bound(p)=lk_new(v_pos(k-1));
% % %         pk_bound(p)=pk_new(v_pos(k-1));
% % %         lk_bound(p+1)=lk_new(v_pos(k));
% % %         pk_bound(p+1)=pk_new(v_pos(k));
% % %         p=p+1;
% % %     elseif v_pos(k)-v_pos(k-1)>=1
% % %         lk_bound(p+1)=lk_new(v_pos(k)-1);
% % %         pk_bound(p+1)=pk_new(v_pos(k)-1);
% % %         p=p+2;
% % %     end
% % %     lk_new(v_pos(k));
% % %     pk_new(v_pos(k));
% % % end
% % 
% % lk_bound=lk_time(diff(v_pos)==1);
% % pk_bound=pk_new(diff(v_pos)==1);
% % % lk_bound=lk_time(and(v_diference<=n_up,v_diference>=n_down));
% % % pk_bound=pk_new(and(v_diference<=n_up,v_diference>=n_down));
% % figure,  plot(x,v_values,lk_bound,pk_bound, '*')