function matrix2csv(mat, file, writemode, starting_delimiter)
closefile = false;
if ~exist  ("writemode",          "var"); writemode          = "a";                                      end
if ~exist  ("starting_delimiter", "var"); starting_delimiter = ",";                                      end
if  isequal(class(file), "string"      ); file = fopen(file, writemode, 'n', 'UTF-8'); closefile = true; end


dims      = ndims(mat);
shape     = size(mat);

flatmat   = reshape(mat, numel(mat), 1);
nelements = numel(mat);

denominator_multiplier = [1,shape];

for index = 1:nelements

fprintf(file, string(flatmat(index)));

if index ~= nelements
fprintf(file,starting_delimiter);
for dim = 1:dims
if rem(index, shape(dim)*prod(denominator_multiplier(1:dim))) == 0; fprintf(file,","); end
end
for dim = 1:dims
if rem(index, shape(dim)*prod(denominator_multiplier(1:dim))) == 0; fprintf(file,"\n"); end
end
end

end

if closefile;fclose(file); end