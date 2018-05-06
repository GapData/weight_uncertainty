from weight_uncertainty.util.util import RestoredModel
from weight_uncertainty import conf
from glob import glob
from os.path import join
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from weight_uncertainty.util.util import calc_risk


def read_images():
    for png in glob(join(conf.input_direc, 'input*.png')):
        print(png)
        im = Image.open(png).convert('L')
        yield (np.array(im).astype(np.float32)-33)/78


batch = np.array(list(read_images()))
num_images = batch.shape[0]

model = RestoredModel(conf.restore_direc)

pred = model.sample_prediction(batch, 50)
entropy, mutual_info, sm_var, sm_value, _ = calc_risk(pred)
decision = np.argmax(np.mean(pred, axis=0), axis=-1)


f, axarr = plt.subplots(num_images, 3)

for n, im in enumerate(batch):
    axarr[n, 0].imshow(im, cmap='gray')
    axarr[n, 0].set_title(f'prediction {decision[n]}')
    axarr[n, 1].imshow(np.ones((28, 28)) * entropy[n], cmap='coolwarm', vmin=0.0, vmax=1.6)
    axarr[n, 1].set_title(f'Epistemic uncertainty{entropy[n]:7.2f}')
    axarr[n, 2].imshow(np.ones((28, 28)) * mutual_info[n], cmap='coolwarm', vmin=0.0, vmax=1.6)
    axarr[n, 2].set_title(f'Aleatoric uncertainty{mutual_info[n]:7.3f}')

for axrow in axarr:
    for ax in axrow:
        plt.setp([ax.get_xticklabels()], visible=False)
        plt.setp([ax.get_yticklabels()], visible=False)
# f.subplots_adjust(hspace=0)  # No horizontal space between subplots
f.subplots_adjust(wspace=0)  # No vertical space between subplots

plt.show()
plt.waitforbuttonpress()
