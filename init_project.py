import os
import sys
import subprocess
import json
from rich.console import Console
from rich.style import Style
from rich.theme import Theme

THEME_STYLES = {
    "info": Style(color="cyan"),
    "success": Style(color="green"),
    "warning": Style(color="yellow"),
    "error": Style(color="red"),
    "title": Style(color="bright_cyan"),
}
THEME = Theme(styles=THEME_STYLES)

console = Console(highlight=False, theme=THEME)

def setup_node_project(folder_path):
    """Sets up a Node.js project by installing dependencies and adding npm scripts."""
    if not os.path.exists(folder_path):
        console.print(f"[+] Error: The folder '{folder_path}' does not exist.", style="error")
        return

    if not os.path.isdir(folder_path):
        console.print(f"Error: '{folder_path}' is not a folder.", style="error")
        return

    # Install dependencies
    dependencies = ["express", "mysql2", "dotenv", "nodemon"]

    console.print("[+] Installing dependencies...", style="info")
    try:
        path = subprocess.run(["where", "npm.cmd"], capture_output=True).stdout.decode().strip()
    except:
        console.print("[+] Error: Unable to find npm. Exiting!", style="error")
        
    subprocess.run([r"C:\Program Files\nodejs\npm.cmd", "install"] + dependencies, check=True)
    console.print("[+] Installed successfully!", style="success")
    # Update package.json with npm scripts
    package_json_path = os.path.join(folder_path, "package.json")

    if os.path.exists(package_json_path):

        with open(package_json_path, "r") as file:
            package_data = json.load(file)

        package_data.setdefault("scripts", {})  # Ensure scripts key exists
        package_data["scripts"].update({
            "start": "node index.js",
            "dev": "nodemon index.js"
        })

        with open(package_json_path, "w") as file:
            json.dump(package_data, file, indent=2)

        console.print("[+] Updated npm scripts in package.json", style="success")
    else:
        console.print("Warning: No package.json found. Please run 'npm init' first.", style="warning")


def setup_appjs(path):
    """Checks if there's code between the predefined section markers and updates if empty."""
    path = os.path.join(path, "src/app.js")
    if not os.path.exists(path):
        console.print(f"[+]Error: The file '{path}' does not exist.", style="error")
        return
    appjs = """//////////////////////////////////////////////////////
// INCLUDES
//////////////////////////////////////////////////////
const express = require('express');

//////////////////////////////////////////////////////
// CREATE APP
//////////////////////////////////////////////////////
const app = express();

//////////////////////////////////////////////////////
// USES
//////////////////////////////////////////////////////
app.use(express.json());
app.use(express.urlencoded({extended:false}));

//////////////////////////////////////////////////////
// SETUP ROUTES
//////////////////////////////////////////////////////
const mainRoutes = require('./routes/mainRoutes');
app.use("/", mainRoutes);

//////////////////////////////////////////////////////
// EXPORT APP
//////////////////////////////////////////////////////
module.exports = app;"""
    with open(path, "w") as file:
        file.write(appjs)
    console.print("[+] app.js successfully added!", style="success")

def setup_indexjs(path):
    """Checks if there's code between the predefined section markers and updates if empty."""
    path = os.path.join(path, "index.js")
    if not os.path.exists(path):
        console.print(f"[+]Error: The file '{path}' does not exist.", style="error")
        return
    indexjs = """//////////////////////////////////////////////////////
// INCLUDES
//////////////////////////////////////////////////////
const app = require('./src/app');

//////////////////////////////////////////////////////
// SETUP ENVIRONMENT
//////////////////////////////////////////////////////
const PORT = 3000;

//////////////////////////////////////////////////////
// START SERVER
//////////////////////////////////////////////////////
app.listen(PORT,()=> {
    console.log(`App listening to port ${PORT}`);
});"""
    with open(path, "w") as file:
        file.write(indexjs)
    console.print("[+] index.js successfully added!", style="success")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        console.print("Usage: python init_project.py <folder_path>")
    else:
        folder_path = sys.argv[1]
        folder_path = os.path.abspath(folder_path)
        os.chdir(folder_path)

        setup_appjs(folder_path)
        setup_indexjs(folder_path)
        setup_node_project(folder_path)
