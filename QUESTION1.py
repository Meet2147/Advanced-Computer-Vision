# -*- coding: utf-8 -*-
"""Q1. TRANSFER LEARNING

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VZu7b-OGYDbhNY7Al7luAS1rAo5wgrfX
"""

!wget --passive-ftp --prefer-family=ipv4 --ftp-user FoodImage@grebvm2.epfl.ch --ftp-password Cahc1moo ftp://tremplin.epfl.ch/Food-5K.zip

!mkdir Food-5k

!unzip Food-5K.zip -d Food-5K

!pip install imutils

from imutils import paths
import shutil
import os

ORIG_INPUT_DATASET = "/content/Food-5K"

BASE_PATH = "dataset"

# define the names of the training, testing, and validation
# directories
TRAIN = "training"
TEST = "evaluation"
VAL = "validation"

# initialize the list of class label names
CLASSES = ["non_food", "food"]

# loop over the data splits
for split in (TRAIN, TEST, VAL):
  # grab all image paths in the current split
  print("[INFO] processing "+split+"...")
  p = os.path.sep.join([ORIG_INPUT_DATASET, split])
  imagePaths = list(paths.list_images(p))
  print(imagePaths)
 
  # loop over the image paths
  for imagePath in imagePaths:
    # extract class label from the filename
    filename = imagePath.split(os.path.sep)[-1]
    label = CLASSES[int(filename.split("_")[0])]
 
    # construct the path to the output directory
    dirPath = os.path.sep.join([BASE_PATH, split, label])
    print(dirPath)
 
    # if the output directory does not exist, create it
    if not os.path.exists(dirPath):
      os.makedirs(dirPath)
 
    # construct the path to the output image file and copy it
    p = os.path.sep.join([dirPath, filename])
    shutil.copy2(imagePath, p)

import os
import shutil
import cv2
from tqdm import tqdm, tqdm_notebook
import numpy as np
import matplotlib.pyplot as plt
import warnings

import tensorflow as tf
import keras
from keras.preprocessing.image import load_img, img_to_array
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import GlobalAveragePooling2D
from keras.layers import Dropout
from keras.layers import BatchNormalization
from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.applications.xception import Xception, preprocess_input
from keras.applications.inception_v3 import InceptionV3
from keras.applications.densenet import DenseNet201
from keras.applications.mobilenet_v2 import MobileNetV2
from keras.applications.vgg19 import VGG19
from keras.models import Model
from keras.models import load_model
from keras.optimizers import *

warnings.filterwarnings("ignore")

"""**PYTORCH**"""

from __future__ import print_function, division

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
import copy

# Just normalization for validation
data_transforms = {
    'training': transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'validation': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

data_dir = '/content/dataset'
os.listdir(data_dir)

data_dir = '/content/dataset'
image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x),
                                          data_transforms[x])
                  for x in ['training', 'validation']}
dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=4,
                                             shuffle=True, num_workers=4)
              for x in ['training', 'validation']}
dataset_sizes = {x: len(image_datasets[x]) for x in ['training', 'validation']}
class_names = image_datasets['training'].classes

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def imshow(inp, title=None):
    """Imshow for Tensor."""
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)
    plt.imshow(inp)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)  # pause a bit so that plots are updated

"""**VISUALIZE THE DATA**"""

# Get a batch of training data
inputs, classes = next(iter(dataloaders['training']))

# Make a grid from batch
out = torchvision.utils.make_grid(inputs)

imshow(out, title=[class_names[x] for x in classes])

"""**DEFINE A FUNCTION TO TRAIN THE MODEL**"""

def train_model(model, criterion, optimizer, scheduler, num_epochs=25):
    since = time.time()

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['training', 'validation']:
            if phase == 'training':
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data.
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'training'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    # backward + optimize only if in training phase
                    if phase == 'training':
                        loss.backward()
                        optimizer.step()

                # statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)
            if phase == 'training':
                scheduler.step()

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                phase, epoch_loss, epoch_acc))

            # deep copy the model
            if phase == 'validation' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())

        print()

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))
    print('Best val Acc: {:4f}'.format(best_acc))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model

"""**DEFINE A FUNCTION TO VISULAIZE THE PREDICTIONS**"""

def visualize_model(model, num_images=6):
    was_training = model.training
    model.eval()
    images_so_far = 0
    fig = plt.figure()

    with torch.no_grad():
        for i, (inputs, labels) in enumerate(dataloaders['validation']):
            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)

            for j in range(inputs.size()[0]):
                images_so_far += 1
                ax = plt.subplot(num_images//2, 2, images_so_far)
                ax.axis('off')
                ax.set_title('predicted: {}'.format(class_names[preds[j]]))
                imshow(inputs.cpu().data[j])

                if images_so_far == num_images:
                    model.train(mode=was_training)
                    return
        model.train(mode=was_training)

"""**Q 1) 1. IMPORTING EXISTING MODELS AND BULDING NEW FC LAYERS**

**RESNET 18**
"""

model_ft = models.resnet18(pretrained=True)
num_ftrs = model_ft.fc.in_features
# Here the size of each output sample is set to 2.
# Alternatively, it can be generalized to nn.Linear(num_ftrs, len(class_names)).
model_ft.fc = nn.Linear(num_ftrs, 2)

model_ft = model_ft.to(device)

criterion = nn.CrossEntropyLoss()

# Observe that all parameters are being optimized
optimizer_ft = optim.SGD(model_ft.parameters(), lr=0.001, momentum=0.9)

# Decay LR by a factor of 0.1 every 7 epochs
exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)

"""**TRAIN THE MODEL**"""

