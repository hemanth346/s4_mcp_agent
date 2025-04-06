# basic import 
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
import math
import sys
import time
import os  # For env variables
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Optional
from dotenv import load_dotenv
load_dotenv()

# from PIL import Image as PILImage
# from pywinauto.application import Application
# import win32gui
# import win32con
# from win32api import GetSystemMetrics
import subprocess

# instantiate an MCP server client
mcp = FastMCP("Test")

# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("CALLED: add(a: int, b: int) -> int:")
    return int(a + b)

@mcp.tool()
def add_list(l: list) -> int:
    """Add all numbers in a list"""
    print("CALLED: add(l: list) -> int:")
    return sum(l)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)

# square root tool
@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    print("CALLED: sqrt(a: int) -> float:")
    return float(a ** 0.5)

# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(string: str) -> list[int]:")
    return [int(ord(char)) for char in string]

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(int_list: list) -> float:")
    return sum(math.exp(i) for i in int_list)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]


@mcp.tool()
async def draw_rectangle(x1: int, y1: int, x2: int, y2: int) -> dict:
    """Draw a rectangle in Paint from (x1,y1) to (x2,y2)"""
    global paint_app
    try:
        if not paint_app:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Paint is not open. Please call open_paint first."
                    )
                ]
            }
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Get primary monitor width to adjust coordinates
        primary_width = GetSystemMetrics(0)
        
        # Ensure Paint window is active
        if not paint_window.has_focus():
            paint_window.set_focus()
            time.sleep(0.2)
        
        # Click on the Rectangle tool using the correct coordinates for secondary screen
        paint_window.click_input(coords=(530, 82 ))
        time.sleep(0.2)
        
        # Get the canvas area
        canvas = paint_window.child_window(class_name='MSPaintView')
        
        # Draw rectangle - coordinates should already be relative to the Paint window
        # No need to add primary_width since we're clicking within the Paint window
        canvas.press_mouse_input(coords=(x1+2560, y1))
        canvas.move_mouse_input(coords=(x2+2560, y2))
        canvas.release_mouse_input(coords=(x2+2560, y2))
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Rectangle drawn from ({x1},{y1}) to ({x2},{y2})"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error drawing rectangle: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def add_text_in_paint(text: str) -> dict:
    """Add text in Paint"""
    global paint_app
    try:
        if not paint_app:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Paint is not open. Please call open_paint first."
                    )
                ]
            }
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Ensure Paint window is active
        if not paint_window.has_focus():
            paint_window.set_focus()
            time.sleep(0.5)
        
        # Click on the Rectangle tool
        paint_window.click_input(coords=(528, 92))
        time.sleep(0.5)
        
        # Get the canvas area
        canvas = paint_window.child_window(class_name='MSPaintView')
        
        # Select text tool using keyboard shortcuts
        paint_window.type_keys('t')
        time.sleep(0.5)
        paint_window.type_keys('x')
        time.sleep(0.5)
        
        # Click where to start typing
        canvas.click_input(coords=(810, 533))
        time.sleep(0.5)
        
        # Type the text passed from client
        paint_window.type_keys(text)
        time.sleep(0.5)
        
        # Click to exit text mode
        canvas.click_input(coords=(1050, 800))
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Text:'{text}' added successfully"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def open_paint() -> dict:
    """Open Microsoft Paint maximized on secondary monitor"""
    global paint_app
    try:
        paint_app = Application().start('mspaint.exe')
        time.sleep(0.2)
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Get primary monitor width
        primary_width = GetSystemMetrics(0)
        
        # First move to secondary monitor without specifying size
        win32gui.SetWindowPos(
            paint_window.handle,
            win32con.HWND_TOP,
            primary_width + 1, 0,  # Position it on secondary monitor
            0, 0,  # Let Windows handle the size
            win32con.SWP_NOSIZE  # Don't change the size
        )
        
        # Now maximize the window
        win32gui.ShowWindow(paint_window.handle, win32con.SW_MAXIMIZE)
        time.sleep(0.2)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text="Paint opened successfully on secondary monitor and maximized"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening Paint: {str(e)}"
                )
            ]
        }
    

# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

