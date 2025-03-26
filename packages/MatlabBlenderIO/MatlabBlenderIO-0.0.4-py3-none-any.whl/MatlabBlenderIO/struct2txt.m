function struct2txt(filename, historian, times)

if exist("times", "var"); historian = query_historian(historian, historian, times); end

File = fopen(filename, 'w');
fclose(File);
path_elements = split(filename, "\");
path = replace(filename, "\"+path_elements(end),"");
name = replace(path_elements(end), ".txt", "");
write_branches(name, historian);


    function write_branches(trace, branches)
        branch_names = fieldnames(branches);
        for branch_index = 1:numel(branch_names)
            branch_name = branch_names{branch_index};

            

            writematrix(trace+"."+branch_name, filename, "delimiter", ",", 'WriteMode','append');
            
                                                is_mesh   = isequal(branch_name, "mesh");
                                                is_parent = isequal(class(branches.(branch_name)), "struct");
            try double(branches.(branch_name)); is_matrix = true; catch; is_matrix = false; end
            try string(branches.(branch_name)); is_string = true; catch; is_string = false; end 
            

                
            if     is_parent; write_branches(trace+"."+branch_name, branches.(branch_name));
            elseif is_mesh 
                    mesh_fileparts = split(branches.(branch_name), "\");
                    mesh_filepath  = path +"\"+ mesh_fileparts{end};                 
                    copyfile(branches.(branch_name), mesh_filepath);
                              writematrix(       mesh_filepath           , filename, "Delimiter", ",", 'WriteMode','append');    
            elseif is_matrix; writematrix(double(branches.(branch_name)) , filename, "Delimiter", ",", 'WriteMode','append');
            elseif is_string; writematrix(string(branches.(branch_name)) , filename, "Delimiter", ",", 'WriteMode','append');
            else;             writematrix("MISSING",                       filename, "Delimiter", ",", 'Writemode','append');
            end
            
        end
        end


end
