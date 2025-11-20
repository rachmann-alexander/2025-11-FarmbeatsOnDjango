# Farmbeats on Django

## Install on a new system
1. `python3 -m venv myenv && source myenv/bin/activate`
2. `pip install -r requirements.txt`
3. `python manage.py migrate`
4. (Optional) `python manage.py collect_readings --samples 3`

## Start the server
1. `source myenv/bin/activate`
2. `python manage.py runserver`
3. use http://127.0.0.1:8000/ in your browser

Thanks to the FarmBeats for Students project for inspiration and open-source resources [^1].

[^1]: https://github.com/microsoft/farmbeatsforstudents

