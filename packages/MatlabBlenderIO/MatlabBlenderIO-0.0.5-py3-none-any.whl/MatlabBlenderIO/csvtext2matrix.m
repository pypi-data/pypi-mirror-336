function [mat, dimension_length] = csvtext2matrix(text)

text = erase(text, char(10));
text = string(text);
if contains(text, ",")

[highest_delimiter_number, lowest_delimiter_number] = find_comma_sequences(text);
highest_delimiter = strjoin(repmat(",", 1,highest_delimiter_number),"");
lowest_delimiter  = strjoin(repmat(",", 1,lowest_delimiter_number ),"");


dimensions         = highest_delimiter_number - lowest_delimiter_number+1;
dimension_length   = zeros(1,dimensions);
delimiter_iterator = highest_delimiter;
dimension_iterator = dimensions;
module             = 1;

while true
data_split_along_dim                 = split(text, delimiter_iterator);
data_split_along_dim                 = data_split_along_dim(~strcmp(data_split_along_dim, ""));
dimension_length(dimension_iterator) = numel(data_split_along_dim)/module;
module                               = module*dimension_length(dimension_iterator);

if isequal(delimiter_iterator, lowest_delimiter)
break
else
delimiter_iterator = extractBefore(delimiter_iterator, strlength(delimiter_iterator));
dimension_iterator = dimension_iterator -1;
end

end

flat_data          = split(text, ",");
flat_data          = flat_data(~strcmp(flat_data, ""));
flat_data          = double(flat_data);
if numel(dimension_length)>1; mat = reshape(flat_data, dimension_length);
else;                         mat = flat_data;
end

else
mat = double(text); dimension_length = 0;


end


end



function [longest, smallest] = find_comma_sequences(text)

comma_sequences = regexp(text, ',+', 'match');
lengths         = cellfun(@length, comma_sequences);
    
if ~isempty(lengths); longest = max(lengths); smallest = min(lengths);
else;                 longest = 0;            smallest = 0;
end

end