#start the training of the model by calling the train_model function
model_ft = train_model(model_ft, criterion, optimizer_ft, exp_lr_scheduler,
                       num_epochs=25)

"""**VISULAIZING THE PREDICTIONS**"""

#here once the model has been trained, we will visualize the predictions made by the model
visualize_model(model_ft)

"""**INCEPTION V3**"""

model_ft = models.inception_v3(pretrained=True)
num_ftrs = model_ft.fc.in_features
# Here the size of each output sample is set to 2.
# Alternatively, it can be generalized to nn.Linear(num_ftrs, len(class_names)).
model_ft.fc = nn.Linear(num_ftrs, 2)

model_ft = model_ft.to(device)

criterion = nn.CrossEntropyLoss()

# Observe that all parameters are being optimized
optimizer_ft = optim.SGD(model_ft.parameters(), lr=0.001, momentum=0.9)

# Decay LR by a factor of 0.1 every 7 epochs
exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)

#start the training of the model by calling the train_model function
model_ft = train_model(model_ft, criterion, optimizer_ft, exp_lr_scheduler,
                       num_epochs=25)





"""**Q 1) 2. EXTRACTING THE BOTTLENECK FEATURES AND TRAINING A CLASSIFIER**

**RESNET 50**
"""

model_conv = torchvision.models.resnet50(pretrained=True)
for param in model_conv.parameters():
    param.requires_grad = False

# Parameters of newly constructed modules have requires_grad=True by default
num_ftrs = model_conv.fc.in_features
model_conv.fc = nn.Linear(num_ftrs, 2)

model_conv = model_conv.to(device)

criterion = nn.CrossEntropyLoss()

# Observe that only parameters of final layer are being optimized as
# opposed to before.
optimizer_conv = optim.SGD(model_conv.fc.parameters(), lr=0.001, momentum=0.9)

# Decay LR by a factor of 0.1 every 7 epochs
exp_lr_scheduler = lr_scheduler.StepLR(optimizer_conv, step_size=7, gamma=0.1)

model_conv = train_model(model_conv, criterion, optimizer_conv,
                         exp_lr_scheduler, num_epochs=25)

visualize_model(model_conv)

plt.ioff()
plt.show()

"""**XCEPTION**

Here we will uitlize keras framework to extract the bottleneck features and training few different classifiers. Since the XCEPTION pertrained model is not presnet in the PYTORCH hence the KERAS framework has been utilized

**IMPORT THE LIBRARIES**
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import os, shutil
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import ResNet50

"""**CREATE A DATA GENERATOR**"""

datagen = ImageDataGenerator(rescale=1./255)
img_width = 224
img_height = 224
batch_size = 32

"""**LOAD THE XCEPTION PRETRIANED MODEL**"""

conv_base = Xception(weights='imagenet',
                 include_top=False,
                 input_shape=(img_width, img_height, 3))  # 3 = number of channels in RGB pictures

"""**EXTRACT THE FEATURES FROM THE INPUT DATA**"""

#DEFINE A FUNCTION THAT WOULD HELP US EXTRACT THE FEATURES FROM THE INPUT DATA
def extract_features(directory, sample_count):
   features = np.zeros(shape=(sample_count, 7, 7, 2048))  # Must be equal to the output of the convolutional base
   labels = np.zeros(shape=(sample_count,2))
   # Preprocess data
   generator = datagen.flow_from_directory(directory,
                                           target_size=(img_width,img_height),
                                           batch_size = batch_size,
                                           class_mode='categorical')
   # Pass data through convolutional base
   i = 0
   for inputs_batch, labels_batch in generator:
       features_batch = conv_base.predict(inputs_batch)
       features[i * batch_size: (i + 1) * batch_size] = features_batch
       labels[i * batch_size: (i + 1) * batch_size] = labels_batch
       i += 1
       if i * batch_size >= sample_count:
           break
   return features, labels

train_size = 1088
validation_size = 256

#CALL THE ABOVE extract_features FUNCTION TO EXTRACT THE FEATURES FROM THE TRIANING AND VALIDATION DATA
train_features, train_labels = extract_features('/content/dataset/training', train_size)  # Agree with our small dataset size
validation_features, validation_labels = extract_features('/content/dataset/validation', validation_size)

#CONCATENATE THE EXTRACTED TRAINING AND VALIDATION FEATURES
features = np.concatenate((train_features, validation_features))

#STORE THE LABELS FOR TRAINING DATA
labels_train= []
for i in range(len(train_labels)):
    labels_train.append(np.argmax(train_labels[i])) 


#STORE THE LABELS FOR VALIDATION DATA
labels_valid= []
for i in range(len(validation_labels)):
    labels_valid.append(np.argmax(validation_labels[i]))

#CONCATENATE THE LABELS FOR TRAINING AND VALIDATION
labels = np.concatenate((labels_train, labels_valid))

X_train, y_train = features.reshape(1344,7*7*2048),labels


#SPLIT THE DATA INTO TRAINING AND TESTING
x_train,x_test,y_train,y_test = train_test_split(X_train,y_train,test_size = 0.2,random_state = 42)

#APPLY THE NAIVE BAYES CLASSIFER ON THE EXTRACTED FEATURES
nb = MultinomialNB()

#FIT THE MODEL ON TRAIN AND LABELS
nb.fit(x_train, y_train)

#PREDICT ON THE NEW DATA
pred = nb.predict(x_test)

#PRINT THE ACCURACY SOCRE
print(f'THE ACCURACY OF THE NAIVE BAYES MODEL IS: {accuracy_score(y_test,pred)}')

