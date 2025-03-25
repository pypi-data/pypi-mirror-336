import re

def get_format_date_py(format_value):
    # Mapping format custom ke format strftime
    format_mapping = {
        "yyyy": "Y",
        "yy": "y",
        "mmmm": "B", 
        "mmm": "b",  
        "mm": "m",    
        "dd": "d",    
        "hh": "H",    
        "h": "I",     
        "MM": "M",   
        "ss": "S",    
        "a": "p"      
    }

    # Hilangkan tanda "-" hanya jika setelah "\"
    format_value = re.sub(r'[;@]', '', format_value)
    format_value = re.sub(r"\\-", r"-", format_value)

    # Split berdasarkan pemisah (termasuk tanda backslash)
    format_parts = re.split(r'([-:/\\\s])', format_value)

    # Konversi format yang dikenali
    for key, value in format_mapping.items():
        format_value = format_value.replace(key, f"%{value}")

    return format_value