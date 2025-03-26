function draw_obj(ax, obj)
% Draws an object imported using csv2obj in a MATLAB axes specified by ax.


initial_plotstate = ax.NextPlot();
ax.NextPlot = "add";

draw_obj_internal(obj, [0;0;0], eye(3))
ax.NextPlot = initial_plotstate;


function draw_obj_internal(obj, accumulated_position, accumulated_attitude)
if isfield(obj, "position"); position = obj.position; else; position = [0;0;0]; end
if isfield(obj, "attitude"); attitude = obj.attitude; else; attitude = eye(3) ; end

if isfield(obj, "mesh")
try mesh = evalin("base", filename2varname(obj.mesh)); catch; mesh = stlread(obj.mesh); assignin("base", filename2varname(obj.mesh), mesh); end
new_mesh = mesh;
new_mesh_Points = accumulated_position' + (new_mesh.Points*(attitude') + position'  )*accumulated_attitude';
new_mesh_tri    = triangulation(mesh.ConnectivityList, new_mesh_Points);
trisurf(new_mesh_tri);
end

accumulated_position = accumulated_position + attitude*position;
accumulated_attitude = attitude*accumulated_attitude;

property_names = fieldnames(obj);
for property_number = 1:numel(property_names);
property_name = property_names{property_number};
if isequal(class(obj.(property_name)), "struct")
draw_obj_internal(obj.(property_name), accumulated_position, accumulated_attitude);
end


end

end

end