function data = query_csv(filename, inquiry)
% Query .csv for specific data.



contents = fileread(filename);
contents = erase(contents, sprintf('\n'));
contents = erase(contents, sprintf('\r'));
contents = erase(contents, newline);
contents = split(contents, ",,,,,,");
contents = contents(1:end-1);
inquiry  = contents{1}+"."+inquiry;
nums     = 1:numel(contents);
index    = nums(cellfun( @(i) contains(i, inquiry), contents' ));


if numel(index) > 1; index = index(1); warning("Multiple instances of inquiry found in file "+filename+". Choosing the first one."); end

element = split(contents{index}, ",,,,,");

try             data = csvtext2matrix(element{2});
if isnan(data); data = element{2}; end
catch;          data = element{2};
end


end