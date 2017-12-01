from . import main
from flask import redirect, url_for, render_template, request
import Tool

@main.before_request  
def before_request():  
    Tool.IsMobile.get()
    return redirect(url_for('.index'))
