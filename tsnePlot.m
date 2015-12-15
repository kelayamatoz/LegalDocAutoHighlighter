close all


pts = [[  72.31308301  -83.85423998] %0
 [  21.23691374   40.98170544]       %1
 [  -2.69489167 -115.84262008]       %2
 [  57.61849721  109.33748211]       %3
 [-147.75080222   10.33290337]       %4
 [  -1.15918759  -23.58749225]       %5
 [ 136.80329939   41.77528536]       %6
 [  96.33278427   74.38381844]       %7
 [ 111.09722928  -38.78210384]       %8
 [  68.45157449  -41.97973421]       %9
 [-108.43713521  -70.85172879]       %10
 [-107.44542431   61.16851817]       %11
 [  37.06337175   73.37893442]       %12
 [  41.33786738 -119.53072651]       %13
 [  23.70183386    6.0739176 ]       %14
 [ 404.18916483   -9.76697524]       %15
 [  66.0946113   531.19745944]       %16
 [ 115.06504209 -112.93860983]       %17
 [   0.8278755  -204.20184225]       %18
 [-153.92297423 -507.90575008]       %19
 [ -17.70152896   10.71457609]       %20
 [ -83.13430174  127.46196807]       %21
 [ -54.76235116   -5.9527989 ]       %22
 [ -19.31090576   51.5358193 ]       %23
 [ -91.28720148   22.3796068 ]       %24
 [  32.46279872  -31.76908681]       %25
 [-307.35180055   69.18767694]       %26
 [ -11.93001483  -71.53363177]       %27
 [ -50.70774086  -96.19600186]       %28
 [ -95.44445021  -19.98690837]       %29
 [-212.26232589   71.73729494]       %30
 [ -32.1000525   102.17186264]       %31
 [  62.48920332    1.35424569]       %32
 [  98.44960536    4.7746128 ]       %33
 [ -62.40392173  -56.33469884]       %34
 [   1.24251839   85.42355854]       %35
 [ -63.39315603   72.25593257]       %36
 [  28.19653529  -70.01872863]       %37
 [ 247.41688931  171.47375507]       %38
 [ -32.62724416  -35.97198785]       %39
 [ -54.08553405   34.56047575]       %40
 [  65.19573009   39.60228373]];        %41


targetPtsIndices = [34, 25, 33, 12, 31, 41, 26, 5, 22, 35, 20];
% targetPtsIndics = [26, 34];

pts1 = pts(:,1);
pts2 = pts(:,2);
scatter(pts1, pts2);
hold on;
scatter(pts1(targetPtsIndices + 1), pts2(targetPtsIndices + 1), 'r')
hold off;
