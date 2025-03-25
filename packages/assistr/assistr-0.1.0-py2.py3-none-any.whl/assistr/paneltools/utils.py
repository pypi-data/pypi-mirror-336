
import param
from panel.custom import JSComponent


frost_css =  f""" 
.title 
{{color:#2b2b2b !important; 
font-family: "Noto Sans","Noto Sans Arabic",Arial,Sans-Serif!important;
font: 550 20px/30px Noto Sans,Arial,"Sans-Serif"!important;
white-space: nowrap!important;
cursor: default!important;
letter-spacing: .05rem!important;
font-size: 12px!important;
font-weight: 600!important;
letter-spacing: .05rem!important;
vertical-align:middle!important; 
-webkit-font-smoothing: antialiased;
 }}

 #header {{ 
    height: 40px!important;
 }}

.header-adjust {{
    padding-top: 40px!important;
}}

.app-header  {{
    display : flex;
    align-items : center;
}} 
 
.sidebar-contents {{

    background-color: #F4F5F7!important;
}}

.lm_content {{ 
    background: #F4F5F7!important;
}}

.bk-Row {{
    display : flex;
    align-items : center;
    -webkit-font-smoothing: antialiased;
}}
"""


class CounterButton(JSComponent):

    _esm = """
    <form>  
      <select id = "main-menu" onchange = "handleMenu()" >  
      <option>Menu</option>  
      <option>resetState</option>  
      <option>NextItem</option>  
      </select>  
      </form>  
    """
    