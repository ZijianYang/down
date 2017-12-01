from . import main
from flask import redirect, url_for, render_template, request
import Tool

@main.before_request  
def before_request():  
    ismobile = Tool.IsMobile.get()  
    if ismobile:
        return redirect("mobile", code=302)
