# AI-Agent-Capstone

- [FileManagerAutomater README](#FileManagerAutomater-README)
- [TodoAutomater README](#TodoAutomater-README)

# FileManagerAutomater README

FileManagerAutomater is a Python project designed to automate the process of organizing and compressing files. It scans a designated input folder for files, categorizes them based on their type (e.g., PDFs, images), moves them into corresponding subfolders in an output directory, and applies compression using external services (ConvertAPI for PDFs and TinyPNG for images). This project helps you maintain an organized file system while reducing file sizes for easier storage and transfer.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Sample Output](#sample-output)
- [Detailed Workflow](#detailed-workflow)
  - [1. Loading Configurations](#1-loading-configurations)
  - [2. Scanning and Moving Files](#2-scanning-and-moving-files)
  - [3. Compressing Files](#3-compressing-files)
- [Module Descriptions](#module-descriptions)
  - [agents.py](#agentspy)
- [Setup and Installation](#setup-and-installation)
- [Usage Examples](#usage-examples)
- [Summary](#summary)

---

## Project Overview

FileManagerAutomater automates file management tasks by processing files in a specified input directory and organizing them in an output directory. The program performs the following tasks:
- **Scanning:** Recursively searches the input folder for files.
- **Categorization:** Identifies file types based on file extensions (e.g., PDFs, images).
- **Organization:** Moves files into subdirectories within the output folder based on their category.
- **Compression:** Uses ConvertAPI to compress PDF files and TinyPNG to compress image files.

By automating these processes, the project minimizes manual file handling and helps optimize file storage space.

---

## Project Structure

Below is the directory structure for FileManagerAutomater:

- **README.md:** This document provides an overview and instructions for the project.
- **agents.py:** The main Python script that implements file scanning, categorization, moving, and compression.
- **agentic_config.yml:** YAML configuration file containing the paths for the input and output folders.
- **file_manager_config.yml:** YAML configuration file that specifies the compression methods for different file types.
- **data/**: Contains two subdirectories:
  - **input_folder:** Where the original files are stored.
  - **output_folder:** Where files are moved and organized.
- **requirements.txt:** Lists the required Python packages needed to run the project.

---

## Sample Output

When you run the script, the output in the terminal will be similar to:

```
Original size of data/input_folder/imagesample1.png: 1.16MB
Moved data/input_folder/imagesample1.png to data/output_folder/Images/imagesample1.png
Size after moving to output folder: 1.16MB
Decision: Category is 'Images'. Selected function: compress_image
Image compression successful for data/output_folder/Images/imagesample1.png
Size after Image compression: 291.13KB

Original size of data/input_folder/pdfsample1.pdf: 18.37KB
Moved data/input_folder/pdfsample1.pdf to data/output_folder/PDFs/pdfsample1.pdf
Size after moving to output folder: 18.37KB
Decision: Category is 'PDFs'. Selected function: compress_pdf
PDF compression successful for data/output_folder/PDFs/pdfsample1.pdf
Size after PDF compression: 18.37KB

All files processed. Agent work completed.
```

This output provides detailed feedback for each step: the original file size, confirmation of file movement, the decision process for selecting the compression function, and the result after compression.

---

## Detailed Workflow

### 1. Loading Configurations

At startup, the program loads configuration files using the `load_config` function. There are two configuration files:

- **agentic_config.yml:**  
  This file contains paths for the input and output folders. For example:
  ```yaml
  input_folder_path: "data/input_folder"
  output_folder_path: "data/output_folder"
  ```
  The script reads these values to know where to find the files and where to place them after processing.

- **file_manager_config.yml:**  
  This file defines the compression methods for various file types:
  ```yaml
  compression_method:
    - PDF: "convertapi"
    - JPG: "tinypng"
    - PNG: "tinypng"
  ```
  These settings tell the program which external API to use for compressing PDFs and images.

By loading these configurations at the beginning, the project ensures that all file paths and compression methods are easily adjustable without changing the code.

### 2. Scanning and Moving Files

The program then scans the specified input folder recursively to locate all files. This is achieved with the `scan_folder` function. Here’s what happens:

- **Scanning:**  
  The function walks through every subdirectory of the input folder and collects file paths. This means it can handle nested directories, ensuring no file is overlooked.

- **Categorization:**  
  For each file, the `get_file_category` function checks its file extension:
  - `.pdf` files are labeled as **PDFs**.
  - Image files (e.g., `.png`, `.jpg`, `.jpeg`) are labeled as **Images**.
  - Other file types fall into the **Others** category.

- **Moving Files:**  
  Once the file category is determined, the `move_file_to_category` function moves the file into a corresponding subfolder within the output directory. For example, an image file is moved to:
  ```
  data/output_folder/Images/
  ```
  This function not only moves the file but also prints confirmation messages, such as the original size and the new file location. This feedback helps you verify that files are being correctly organized.

### 3. Compressing Files

After moving each file, the script checks if the file qualifies for compression:

- **Selecting Compression Function:**  
  The function `select_compression_function` determines the right compression function based on the file category:
  - For **PDFs**, it selects `compress_pdf`.
  - For **Images**, it selects `compress_image`.
  - For other categories, no compression is applied.

- **Compression Process:**  
  - **PDF Compression:**  
    The `compress_pdf` function sends the PDF file to ConvertAPI using an HTTP POST request. It includes the file, a secret API key, and additional parameters. Upon a successful response, it prints a success message.
  - **Image Compression:**  
    The `compress_image` function uses the TinyPNG API via the `tinify` Python package. It uploads the image, compresses it, and saves the result back to the same location. If successful, it prints a message confirming the compression.

Throughout the compression phase, the program prints the file sizes before and after compression. This detailed output lets you see the efficiency of the compression process.

---

## Module Descriptions

### agents.py

- **Purpose:**  
  The `agents.py` script is the central module that coordinates the file management workflow. It integrates configuration loading, file scanning, file movement, and file compression into one seamless process.

- **Key Functions:**
  - `load_config(config_path)`: Reads YAML configuration files to fetch input/output paths and compression methods.
  - `scan_folder(folder_path)`: Recursively collects all file paths from the input folder.
  - `get_file_category(file_path)`: Determines the category of a file based on its extension (e.g., PDFs, Images).
  - `move_file_to_category(file_path, base_output_folder)`: Moves a file into the appropriate subdirectory within the output folder.
  - `compress_pdf(file_path, method)`: Compresses PDF files using ConvertAPI.
  - `compress_image(file_path, method)`: Compresses image files using TinyPNG.
  - `select_compression_function(category)`: Chooses the appropriate compression function based on the file category.
  - `main()`: The main driver function that orchestrates the entire process—loading configurations, scanning files, moving them, and compressing as necessary.

This modular design ensures that each task is handled by a dedicated function, making the code easier to maintain and update.

---

## Setup and Installation

1. **Clone or Download the Repository:**  
   Make sure you have the complete project structure, including configuration files and the `data` folder.

2. **Create a Virtual Environment:**  
   It is recommended to use a virtual environment to manage dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Required Packages:**  
   Install the required packages using the provided `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration Files:**  
   Ensure that `agentic_config.yml` and `file_manager_config.yml` are correctly set up with your desired paths and compression methods.

5. **API Keys and Dependencies:**  
   - For PDF compression, ensure you have a valid ConvertAPI secret key.
   - For image compression, install the `tinify` package and use your TinyPNG key.

---

## Usage Examples

### Example 1: Processing Image Files

Assume you have the following image files in your input folder:
- `imagesample1.png`
- `imagesample2.png`
- `imagesample3.png`

When you run the script with:
```bash
python3 agents.py
```
The program will:
- Scan the input folder and list these image files.
- Determine that these files belong to the **Images** category.
- Move each file into `data/output_folder/Images`.
- Select the TinyPNG compression function to compress each image.
- Print the original and compressed file sizes, along with success messages.

### Example 2: Processing PDF Files

If your input folder contains:
- `pdfsample1.pdf`
- `pdfsample2.pdf`

The script will:
- Recognize these files as **PDFs**.
- Move them to `data/output_folder/PDFs`.
- Use the ConvertAPI service to compress the PDF files.
- Display messages that show the file sizes before and after compression, ensuring that your PDFs are optimized.

---

## Summary

FileManagerAutomater is a comprehensive tool for automating file organization and compression. By leveraging configuration files and external APIs, it eliminates the need for manual file management tasks. The project’s modular structure—with functions dedicated to scanning, moving, and compressing files—ensures that each component is easy to understand, maintain, and modify.

With detailed output at every step, you receive immediate feedback on file movements and compression efficiency. This allows you to verify that the system works correctly and to quickly identify any issues. Whether you need to manage a few files or handle large volumes of data, FileManagerAutomater streamlines the process and optimizes storage with minimal manual intervention.

Enjoy using FileManagerAutomater to keep your files organized and efficient!


# TodoAutomater README

TodoAutomater is a Python project designed to automate daily tasks based on natural language instructions. It reads tasks from a plain text file (`todo.txt`), sends those instructions to Google’s Gemini language model (LLM) to convert them into a structured JSON format, and then uses that JSON to perform actions such as sending email reminders, fetching stock prices via yfinance, and creating calendar events on Google Calendar.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Sample Output](#sample-output)
- [Detailed Workflow](#detailed-workflow)
  - [1. Reading User Tasks](#1-reading-user-tasks)
  - [2. Parsing Tasks with Gemini](#2-parsing-tasks-with-gemini)
  - [3. Scheduling and Executing Tasks](#3-scheduling-and-executing-tasks)
- [Module Descriptions](#module-descriptions)
  - [gemini_parser.py](#gemini_parserpy)
  - [email_sender.py](#email_senderpy)
  - [stock_fetcher.py](#stock_fetcherpy)
  - [calendar_invite.py](#calendar_invitepy)
- [Setup and Installation](#setup-and-installation)
- [Usage Examples](#usage-examples)
- [Summary](#summary)

---

## Project Overview

The primary goal of TodoAutomater is to enable you to automate routine tasks using plain language instructions. For instance, you might have tasks like:

- "Remind me to submit my assignment at 19:20"
- "Send me the price of NVDA stock via email at 19:20"
- "Add an invite for a lecture on 2025-03-07 at 18:05"

Instead of manually coding each reminder or event, you write these instructions in `todo.txt`. The project uses Google’s Gemini LLM to transform these instructions into a structured JSON format that the code can easily process. Once parsed, each task is scheduled to run at the specified time using Python’s threading capabilities.

---

## Project Structure

Here is the directory structure of the project:


- **credentials/**: Contains your Google Calendar OAuth JSON file. This file is required for authenticating with the Google Calendar API.
- **main.py**: The main driver script. It reads tasks from `todo.txt`, uses the Gemini parser to convert them into JSON, schedules the tasks, and keeps the program running.
- **modules/**: Contains all the supporting modules:
  - **gemini_parser.py**: Sends your natural language tasks to Gemini, cleans up its output, and converts it into structured JSON.
  - **email_sender.py**: Sends emails using Gmail’s SMTP server.
  - **stock_fetcher.py**: Fetches current stock prices using the yfinance library.
  - **calendar_invite.py**: Creates calendar events in Google Calendar using the Calendar API.
- **todo.txt**: A text file where you write your tasks in plain English.
- **token.pickle**: A file generated after the first successful OAuth authentication with Google Calendar; it stores your credentials for subsequent API calls.

---
## Sample Output
<img width="903" alt="Screenshot 2025-03-03 at 20 23 19" src="https://github.com/user-attachments/assets/7c3baccc-5571-47f8-aeba-ec8bb8be799c" />
---

## Detailed Workflow

### 1. Reading User Tasks

When you run the project, the first step is to read the tasks you’ve written in `todo.txt`. This file should contain one or more lines of plain language instructions. For example, your file might look like:

```
Remind me to do submit the assignmnet for session30 (final capstone) at 19:20 Send me the price of NVDA stock via email at 19:20 Add an invite for a lecture on 2025-03-07 at 18:05
``` 


The **main.py** script opens this file and reads its content into a single string. This string is then passed to the Gemini parser module.

### 2. Parsing Tasks with Gemini

In the `modules/gemini_parser.py` file, the function `parse_tasks(task_text)` takes the raw text from `todo.txt` and builds a detailed prompt. The prompt instructs Gemini to:
- Recognize different types of tasks (email reminders, stock price checks, calendar invites).
- Output a well-formed JSON array containing one object per task.
- Include all relevant fields such as `task_type`, `email`, `subject`, `message`, `time`, and for calendar invites, an `event` object with `summary`, `start`, and `end`.

**Example prompt snippet:**

> "Output a JSON array of task objects. Each object has 'task_type', 'time', and additional fields depending on the task type. For example:
> 
> ```json
> [
>   {
>     "task_type": "email_reminder",
>     "email": "someone@gmail.com",
>     "subject": "Reminder",
>     "message": "Remind me to do X",
>     "time": "17:00"
>   }
> ]
> ```
> 
> Now parse these instructions into JSON: [your task text]"

Gemini then returns a response. Sometimes the response is wrapped in markdown code fences (```json ... ```), so our code uses a helper function `clean_llm_output()` to remove these fences. After cleaning, the code uses `json.loads()` to convert the response into a Python list of dictionaries (structured JSON).

### 3. Scheduling and Executing Tasks

After parsing, **main.py** iterates over each task in the JSON array and schedules it using Python’s `threading.Timer`. For each task:
- The specified time is parsed.
  - If the time is in `HH:MM` format, it is assumed to be for the current day.
  - If the time is in ISO format (e.g., `2025-03-07T18:05:00`), it is parsed as such.
- If the scheduled time has already passed, the task executes immediately.
- For calendar invites, the task is scheduled to run immediately (delay set to 0) regardless of the provided time.

When the timer triggers, the `dispatch_task()` function is called. This function inspects the `task_type` and calls the appropriate module:
- **Email Reminders:**  
  The `email_sender.send_email()` function is invoked to send an email with the reminder message.
- **Stock Price Tasks:**  
  The `stock_fetcher.get_stock_price()` function retrieves the current price for the stock (e.g., NVDA) using yfinance, and then the email sender sends this information via email.
- **Calendar Invites:**  
  Before calling the calendar function, the code checks if the `event` details are provided as simple strings. If so, it wraps them into the proper format with keys `"dateTime"` and `"timeZone"`. Then, the `calendar_invite.create_calendar_invite()` function is called to create an event in Google Calendar.

The application then enters an infinite loop (with a sleep interval) so that it remains active until you manually stop it.

---

## Module Descriptions

### gemini_parser.py

- **Purpose:**  
  Converts natural language tasks from `todo.txt` into a structured JSON array.
- **Key Functions:**
  - `call_gemini(prompt)`: Sends the detailed prompt to the Gemini model using the google-genai API and returns the raw text.
  - `clean_llm_output(llm_output)`: Strips markdown code fences from the Gemini response if present.
  - `parse_tasks(task_text)`: Builds the complete prompt (including examples), calls Gemini, cleans the response, and parses it into JSON.
  - `pretty_print_tasks(tasks)`: Prints the parsed JSON in a formatted style for debugging and verification.

### email_sender.py

- **Purpose:**  
  Handles sending emails via Gmail's SMTP server.
- **Key Function:**
  - `send_email(sender, password, recipient, subject, message)`: Connects to Gmail’s SMTP server using the provided credentials and sends an email with the specified subject and message.

### stock_fetcher.py

- **Purpose:**  
  Fetches real-time stock prices.
- **Key Function:**
  - `get_stock_price(ticker)`: Uses the yfinance library to get the regular market price for a given stock ticker (e.g., NVDA).

### calendar_invite.py

- **Purpose:**  
  Creates events in Google Calendar.
- **Key Functions:**
  - `get_credentials()`: Handles the OAuth authentication with Google Calendar. If valid credentials do not exist, it opens a browser window to allow you to sign in and generates a `token.pickle` file for future use.
  - `create_calendar_invite(event_details)`: Inserts an event into your primary calendar using the Google Calendar API. It expects the event details to be formatted correctly with start and end times.

---

## Setup and Installation

1. **Clone or Download the Repository:**
   - Ensure you have the entire project structure, including `credentials`, `modules`, `main.py`, `todo.txt`, and `token.pickle`.

2. **Set Up a Virtual Environment:**
   - Create a virtual environment (if not already created):
     ```bash
     python3 -m venv .venv
     ```
   - Activate the virtual environment:
     ```bash
     source .venv/bin/activate
     ```

3. **Install Required Packages:**
   - Install all dependencies (you might need to create a `requirements.txt` if not provided, including packages such as `yfinance`, `google-genai`, and others):
     ```bash
     pip install 
     yfinance 
     google-genai g
     oogle-api-python-client 
     google-auth 
     google-auth-oauthlib
     ```

4. **Set Up Google Credentials:**
   - Place your OAuth JSON file in the `credentials/` folder.
   - On first run, the application will prompt you to authenticate with your Google account. This creates a `token.pickle` file which stores your access credentials.

5. **Run the Application:**
   - Edit your `todo.txt` with your tasks.
   - Start the application:
     ```bash
     python3 main.py
     ```

---

## Usage Examples

### Example 1: Email Reminder
In your `todo.txt`, include:
```
Remind me to submit my assignment at 19:20
```

- **Gemini Parsing:**  
  Gemini converts this line into:
  ```json
  {
    "task_type": "email_reminder",
    "email": "rishitladdha02nov@gmail.com",
    "subject": "Reminder",
    "message": "Remind me to submit my assignment",
    "time": "19:20"
  }
- Execution:
At 19:20, the application sends an email reminder.

### Example 2: Stock Price Alert
In your todo.txt, include:
```
Send me the price of NVDA stock via email at 19:20
```
- Gemini Parsing:
Gemini outputs:
```json
{
  "task_type": "stock_price",
  "stock_symbol": "NVDA",
  "email": "rishitladdha02nov@gmail.com",
  "subject": "NVDA Stock Price",
  "time": "19:20"
}
```
- Execution:
At 19:20, the application uses yfinance to fetch the current price of NVDA and then sends an email with the stock price.

### Example 3: Calendar Invite
In your `todo.txt`, include:
```
Add an invite for a lecture on 2025-03-07 at 18:05
```
- **Gemini Parsing:**  
  Gemini converts this into:
  ```json
  {
    "task_type": "calendar_invite",
    "time": "2025-03-07T18:05:00",
    "event": {
      "summary": "lecture",
      "start": "2025-03-07T18:05:00",
      "end": "2025-03-07T19:05:00"
    }
  }
  ```
- **Execution:**  
  The calendar invite is created immediately. The code wraps the start and end times into the correct format for the Google Calendar API and creates the event on your primary calendar.

---

## Summary

TodoAutomater is an automation tool that bridges the gap between natural language task descriptions and actionable automation. Its key components include:

- **Gemini Integration:**  
  Converts plain text instructions into structured JSON using Google’s Gemini LLM. This allows you to write tasks in simple language without worrying about code syntax.

- **Task Scheduling and Execution:**  
  Each parsed task is scheduled to run at the specified time using Python’s `threading.Timer`. This lets you automate reminders, stock price alerts, and calendar events seamlessly.

- **Modular Design:**  
  The project is split into logical modules:
  - `gemini_parser.py` handles the conversion of natural language to JSON.
  - `email_sender.py` manages email delivery.
  - `stock_fetcher.py` fetches real-time stock data.
  - `calendar_invite.py` integrates with Google Calendar.

- **Easy Setup:**  
  With a virtual environment, proper package installation, and Google OAuth setup, you can quickly get started and customize the tool to your needs.

This project is an excellent example of combining LLM-powered natural language processing with traditional programming to create a practical automation tool. Enjoy automating your daily tasks with TodoAutomater!
