function obj2csv(filename, obj)
% Saves down an obj-struct with parameters position, attitude and/or mesh plus additional optinal parameters and child-sctructs to a .csv file.
    
    File = fopen(filename, 'w');
    
    path_elements = split(filename, "\");
    name = path_elements{end};
    name = split(name, ".");
    name = name{1};
    path = erase(filename, path_elements{end});
    
    fprintf(File, name);
    write_branches(name, obj);
    fprintf(File, ",,,,,\n");

    fclose(File);
    
        function write_branches(trace, branches)
            branch_names = fieldnames(branches);
            for branch_index = 1:numel(branch_names)
                branch_name = branch_names{branch_index};

                fprintf(File, ",,,,,,\n");
                fprintf(File,trace+"."+branch_name);
                fprintf(File, ",,,,,\n");

                is_meshpath = isequal(branch_name, "mesh");
                if      isequal(class(branches.(branch_name)), "struct"); is_parent = true; else;  is_parent = false; end
                try if ~isnan(double(branches.(branch_name)));            is_matrix = true; else ; is_matrix = false; end 
                                                                                            catch; is_matrix = false; end
                try           string(branches.(branch_name) );            is_string = true; catch; is_string = false; end


                if is_meshpath
                    mesh_filename = split(branches.(branch_name), "\");
                    mesh_filename = mesh_filename{end};
                    if isequal(path, ""); path = "."; end
                    mesh_destination = path+mesh_filename;
                    if ~isequal(branches.(branch_name), mesh_destination); copyfile(branches.(branch_name), mesh_destination); end
                end
                %% Set priority-order by ordering the if-statements:
                if     is_parent;   write_branches(trace+"."+branch_name,                  branches.(branch_name) );
                elseif is_meshpath; fwrite        (File,                                   mesh_filename          );
                elseif is_matrix;   fprintf       (File,        matrix2csvtext(double(branches.(branch_name)),","));
                elseif is_string;   fwrite        (File,                            string(branches.(branch_name)));
                else;               fprintf       (File,                                                 "MISSING");
                end
                
            end
    
    
        end
    end