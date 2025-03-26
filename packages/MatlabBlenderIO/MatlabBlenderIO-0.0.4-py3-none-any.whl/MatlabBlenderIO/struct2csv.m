function struct2csv(filename, historian, times)
    if exist("times", "var"); historian = query_historian(historian, historian, times); end
    
    File = fopen(filename, 'w');
    
    path_elements = split(filename, "\");
    name = path_elements{end};
    name = split(name, ".");
    name = name{1};
    path = replace(filename, path_elements(end),"");
    
    write_branches(name, historian);
    
    
        function write_branches(trace, branches)
            branch_names = fieldnames(branches);
            for branch_index = 1:numel(branch_names)
                branch_name = branch_names{branch_index};
                branches.(branch_name)
    
                fprintf(File,trace+"."+branch_name);
                fprintf(File, ",,,,\n");

                is_meshpath = isequal(branch_name, "mesh");
                try struct(branches.(branch_name)); is_parent = true; catch; is_parent = false; end
                try double(branches.(branch_name)); is_matrix = true; catch; is_matrix = false; end
                try string(branches.(branch_name)); is_string = true; catch; is_string = false; end


                if is_meshpath
                    mesh_filename = split(branches.(branch_name), "\");
                    mesh_filename = mesh_filename{end};
                    if isequal(path, ""); path = "."; end
                    mesh_destination = path+"\"+mesh_filename;
                    copyfile(branches.(branch_name), mesh_destination);
                end
                %% Set priority-order by ordering the if-statements:
                if     is_parent;   write_branches(trace+"."+branch_name,                  branches.(branch_name) );
                elseif is_meshpath; fwrite        (File,                                        mesh_destination  );
                elseif is_matrix;   fwrite        (File,        matrix2csvtext(double(branches.(branch_name)),","));
                elseif is_string;   fwrite        (File,      replace(  string(branches.(branch_name)), "\", "\\"));
                else;               fwrite        (File,                                                 "MISSING");
                end
                
                fprintf(File, "\n,,,,,\n");
            end
    
    
        end
    
    fclose(File);
    end