powershell -command "& { (New-Object Net.WebClient).DownloadFile('https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe', 'plink.exe') }"
python3 -m venv .\tvent
call tvent\Scripts\activate.bat
pip3 install -r requirements.txt
