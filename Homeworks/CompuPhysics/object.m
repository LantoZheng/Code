% 构建物体三维物体类
classdef object
    properties
        points = []; % 三维物体的顶点，为n*3的矩阵
        slides = []; % 三维物体的面，为n*3的矩阵，每行值为该面元的三个顶点在points中的索引
        additional = struct('activate', 0, 'brightness', [], 'color', []); % 各个面元的亮度和色彩
    end
    methods
        function bu = iscovered(obj, slide_number, observer) 
            % 检测从observer出发的光线是否被遮挡
            % slide_number: 被观察的面片编号
            % observer: 观察者位置, 1x3 向量
            % bu: 返回true如果被遮挡，否则返回false
            
            % 获取要检查的面片
            slide = obj.slides(slide_number, :);
            % 计算面片的中心
            center = mean(obj.points(slide, :), 1);
            % 计算从观察者到面片中心的方向向量，并归一化
            n = center - observer;
            n = n / norm(n);
            % 遍历其他面片
            bu = false;
            for i = 1:size(obj.slides, 1)
                if i ~= slide_number
                    other_slide = obj.slides(i, :);
                    % 获取其他面片的三个顶点
                    p1 = obj.points(other_slide(1), :);
                    p2 = obj.points(other_slide(2), :);
                    p3 = obj.points(other_slide(3), :);
                    % 检查光线是否与面片相交
                    if obj.rayIntersectsTriangle(observer, n, p1, p2, p3)
                        bu = true;
                        return;
                    end
                end
            end
        end

        function obj = move(obj, x, y, z)
            % 移动物体的所有顶点
            % x, y, z: 移动的距离
            
            for i = 1:size(obj.points, 1)
                obj.points(i, :) = obj.points(i, :) + [x, y, z];
            end
        end
    end

    methods (Static)
        function intersect = rayIntersectsTriangle(rayOrigin, rayVector, vertex0, vertex1, vertex2)
            % Möller-Trumbore ray-triangle intersection algorithm
            % 检查光线是否与三角形相交
            % rayOrigin: 光线起点, 1x3 向量
            % rayVector: 光线方向向量, 1x3 向量
            % vertex0, vertex1, vertex2: 三角形的三个顶点, 1x3 向量
            % intersect: 返回true如果相交，否则返回false
            
            intersect = false;
            epsilon = 1e-6;

            edge1 = vertex1 - vertex0;
            edge2 = vertex2 - vertex0;
            h = cross(rayVector, edge2);
            a = dot(edge1, h);

            if a > -epsilon && a < epsilon
                return; % 光线与三角形平行
            end

            f = 1.0 / a;
            s = rayOrigin - vertex0;
            u = f * dot(s, h);

            if u < 0.0 || u > 1.0
                return;
            end

            q = cross(s, edge1);
            v = f * dot(rayVector, q);

            if v < 0.0 || u + v > 1.0
                return;
            end

            t = f * dot(edge2, q);

            if t > epsilon % 光线相交
                intersect = true;
            end
        end
    end
end

% 参考文献:
% Möller, T., & Trumbore, B. (1997). Fast, minimum storage ray-triangle intersection. Journal of Graphics Tools, 2(1), 21-28. DOI: 10.1080/10867651.1997.10487468
% Shirley, P. (2005). Fundamentals of Computer Graphics. A K Peters/CRC Press.
% Glassner, A. S. (1989). An Introduction to Ray Tracing. Academic Press.
