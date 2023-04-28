

import os
import shutil
import calapy as cp
cp.initiate(['mixamo', 'txt'])


directory_project = os.getcwd()
directory_mixamo = os.path.join(directory_project, 'mixamo_dataset')

directory_actors = os.path.join(directory_mixamo, 'actors')
if not (os.path.exists(directory_actors)):
    os.mkdir(directory_actors)

directory_tmp = os.path.join(directory_project, 'tmp')
if not (os.path.exists(directory_tmp)):
    os.makedirs(directory_tmp, exist_ok=True)

driver_name = 'chromedriver.exe'
driver_path = os.path.join(directory_project, driver_name)

actor_csv_name = 'actors.csv'
actor_csv_path = os.path.join(directory_project, actor_csv_name)

i_column_actor_names = 1
i_column_mixamo_actor_names = 2
i_column_search_actor_as = 3
i_column_websites_search_actors = 4

columns = [i_column_actor_names, i_column_mixamo_actor_names,
           i_column_search_actor_as, i_column_websites_search_actors]

rows = slice(1, None, 1)

dtype = [str, str, str, str]

actor_names, mixamo_actor_names, search_actor_as, websites_search_actors = cp.txt.csv_file_to_arrays(
    actor_csv_path, rows, columns, delimiter=',', dtype=dtype)

n_actors = len(actor_names)


# adobe_username = None
adobe_username = 'cc18849@essex.ac.uk'
adobe_password = 'Carmel000'

# adobe_username = 'melocalafuria@gmail.com'
# adobe_password = 'sdfsdjbGVHJV3782'

# adobe_username = 'calafioremelo@gmail.com'
# adobe_password = 'D8J3d4HLj9mP1k4Fo2E4Hk'

cp_MixamoBot = cp.mixamo.MixamoBot(
    directory_driver=driver_path, directory_downloads=directory_tmp, username=adobe_username, timeout=600)

login = True
# login = False
if login:
    cp_MixamoBot.login(password=adobe_password)
else:
    first_name = 'Carmelo'
    last_name = 'Calafiore'
    birthday = dict(day='8', month='8', year='1989')

    # adobe_password = first_name = last_name = birthday = None
    # first_name = last_name = birthday = None

    cp_MixamoBot.signup(password=adobe_password, first_name=first_name, last_name=last_name, birthday=birthday)

# for a in [1]:
for a in range(0, n_actors, 1):

    cp_MixamoBot.activate_character(mixamo_actor_names[a], websites_search_actors[a])

    directory_a = os.path.join(directory_actors, actor_names[a] + '.fbx')

    cp_MixamoBot.download_t_pose(directory_a)


# print('The time spent was {}'.format(timer.getTime()))
cp_MixamoBot.driver.quit()
shutil.rmtree(directory_tmp)
print('FINISHED')
