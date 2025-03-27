import webview
import os
import io
import sys

import roon.allpy2json as allpy2json
import roon.engine as engine

import importlib.resources as resources
import http.server
import socketserver
import threading

from importlib.metadata import version
try:
    import tomllib
except ImportError:
    import tomli as tomllib

def get_version(package_name):
    try:
        return version(package_name)
    except ImportError:
        with open("pyproject.toml", "rb") as f:
            data = tomllib.load(f)
        return data["project"]["version"]

base_dir = None

# Path to your Svelte app's build folder
svelte_build_dir = os.path.abspath("./roon/static/svelte")  # Adjust path as needed

# Global server reference for clean shutdown
httpd = None

# Serve the Svelte app locally
def start_server():
    global httpd

    """Start an HTTP server to serve Svelte static files."""
    # Check if the Svelte build directory exists
    try:
        with resources.path("roon.static", "svelte") as svelte_path:
            svelte_build_dir = str(svelte_path)
        if not os.path.exists(svelte_build_dir):
            raise FileNotFoundError(f"Svelte build directory not found: {svelte_build_dir}")
    except Exception as e:
        print(f"Error finding Svelte build directory: {e}")
        svelte_build_dir = os.path.abspath("/Users/brandenburg.89/Development/rune/svelte/svelte-node-graph/roon/static/svelte")  # Adjust path as needed

    os.chdir(svelte_build_dir)
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    # Custom TCPServer with SO_REUSEADDR
    class ReuseTCPServer(socketserver.TCPServer):
        allow_reuse_address = True  # Enable port reuse

    # Start the server
    httpd = ReuseTCPServer(("", PORT), Handler)

    # Run server in a separate thread
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return f"http://localhost:{PORT}"

# Python functions to expose to JavaScript

exec_globals = {}
exec_locals = {}
class Api:
    def run_python(self, code, globals=None, locals=None):
        """Run Python code in a specific directory and return the result."""
        try:
            # Capture stdout and stderr
            stdout_buffer = io.StringIO()
            stderr_buffer = io.StringIO()
            sys.stdout = stdout_buffer
            sys.stderr = stderr_buffer

            exec_globals.update({ "cwd": base_dir, "ROON": True })

            # add globals to exec_globals
            if globals is not None:
                exec_globals.update(globals)
            if locals is not None:
                exec_locals.update(locals)
            # Execute code
            exec(code, exec_globals, exec_locals)

            # Restore stdout/stderr
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            return {
                "result": exec_globals.get("result", exec_locals.get("result", "UNABLE to find RESULT in globals or locals")),
                "output": stdout_buffer.getvalue(),
                "error": stderr_buffer.getvalue()
            }
        except Exception as e:
            return {
                "result": None,
                "output": stdout_buffer.getvalue(),
                "error": str(e)
            }
        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

def full_setup():
    # Start the local server
    url = start_server()

    # Create the web view window
    api = Api()
    window = webview.create_window(
        "roon - " + get_version("roon"),
        url,
        js_api=api,  # Expose Python functions to JS
        width=800,
        height=600,
        resizable=True,
        fullscreen=True,
        # frameless=True,
        # transparent=True,
        # background_color='#00000000'
        # vibrancy=True
    )

      # Inject JS to set a custom flag when the page loads
    window.events.loaded += lambda: window.evaluate_js("""
      window.is_pywebview = true; // Custom flag
      console.log("PyWebView flag set");
    """)

    # Cleanup on window close
    def on_closed():
        global httpd
        if httpd:
            print("Shutting down server...")
            httpd.shutdown()
            httpd.server_close()
            httpd = None
    
    window.events.closed += on_closed

    webview.start(debug=True)

if __name__ == "__main__":
    print("Calling from: ", os.getcwd())
    base_dir = os.getcwd()
    full_setup()