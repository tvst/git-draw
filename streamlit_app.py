import datetime
import numpy as np
import os
import shutil
import tempfile

import streamlit as st

import hilevel_util
from gridcanvas import gridcanvas


@st.cache_resource
def get_readme_contents():
    with open('template.md', 'rb') as f:
        return f.read()


"""
# :see_no_evil: Git draw

Draw your own Github contribution chart!

It's a great way to send messages to lurkers and recruiters :wink:
"""

''
''

"""
## :pencil: Step 1: Draw something

Drag your mouse over the grid below to draw your own Git history.
The right-most column is the current week.
"""

num_weeks = st.slider("Number of weeks in grid", 1, 50, 10)
weeks = gridcanvas(num_weeks=num_weeks)
dates = []

now = datetime.datetime.now()
today_utc = datetime.datetime(
    year=now.year, month=now.month, day=now.day, hour=12, tzinfo=datetime.timezone.utc)
curr_weekday = today_utc.weekday()
one_day = datetime.timedelta(days=1)

if curr_weekday < 5: # < Saturday
    last_saturday = today_utc - datetime.timedelta(days=curr_weekday + 2)
elif curr_weekday == 6: # Sunday
    last_saturday = today_utc - one_day
else: # == Saturday
    last_saturday = today_utc

@st.cache_data
def get_dates(weeks):
    dates = []
    if not weeks:
        return dates

    w = len(weeks)
    curr_day = last_saturday

    # Iterate backward from the last Saturday.
    for w, week in enumerate(reversed(weeks)):
        for d, day_value in enumerate(reversed(week)):
            if day_value:
                dates.append(curr_day)

            curr_day -= one_day

    return list(reversed(dates))

dates = get_dates(weeks)

''
''

"""
## :robot_face: Step 2: Generate repo

Type the email associated with your Github account, so we can generate a repo
full of commits with that email set as the author.
"""

if 'repo_zip' not in st.session_state:
    st.session_state.repo_zip = None

temp_dir = None
repo_zip_path = None

if dates:
    email = None
    name = None
    generate_clicked = False

    email = st.text_input('Email of commit author')
    name = st.text_input('Human-readable name for commit author')

    if st.button('Generate'):
        temp_dir = tempfile.TemporaryDirectory()
        temp_dir_path = temp_dir.name

        repo_dir_name = 'git-drawing'
        repo_dir_path = os.path.join(temp_dir_path, repo_dir_name)
        os.mkdir(repo_dir_path)

        hilevel_util.draw_git_history(
            repo_dir=repo_dir_path,
            email=email,
            name=name,
            dates=dates,
            readme_contents=get_readme_contents(),
        )

        repo_zip_path = os.path.join(temp_dir_path, 'git-drawing')
        shutil.make_archive(repo_zip_path, 'zip', temp_dir_path, repo_dir_name)

        with open(f'{repo_zip_path}.zip', 'rb') as zip_file:
            st.session_state.repo_zip = zip_file.read()

        temp_dir.cleanup()

else:
    st.warning('Please do step 1 first!')

''
''

"""
## :arrow_down: Step 3: Download repo

Download a zip file with the generated Git repo.
"""

if st.session_state.repo_zip is None:
    st.warning('Please finish steps 1 and 2 first.')
    st.button('Download zip here', disabled=True)

else:
    st.download_button(
        'Download zip here',
        data=st.session_state.repo_zip,
        file_name='git-drawing.zip',
    )

''
''

"""
## :eight_spoked_asterisk: Step 4: Unpack repo and push to Github

1. **Create a new empty repo in Github.**

   For the lazy, [just click here](https://github.com/new)
   then give the repo a name like `git-drawing`.

1. **Unzip the downloaded file.**

   Once you're done, you'll see a new folder called `git-drawing`.

1. **Push to Github.**

   Set your repo from step 1 as your remote Git server and push to it.

   Below are the commmands to do this, assuming you named your repo `git-drawing`.

   (Replace `YOUR_NAME` with your Github username, of course :wink:)

   ```
   cd git-drawing
   git remote add origin https://github.com/YOUR_NAME/git-drawing.git
   git push -u origin main
   ```

1. **PROFIT!!! :money_mouth_face:**
"""
