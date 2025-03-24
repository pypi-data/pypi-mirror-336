import os
import subprocess
import select
import time
import asyncio

def run_with_output(cmd):
    """Helper function to run commands and stream their output"""

    # print("Running command:", " ".join(cmd), flush=True)

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1
    )
    
    output = []
    # Use select to read from whichever pipe has data
    while True:
        reads = [process.stdout.fileno(), process.stderr.fileno()]
        ret = select.select(reads, [], [], 0.1)  # 0.1 second timeout
        
        for fd in ret[0]:
            if fd == process.stdout.fileno():
                line = process.stdout.readline()
                if line:
                    # print(line, end='', flush=True)
                    output.append(line)
            if fd == process.stderr.fileno():
                line = process.stderr.readline()
                if line:
                    # print("STDERR:", line, end='', flush=True)  # Clearly mark stderr output
                    output.append(line)
        
        # Check if process has finished
        if process.poll() is not None:
            # Read any remaining output
            for line in process.stdout.readlines():
                print(line, end='', flush=True)
                output.append(line)
            for line in process.stderr.readlines():
                print("STDERR:", line, end='', flush=True)
                output.append(line)
            break
        
        # Add a small sleep to prevent CPU spinning
        time.sleep(0.001)
    
    if process.returncode != 0:
        print(''.join(output))
        raise subprocess.CalledProcessError(process.returncode, cmd)
    
    return ''.join(output)

def install_dependencies():
    # Install system dependencies
    # try:
    #     run_with_output(['sudo', 'apt-get', 'update'])
    #     run_with_output(['sudo', 'apt-get', 'install', '-y', 'bash', 'xvfb', 'x11vnc', 'xterm', 'nodejs', 'npm'])
    #     run_with_output(['sudo', 'rm', '-rf', '/var/lib/apt/lists/*'])
    # except subprocess.CalledProcessError as e:
    #     print("Failed to install system dependencies:")
    #     print(e.output)
    #     raise

    # # Install playwright and dependencies
    # try:
    #     run_with_output(['sudo', 'npm', 'install', 'create-playwright'])
    #     run_with_output(['sudo', 'npm', 'init', 'playwright', '--', '--quiet', '--install-deps', '--gha', '--browser', 'chromium'])
    # except subprocess.CalledProcessError as e:
    #     print("Failed to install playwright dependencies:")
    #     print(e.output)
    #     raise

    # # Install browser-use package
    # try:
    #     run_with_output(['pip', 'install', 'browser-use'])
    # except subprocess.CalledProcessError as e:
    #     print("Failed to install browser-use:")
    #     print(e.output)
    #     raise

    # Set required environment variables
    os.environ["ANONYMIZED_TELEMETRY"] = "false"
    os.environ["BROWSER_USE_LOGGING_LEVEL"] = "debug"


def advanced_browser(self, task, api_key, api_base):

    if not self.installed_dependencies:
        install_dependencies()
        self.installed_dependencies = True

    from browser_use.browser.browser import Browser, BrowserConfig
    from browser_use import Agent, Controller
    from langchain_openai import ChatOpenAI

    print("Task:", task, flush=True)

    async def main():
        browser = Browser(
            config=BrowserConfig(
                headless=True  # Enable headless mode
            )
        )
        
        controller = Controller()
        
        agent = Agent(
            task=task,
            llm=ChatOpenAI(
                model="gpt-4o", 
                api_key=api_key, 
                base_url=api_base
            ),
            controller=controller,
            browser=browser,
            generate_gif=False
        )
        
        await agent.run()

    asyncio.run(main())