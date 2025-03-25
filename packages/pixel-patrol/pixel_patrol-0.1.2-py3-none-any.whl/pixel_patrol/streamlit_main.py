import os

def main():
    from streamlit.runtime.scriptrunner import get_script_run_ctx
    if get_script_run_ctx() is None:
        from streamlit.web.cli import main
        import sys
        sys.argv = ['streamlit', 'run', os.path.dirname(os.path.abspath(__file__)) + os.sep + "main.py"]
        main()
