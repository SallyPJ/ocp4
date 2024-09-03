# Chess Tournament Manager
This project is a Chess Tournament Manager that allows you to manage players, tournaments, and generate HTML reports for tournaments.  
The program is cross-platform and works on Windows, macOS, and Linux.

## Dependencies
- uuid
- tabulate
- Jinja2

## Prerequisites
Before running this program, ensure you have the following installed on your machine:

Python 3.8 or higher
Python dependencies listed in requirements.txt (see the "Installation" section)

## Installation

### 1. Clone the project
Open Git Bash or your preferred terminal application.  
Navigate to the directory where you want to clone the project using the cd (change directory) command.  
Run the following command to clone the repository:  
 ```bash
git clone https://github.com/SallyPJ/ocp2.git
 ```

### 2. Create and activate a virtual environment in the project folder  
In the project folder, create the virtual environment.  
 ```bash
python -m venv env
 ```
Then activate the project environment.  
Windows(Powershell)  
 ```bash
source env\scripts\activate
 ```
Linux/Mac  
 ```bash
source env/bin/activate
 ```
### 3. Install dependencies
The program relies on several Python libraries which can be installed using pip.   
Navigate to the directory containing the project files in your terminal or command prompt and run the following command:
 ```bash
pip install -r requirements.txt
 ```
### 5. Run the program
 ```bash
python main.py
 ```
## Usage

#### Main Menu:
<img width="400" alt="image" src="https://github.com/user-attachments/assets/434f899d-1061-4de6-852d-b0ae43ffd779">

1. Manage players, create a new player, or view the list of registered players.
2. Create a new tournament, manage existing tournaments, or view finished tournaments.
3. Generate reports on tournaments (in HTML).

#### Player Management:
<img width="400" alt="image" src="https://github.com/user-attachments/assets/e5d8a6b0-ef5f-4943-b698-70179a82b0ad">

1. Create a new player by providing their last name, first name, date of birth, and national chess ID.
2. Display the list of all registered players.

#### Tournament Management:
<img width="400" alt="image" src="https://github.com/user-attachments/assets/2882b737-b214-46c0-abff-f6d6349a7a9f">

1. Create a new tournament by specifying details such as name, location, dates, number of rounds, etc.
2. Start or resume an existing tournament.
3. List and Details of Finished Tournaments: View details of finished tournaments.

### 3 Data Management (Reports):
<img width="400" alt="image" src="https://github.com/user-attachments/assets/77674669-4614-4ad6-9ccb-3ee154536914">  
  
1. Tournament Overview (HTML): Generate an HTML report of all tournaments.
The report will be generated and saved as tournament_report.html in the root directory of the project.  
The HTML file will automatically open in your default web browser.

## Outputs
The application generates the following key outputs:  

#### Tournament HTML Report:
File: tournament_report.html  
Location: Root directory  
Description: A detailed HTML report providing an overview of all tournaments, including player lists, match results, and tournament details.  

#### Player Data File:
File: players.json  
Location: data directory  
Description: A JSON file storing all registered player information, including names, national IDs, and accumulated points.  

#### Tournament Data File:
File: tournaments.json  
Location: data directory  
Description: A JSON file containing tournament details such as name, location, dates, player lists, rounds, and match results.  

#### Console Outputs:
Description: Various messages, menus, and data summaries displayed in the console to guide the user through the application's functionality and provide feedback.  

## Running Flake8 with HTML Report
To generate an HTML report with Flake8:  

1. Ensure that the flake8-html package is installed.  

```bash
pip install flake8-html
```
2. Configure flake8 to exclude certain files/folders.  
  Create a .flake8 file at the root of your project with the following content:  

```bash
[flake8]
exclude =
    .git,
    __pycache__,
    build,
    dist,
    venv,
    .venv,
    env,
    .env
max-line-length = 88
```
  
3. Run Flake8 with the following command.

```bash
flake8 --format=html --htmldir=flake8_report
```
The report will be generated in the flake8_report directory as HTML files.  
Open index.html to view the results.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.
