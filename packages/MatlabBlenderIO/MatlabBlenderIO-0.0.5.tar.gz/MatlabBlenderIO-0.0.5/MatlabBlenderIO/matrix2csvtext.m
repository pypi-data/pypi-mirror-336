function text = matrix2csvtext(mat, starting_delimiter)

if ~exist  ("starting_delimiter", "var"); starting_delimiter = ","; end

text                   = "";
dimensions             = ndims(mat);
dimension_lenghts      = size(mat);
flatmat                = reshape(mat, numel(mat), 1);
number_of_elements     = numel(mat);
denominator_multiplier = [1,dimension_lenghts];


for index = 1:number_of_elements


text = text+string(flatmat(index));

if index ~= number_of_elements
text = text+starting_delimiter;
for dim = 1:dimensions; if rem(index, dimension_lenghts(dim)*prod(denominator_multiplier(1:dim))) == 0; text = text+"," ; end; end
for dim = 1:dimensions; if rem(index, dimension_lenghts(dim)*prod(denominator_multiplier(1:dim))) == 0; text = text+"\n"; end; end
end

end
