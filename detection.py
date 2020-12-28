from anonymization.image_processing import Img
from anonymization import utils
import anonymization


img_dir = '../res/testimg/input'
model_dir = '../res/model/saved_model'
label_path = '../res/model/config/label_map.pbtxt'

TEST_IMAGE_PATHS = utils.save_load.get_image_paths(img_dir)

model = utils.load_model(model_dir)
label = utils.load_label(label_path)

for img_path in TEST_IMAGE_PATHS:
    input_img = Img(img_path)