@mcp.tool()
async def send_email(
    subject: str, 
    body: str
) -> dict:
    """
    Sends an email using input parameters
    
    Args:
        subject (str): Subject of the email
        body (str): Body content of the email
    
    Returns:
        dict: Status of the operation with success/error message

    """
    try:
        # Get credentials from environment variables
        sender_email = os.environ.get("EMAIL_SENDER")
        smtp_password = os.environ.get("EMAIL_PASSWORD")
        recipient_email = os.environ.get("EMAIL_RECIPIENT")
        
        # Check if required environment variables are set
        if not sender_email:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Error: EMAIL_SENDER not set in environment. Please create a .env file with your credentials."
                    )
                ]
            }
                
        if not smtp_password:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Error: EMAIL_PASSWORD not set in environment. Please create a .env file with your credentials."
                    )
                ]
            }
        
        if not recipient_email:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Error: EMAIL_RECIPIENT not set in environment. Please create a .env file with your credentials."
                    )
                ]
            }
        
        # Default SMTP settings for Gmail
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
                
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = f"{subject}"
        
        # Add body to email
        message.attach(MIMEText(f"{body}", "plain"))
        
        # Create SMTP session
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            
            # Log the connection attempt
            print(f"CALLED: send_email - Connecting to {smtp_server}:{smtp_port} as {sender_email}")
            
            # Try to login
            server.login(sender_email, smtp_password)
            
            # Send the message
            server.send_message(message)
            print(f"CALLED: send_email - Email sent successfully to {recipient_email}")
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Email sent successfully to {recipient_email}"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error sending email: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def create_keynote_slide_with_content(
    text: str = "Hello World"
) -> dict:
    """
    Creates a new Keynote slide with a styled rectangle and centered text.
    
    Args:
        text (str): Text to be added inside the rectangle. Defaults to "Hello World"
    
    Returns:
        dict: A dictionary containing:
            - status: Success/failure of the operation
            - message: Detailed status message
    """
    try:
        # First check if Keynote is available
        check_result = subprocess.run(
            ['osascript', '-e', 'tell application "Keynote" to version'], 
            capture_output=True, 
            text=True
        )
        
        if check_result.returncode != 0:
            return {
                "status": "error",
                "message": f"Keynote is not available: {check_result.stderr.strip()}"
            }
            
        # Escape quotes in text for AppleScript
        safe_text = text.replace('"', '\\"').replace('\\', '\\\\')
        
        # Step 1: Ensure Keynote is open and a document exists
        setup_script = '''
        tell application "Keynote"
            activate
            if not (exists document 1) then
                make new document
            end if
        end tell
        '''
        
        setup_result = subprocess.run(['osascript', '-e', setup_script], capture_output=True, text=True)
        if setup_result.returncode != 0:
            return {
                "status": "error",
                "message": f"Failed to setup Keynote: {setup_result.stderr.strip()}"
            }
            
        # Step 2: Ensure we have a slide
        slide_script = '''
        tell application "Keynote"
            tell front document
                if (count of slides) is 0 then
                    make new slide at end of slides
                end if
            end tell
        end tell
        '''
        
        slide_result = subprocess.run(['osascript', '-e', slide_script], capture_output=True, text=True)
        if slide_result.returncode != 0:
            return {
                "status": "error",
                "message": f"Failed to create slide: {slide_result.stderr.strip()}"
            }
            
        # Step 3: Create a shape
        shape_script = '''
        tell application "Keynote"
            tell front document
                tell slide 1
                    make new shape
                end tell
            end tell
        end tell
        '''
        
        shape_result = subprocess.run(['osascript', '-e', shape_script], capture_output=True, text=True)
        if shape_result.returncode != 0:
            return {
                "status": "error",
                "message": f"Failed to create shape: {shape_result.stderr.strip()}"
            }

        # Step 4: Set width, height, and position
        size_script = '''
        tell application "Keynote"
            tell front document
                tell slide 1
                    tell last shape
                        set width to 500
                        set height to 300
                        set position to {262, 234}
                    end tell
                end tell
            end tell
        end tell
        '''
        
        size_result = subprocess.run(['osascript', '-e', size_script], capture_output=True, text=True)
        if size_result.returncode != 0:
            return {
                "status": "error",
                "message": f"Failed to size/position shape: {size_result.stderr.strip()}"
            }
        
        # Step 5: Set text content
        text_script = f'''
        tell application "Keynote"
            tell front document
                tell slide 1
                    tell last shape
                        set object text to "{safe_text}"
                    end tell
                end tell
            end tell
        end tell
        '''
        
        text_result = subprocess.run(['osascript', '-e', text_script], capture_output=True, text=True)
        if text_result.returncode != 0:
            return {
                "status": "error",
                "message": f"Failed to set text: {text_result.stderr.strip()}"
            }
            
        # Step 6: Format text
        format_script = '''
        tell application "Keynote"
            tell front document
                tell slide 1
                    tell last shape
                        tell object text
                            set size to 24
                            set font to "Helvetica"
                        end tell
                    end tell
                end tell
            end tell
        end tell
        '''
        
        format_result = subprocess.run(['osascript', '-e', format_script], capture_output=True, text=True)
        if format_result.returncode != 0:
            return {
                "status": "error",
                "message": f"Failed to format text: {format_result.stderr.strip()}"
            }
            
        # If we got here, everything worked
        return {
            "status": "success", 
            "message": "Slide created successfully with rectangle and text"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution
