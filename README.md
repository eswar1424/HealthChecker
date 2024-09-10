# HealthChecker 

## Description
This is a Script to check the Health of the services running on the linux servers.


### Requirements
- Python 3.x


### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/eswar1424/HealthChecker.git
   ```

2. Go into the project:
    ```bash
   cd HealthChecker
   ```
   
   
3. Activate the python virtual Environment
    
    - For **Windows**
    ```bash
    HealthCheckerEnv\Scripts\Activate 
    ```
    
    - For **Linux**
    ```bash
    source HealthCheckerEnv/Scripts/activate
    ```

4. Install all the dependencies required for the project
    - For **Windows**
    ```bash
    pip install -r requirement.txt
    ```
    
    - For **Linux**
    ```bash
    pip3 install -r requirement.txt
    ```

5. Configure the Script according to your requirement.
    - Configure server details for which you want to do Health check.
        - create a file named **servers.csv** in root directory of the project (see servers_dummy.csv for reference)
        
    - Configure GMail id's and password's to send Healthcheck reports.
        - create a file named **.env** in root directory of the project (see .env_dummy for reference)
        

6. Run the HealthChecker script (you should be in the root directory of the project)
    - For **Windows**
    ```bash
    python health_checker.py
    ```
    
    - For **Linux**
    ```bash
    python3 health_checker.py
    ```

