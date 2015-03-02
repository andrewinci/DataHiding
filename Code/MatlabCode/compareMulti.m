%import from database
addpath ~/Dev/matlab-sqlite3-driver/
sqlite3.open('/Users/darka/Dev/DataHiding/Code/cache/articles.db');
corr = sqlite3.execute('select * from comparated_image;');
corr_size = size(corr);
corr_size = corr_size(2);
for i=1:corr_size
id_base = corr(i).img_base_id;
id_corr = corr(i).img_corr_id;
[H,S,C] = getParameter(corr(i))
clc;
%disp(['processed' i ' relation over' corr_size])
fprintf('processed %d reation over %d\n H = %2.2f, S = %2.2f, C = %2.2f',i,corr_size,H,S,C);
%disp([H,S,C]);
%save to database
sqlite3.execute('update comparated_image set Harris = ?, SURF = ?, correlation = ?, is_similar = 2 where img_base_id =? and img_corr_id =?;', H, S, C, id_base, id_corr );
end
