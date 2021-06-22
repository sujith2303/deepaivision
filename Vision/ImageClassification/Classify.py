import numpy as np
import tensorflow as tf
import tqdm
import os
import matplotlib.pyplot as plt

__author__ = 'Sujith Anumala'

class ImageClassification:
  def __init__(self,ImagePath=None,LabelsPath=None,num_classes=None,names=None,input_shape=(320,320,3)):
    self.ImagePath = ImagePath
    self.LabelsPath= LabelsPath
    self.classes   = classes
    self.images    = []
    self.labels    = []
    self.history   = None
    self.filename  = []
    self.input_shape = input_shape
    self.model       =None
    self.names     = names   #Names of the classes
    if not ImagePath:
      raise FileNotFoundError('Enter a valid path')
    if not LabelsPath:
      raise FileNotFoundError('Enter a valid path')
    if not num_classes:
      raise ValueError('Enter a Non-zero number')
   get_train_data()
   get_labels()
  
  def get_train_data(self):
    self.filename = os.listdir(self.ImagePath)
    print('Loading images..............')
    for file in tqdm(self.filename):
      img = cv2.imread(os.path.join(self.ImagePath,file))
      img = cv2.resize(img,self.input_shape)
      img = np.array(img)
      img/=255
      self.images.append(img)
      
    self.images = np.array(self.images)
    print('Successfully Loaded all the images.....')
  def get_labels(self,datatype='.txt'):
    for i in self.filename:
      label = (open(f'{i}.txt','r')).read()
      label = self.names.findindex(label)
      self.labels.append(label)
    self.labels = np.array(self.labels)
    self.labels = tf.keras.utils.to_categorical(self.labels)
  
  def Train(self,epochs=10,batch_size = 128):
    input_shape=self.input_shape
    
    model =tf.keras.applications.vgg16.VGG16(
    include_top=False, weights='imagenet')
    
    x_input = tf.keras.layers.Input(shape = input_shape)
    x = model(x_input,training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(100,activation='relu')(x_input)
    output=tf.keras.layers.Dense(self.classes,activation='Softmax')(x)
    
    model = tf.keras.Model(x_input,output,name='Classification Model')
    if self.num_classes>2:
      model.compile(loss=tf.keras.losses.CategoricalCrossentropy(),optimizer='adam',metrics=['Accuracy'])
    elif self.num_classes==2:
      model.compile(loss=tf.keras.losses.BinaryCrossentropy(),optimizer='adam',metrics=['Accuracy'])
    else:
      raise ValueError('Enter a value for num_classes greater than or equals to 2')
    
    history = model.fit(x=trainx,y=trainy,epochs,batch_size=batch_size)
    self.model =model
    #return model
  def predict(self,image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img,self.input_shape)
    img = np.expand_dims(img,axis=0)
    print('Detected a',self.names[np.argmax(self.model.predict(img))])
   
  def plot_results(self):
    history = self.history
    print('Plotting accuracy.................')
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    print('Plotting loss.................')
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
  def summary(self):
    print('Showing the summary of your model')
    self.model.summary()
  def save_model(self,path):
    print(f'Saving your model at {path} Location')
    path = str(path) + '/' + 'model.h5'
    self.model.save(path)
  def save_weights(self,path,save_format='.h5'):
    print(f'Saving weights at {path} location') 
    if save_format == '.h5':
      path=str(path) + '/' +'weights.h5'
      self.model.save_weights(path)
    elif save_format == '.weights':
      path =str(path) + '/' + 'weights.weights'
      self.model.save_weights(path)
    else:
      path =str(path) + '/' + 'weights' + str(save_format)
      self.model.save_weights(path)
    print(f'Successfully saved your weights at {path} location')
      
    

