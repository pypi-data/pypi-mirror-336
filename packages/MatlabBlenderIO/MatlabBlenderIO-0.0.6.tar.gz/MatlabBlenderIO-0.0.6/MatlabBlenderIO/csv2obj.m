function outstruct = csv2obj(filename)
% Takes in the filepath to an object stored as a .csv file, and imports it into MATLAB.
outstruct = struct();
outstruct.is_body = true;

path = split(filename, "\");
path = string(erase(filename, path{end}));

contents = fileread(filename);
contents = erase(contents, sprintf('\n'));
contents = erase(contents, sprintf('\r'));
contents = erase(contents, newline);
contents = split(contents, ",,,,,,");
contents = contents(1:end-1);

for content_index = 1:numel(contents)
parts     = split(contents(content_index), ",,,,,");
address   = split(parts{1}, ".");
is_mesh   = contains(parts{1}, "mesh");
is_parent = (numel(parts)==1);

if numel(address)>1
if      is_parent; outstruct = setfield(outstruct, address{2:end}, struct());
elseif  is_mesh  ; outstruct = setfield(outstruct, address{2:end}, path+string(parts{2}));
else;   try        outstruct = setfield(outstruct, address{2:end}, csvtext2matrix(parts{2}));
        catch;     outstruct = setfield(outstruct, address{2:end}, "MISSING");
        end
end
end

end



end