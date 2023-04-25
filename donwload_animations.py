
import os
import shutil
import time
import numpy as np
import calapy as cp
cp.initiate(['mixamo', 'txt'])


directory_project = os.getcwd()
directory_mixamo = os.path.join(directory_project, 'mixamo_dataset')

directory_animations = os.path.join(directory_mixamo, 'animations')
if not (os.path.exists(directory_animations)):
    os.makedirs(directory_animations, exist_ok=True)

directory_tmp = os.path.join(directory_project, 'tmp')
if not (os.path.exists(directory_tmp)):
    os.makedirs(directory_tmp, exist_ok=True)

driver_name = 'chromedriver.exe'
driver_path = os.path.join(directory_project, driver_name)

animations_csv_name = 'animations.csv'
animations_csv_path = os.path.join(directory_project, animations_csv_name)

actor_csv_name = 'actors.csv'
actor_csv_path = os.path.join(directory_project, actor_csv_name)

n_mirrors = 2
n_rhos = 1


i_column_i_classes = 1
i_column_names_classes = 2
i_column_names_animations = 5
i_column_names_saved_animations = 31

i_column_websites_animations = 8
i_column_n_search_results = 9
i_column_i_search_result = 10

i_column_n_frames_default = 11

i_column_trims = slice(12, 14, 1)

i_column_adjust_trim = slice(16, 18, 1)

i_column_trim_range = slice(18, 20, 1)

i_column_n_mixamo_variables = 20
i_column_mixamo_variables = slice(21, 31, 1)
n_max_mixamo_variables = 5

#i_column_mixamo_variables = 25
columns = [
    i_column_i_classes, i_column_names_classes, i_column_names_animations, i_column_names_saved_animations,
    i_column_websites_animations, i_column_n_search_results, i_column_i_search_result, i_column_n_frames_default,
    i_column_trims, i_column_adjust_trim, i_column_trim_range, i_column_n_mixamo_variables,
    i_column_mixamo_variables
]

rows = slice(1, None, 1)

dtype = [int, str, str, str,
         str, int, int, int,
         int, str, int, int,
         float]

(
    i_classes, names_classes, names_animations, names_saved_animations,
    websites_animations, n_search_results_from_csv, i_search_result, n_frames_default,
    trims, adjust_trim, trim_range, n_mixamo_variables_from_csv,
    mixamo_variables
) = cp.txt.csv_file_to_arrays(animations_csv_path, rows, columns, delimiter=',', dtype=dtype)

classes = np.unique(i_classes)
n_classes = len(classes)
n_animations = len(i_classes)

mixamo_variables = np.moveaxis(np.asarray(
    np.split(mixamo_variables, n_max_mixamo_variables, axis=1), dtype=float), 0, 1)

adjust_trim = adjust_trim == 'TRUE'

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

    # for i_animation in range(7, n_animations, 1):
    for i_animation in range(0, n_animations, 1):

        directory_i_class = os.path.join(directory_animations, names_classes[i_animation])

        if not (os.path.exists(directory_i_class)):
            os.mkdir(directory_i_class)

        directory_a_actor = os.path.join(directory_i_class, actor_names[a])

        if not (os.path.exists(directory_a_actor)):
            os.mkdir(directory_a_actor)

        directory_i_animation = os.path.join(directory_a_actor, names_animations[i_animation])
        if not (os.path.exists(directory_i_animation)):
            os.mkdir(directory_i_animation)

        directory_i_fbx = os.path.join(directory_tmp, names_saved_animations[i_animation])

        print(' - '.join([
            str(i_animation) + 'th animation', names_classes[i_animation],
            actor_names[a], names_animations[i_animation]]))

        cp_MixamoBot.activate_animation(
            websites_animations[i_animation], n_search_results_from_csv[i_animation],
            i_search_result[i_animation])

        cp_MixamoBot.check_n_frames_default_from_web(n_frames_default[i_animation])

        time.sleep(0.2)
        elements_trim = cp_MixamoBot.driver.find_elements('name', 'trim')

        elements_variables_mixamo = cp_MixamoBot.driver.find_elements(
            'css selector', 'input.input-text-unstyled.animation-slider-value.input-text-editable')[::-1]

        n_variables_mixamo_from_web = len(elements_variables_mixamo)
        if n_variables_mixamo_from_web == n_mixamo_variables_from_csv[i_animation]:

            n_variables_mixamo = n_variables_mixamo_from_web
            samples_variables_mixamo = np.empty([n_mirrors, n_rhos, n_variables_mixamo], dtype=int)

            for i_variable_mixamo in range(n_variables_mixamo):
                # print(mixamo_variables[i_animation, i_variable_mixamo])
                samples_variables_mixamo[:, :, i_variable_mixamo] = (
                    np.random.randint(
                        mixamo_variables[i_animation, i_variable_mixamo, 0],
                        mixamo_variables[i_animation, i_variable_mixamo, 1] + 1,
                        size=[n_mirrors, n_rhos]))

            for i_mirror in range(0, n_mirrors, 1):

                directory_i_mirror = os.path.join(directory_i_animation, 'mirror_{:02d}'.format(i_mirror))

                if not (os.path.exists(directory_i_mirror)):
                    os.mkdir(directory_i_mirror)

                for i_rho in range(0, n_rhos, 1):

                    directory_i_rho = os.path.join(directory_i_mirror, 'rho_{:02d}.fbx'.format(i_rho))

                    if os.path.exists(directory_i_rho):
                        os.remove(directory_i_rho)
                        print("{} deleted".format(directory_i_rho))

                    cp_MixamoBot.set_animation_parameters(
                        samples_variables_mixamo[i_mirror, i_rho, :],
                        elements_variables_mixamo=elements_variables_mixamo)

                    cp_MixamoBot.set_animation_trim(
                        start=trims[i_animation, 0],
                        end=trims[i_animation, 1],
                        elements_trim=elements_trim)

                    cp_MixamoBot.adjust_trim_to_make_n_frames_equal_or_larger_than_threshold(
                        trims[i_animation], trim_range[i_animation],
                        adjust_trim=adjust_trim[i_animation],
                        elements_trim=elements_trim, threshold=60)

                    cp_MixamoBot.download_animation(directory_i_fbx, directory_i_rho)

        else:
            raise ValueError(
                'For the animation {}, the following condition is not met:\n'
                'n_variables_mixamo_from_web == n_mixamo_variables_from_csv[i_animation]\n'
                'n_variables_mixamo_from_web = {}\n'
                'n_mixamo_variables_from_csv[i_animation] = {}\n'.format(
                    i_animation, n_variables_mixamo_from_web, n_mixamo_variables_from_csv[i_animation]))


# print('The time spent was {}'.format(timer.getTime()))
cp_MixamoBot.driver.quit()
shutil.rmtree(directory_tmp)
print('FINISHED')
