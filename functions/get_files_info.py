import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs , directory))
        
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        content = os.listdir(target_dir)
        data = []
            
                    
        for c in content:
            name = c
            path = os.path.join(target_dir,name)
            size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            
            details = {
                "name" : name,
                "size" : size,
                "is_dir" : is_dir
            }
                        
            data.append(details)
                
        string_of_data = ""
        for d in data:
            string_of_data += f"- {d["name"]}: file_size={d["size"]} bytes, is_dir={d["is_dir"]}\n"
                
        return string_of_data

    except Exception as e:
        return f"Error: {e}"
        
    
    


    