#!/usr/bin/env python
import os
from App import create_app
from flask_script import Manager, Shell


APP = create_app()
MANAGER = Manager(APP)

def make_shell_context():
    return dict(app=APP)

MANAGER.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    MANAGER.run()
