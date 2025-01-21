import dash_bootstrap_components as dbc

#
navbar = dbc.NavbarSimple(
    brand="NYC Housing Profiler", 
    color="#006BB6", #NY dark blue color for main bar
    dark=True, 
    style={
        "borderBottom": "2px solid #ffffff",  # Optional subtle border underline of the brand
        "padding": "10px 20px",  # Adjust spacing 
    },
    brand_style={
        "color": "white",  # White brand 
        "fontSize": "25px", # font size of brand
        "fontWeight": "bold", # bold font
    },
    className="mt-3 mb-3"
)
