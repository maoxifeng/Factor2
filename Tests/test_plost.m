aa = IA_OLSReturn;
aa(isnan(aa)) = 0;
bb = LC_YearDuration_IA_3Groups_Return(:, 4);
bb(isnan(bb)) = 0;

a = cumprod(aa+1);
b = cumprod(bb+1);
plot([a(2735:5691), b(2735:5691)]);
plot([a, b]);
plot(b);
plot(a);
find(aa~=0, 1);




cc = squeeze(ThreeDArray(1,:,:));