% 构建物体三维物体类
classdef imObject
    properties
        points = []; % 三维物体的顶点，为n*3的矩阵
        slides = []; % 三维物体的面，为n*3的矩阵，每行值为该面元的三个顶点在points中的索引
        additional = struct('activate', 0, 'brightness', [], 'color', []); % 各个面元的亮度和色彩
    end
    methods
        function bu = IsCovered(obj, slide_number, observer) 
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

        function visibleSlides = VisibleSlides(obj, observer)
            % 查找从observer观察能够不被遮挡的片元
            % observer: 观察者位置, 1x3 向量
            % visibleSlides: 可见片元的索引
            
            numSlides = size(obj.slides, 1);
            visibleSlides = [];
            
            for i = 1:numSlides
                slide = obj.slides(i, :);
                % 计算面片的中心
                center = mean(obj.points(slide, :), 1);
                % 计算从观察者到面片中心的方向向量，并归一化
                n = center - observer;
                n = n / norm(n);
                % 检查该片元是否被其他片元遮挡
                IsCovered = false;
                for j = 1:numSlides
                    if j ~= i
                        other_slide = obj.slides(j, :);
                        % 获取其他面片的三个顶点
                        p1 = obj.points(other_slide(1), :);
                        p2 = obj.points(other_slide(2), :);
                        p3 = obj.points(other_slide(3), :);
                        % 检查光线是否与面片相交
                        if obj.rayIntersectsTriangle(observer, n, p1, p2, p3)
                            IsCovered = true;
                            break;
                        end
                    end
                end
                if ~IsCovered
                    visibleSlides = [visibleSlides, i];
                end
            end
        end

        function groups = SlidesGroupByDistance(obj, observer, n)
            % 根据距离将片元分为n组
            % observer: 观察者位置, 1x3 向量
            % n: 分组数量
            % groups: 一个结构数组，每个结构包含一个字段index，表示该组片元的索引，和一个字段distance，表示该组片元的平均距离

            numSlides = size(obj.slides, 1);
            if numSlides == 0
                warning('No slides available in the object.');
                groups = struct('index', {}, 'distance', {});
                return;
            end

            distances = zeros(1, numSlides);

            for i = 1:numSlides
                slide = obj.slides(i, :);
                center = mean(obj.points(slide, :), 1);
                distances(i) = norm(center - observer);
            end

            [sortedDistances, sortedIndices] = sort(distances);
            groupSize = ceil(numSlides / n);
            groups = struct('index', cell(1, n), 'distance', cell(1, n));

            for i = 1:n
                startIdx = (i-1) * groupSize + 1;
                endIdx = min(i * groupSize, numSlides);
                groups(i).index = sortedIndices(startIdx:endIdx);
                groups(i).distance = mean(sortedDistances(startIdx:endIdx));
            end
        end


        function obj = move(obj, x, y, z)
            % 移动物体的所有顶点
            % x, y, z: 移动的距离
            one = ones(size(obj.points,1),1);
            obj.points = obj.points + [one .* x, one .* y, one .* z];
        end

        function brightness = calculateBrightness(obj, lightPos, lightIntensity, cameraPos)
            % 计算每个片元在相机处观察到的亮度
            % lightPos: 光源位置, 1x3 向量
            % lightIntensity: 光源亮度, 标量
            % cameraPos: 相机位置, 1x3 向量
            % brightness: 每个片元的亮度, 1xn 向量
            
            numSlides = size(obj.slides, 1);
            brightness = zeros(1, numSlides);
            for i = 1:numSlides
                slide = obj.slides(i, :);
                p1 = obj.points(slide(1), :);
                p2 = obj.points(slide(2), :);
                p3 = obj.points(slide(3), :);
                % 计算面片的法向量
                normal = cross(p2 - p1, p3 - p1);
                normal = normal / norm(normal);
                % 计算光线方向
                lightDir = lightPos - mean([p1; p2; p3], 1);
                lightDir = lightDir / norm(lightDir);
                % 计算相机方向
                viewDir = cameraPos - mean([p1; p2; p3], 1);
                viewDir = viewDir / norm(viewDir);
                % Lambertian光照模型计算亮度
                cosTheta = max(dot(normal, lightDir), 0);
                brightness(i) = lightIntensity * cosTheta;
            end
        end
        %Ref:Akenine-Möller, T., Haines, E., Hoffman, N. (2018). Real-Time Rendering. A K Peters/CRC Press.
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
