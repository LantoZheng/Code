% 定义参数
L = 10; % 总长度
c = -0.5; % 波速
dt = 0.05; % 时间步长
dx = 0.01; % 空间步长
t_end = 200000; % 总时间

x = 0:dx:L; % 空间网格
t = 0:dt:t_end; % 时间网格

% 初始化波形
u1 = zeros(size(x)); % 正三角形波
u2 = zeros(size(x)); % 半圆形波

% 正三角形波的参数
tri_center = 0;
tri_width = 1;
tri_height = 1;

% 半圆形波的参数
semi_center = L;
semi_radius = 1;

% 创建图形窗口
figure;
ax = gca;
ax.XLim = [0, L];
ax.YLim = [0, 1.5];

% 绘制初始波形
u = u1+u2
line = plot(x, u, 'b-', 'LineWidth', 2);
title('Wave Interaction');
xlabel('x');
ylabel('Amplitude');
grid on;

% 动画循环
for n = 1:length(t)
    % 更新正三角形波
    u1 = zeros(size(x));
    tri_left = tri_center - tri_width/2 - c*t(n);
    tri_right = tri_center + tri_width/2 - c*t(n);
    for i = 1:length(x)
        if x(i) >= tri_left && x(i) <= tri_center - c*t(n)
            u1(i) = tri_height * (x(i) - tri_left) / (tri_width/2);
        elseif x(i) > tri_center - c*t(n) && x(i) <= tri_right
            u1(i) = tri_height * (tri_right - x(i)) / (tri_width/2);
        end
    end
    
    % 更新半圆形波
    u2 = zeros(size(x));
    for i = 1:length(x)
        if (x(i) - (semi_center + c*t(n)))^2 <= semi_radius^2
            u2(i) = sqrt(semi_radius^2 - (x(i) - (semi_center + c*t(n)))^2);
        end
    end
    
    % 更新图形
    line.YData = u1+u2;
    pause(0.05)
    drawnow;
end