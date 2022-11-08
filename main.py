import os

MODEL_FOLDER = 'models'
MODEL_SAVED_NAME = 'resnet_unfreeze_all_filtered.tf'
MODEL_NAME = 'resnet_unfreeze_all_filtered'
MODEL_VERSION = '1'

# Define paths on host and guest system
model_path_host = os.path.join(os.getcwd(), MODEL_FOLDER, MODEL_SAVED_NAME, 'model')
model_path_guest = os.path.join('/models', MODEL_NAME, MODEL_VERSION)

# Container start command
docker_run_cmd = f'docker run ' \
                 f'-p 8501:8501 ' \
                 f'-v {model_path_host}:{model_path_guest} ' \
                 f'-e MODEL_NAME={MODEL_NAME} ' \
                 f'-d ' \
                 f'--name tf_serving ' \
                 f'tensorflow/serving'

# If container is not running, create a new instance and run it
docker_run_cmd_cond = f'if [ ! "$(docker ps -q -f name=tf_serving)" ]; then \n' \
                      f'   if [ "$(docker ps -aq -f status=exited -f name=tf_serving)" ]; then 														\n' \
                      f'   		docker rm tf_serving \n' \
                      f'   fi \n' \
                      f'   {docker_run_cmd} \n' \
                      f'fi'

# Start container
os.system(docker_run_cmd_cond)