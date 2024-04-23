x = 0:0.1:2;
y = [0 0.2*ones(1,10) zeros(1,10)];
[xData, yData] = prepareCurveData( x, y );
% 设置 傅里叶拟合选项。
ft = fittype( 'fourier8' );
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
opts.Display = 'Off';
opts.StartPoint = [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1.5707963267949];
% 对数据进行模型拟合。
[fitresult, gof] = fit( xData, yData, ft, opts );
% 绘制数据拟合图。
figure( 'Name', '阶跃函数拟合' );
h = plot( fitresult, xData, yData );
legend( h, '原数据', '8项傅里叶拟合', 'Location', 'NorthEast', 'Interpreter', 'none' );
% 为坐标区加标签
xlabel( 'x', 'Interpreter', 'none' );
ylabel( 'y', 'Interpreter', 'none' );
grid on

% 设置 保型内插法。
ft = 'pchipinterp';
opts = fitoptions( 'Method', 'PchipInterpolant' );
opts.ExtrapolationMethod = 'pchip';
opts.Normalize = 'on';

% 对数据进行模型拟合。
[fitresult, gof] = fit( xData, yData, ft, opts );

% 绘制数据拟合图。
figure( 'Name', '阶跃函数拟合' );
h = plot( fitresult, xData, yData );
legend( h, '原数据', '保形内插法插值', 'Location', 'NorthEast', 'Interpreter', 'none' );

xlabel( 'x', 'Interpreter', 'none' );
ylabel( 'y', 'Interpreter', 'none' );
grid on


%进行FFT变换
Y = fft(y,32);
%获取功率谱
yff = Y.*conj(Y);
%逆傅里叶变换
y_pred=sqrt(ifft(Y).*conj(ifft(Y)));
%截取原定义域
y_pred=y_pred(1:21);
%绘图
figure( 'Name', '阶跃函数拟合' );
h = plot(x,y_pred);
hold on
scatter(x,y)
legend( h,'FFT拟合', 'Location', 'NorthEast', 'Interpreter', 'none' );
xlabel( 'x', 'Interpreter', 'none' );
ylabel( 'y', 'Interpreter', 'none' );
grid on