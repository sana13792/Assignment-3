# An image Classification piepline using CNN
**Problem Statement**- Implement an image classification pipeline using CNN to classify the natural scenes images into different classes <br/>
**Dataset used**-([https://www.kaggle.com/puneet6060/intel-image-classification/version/2])<br/>
**Dataset details**This is the Data of Natural Scenes around the world.This Data contains around 25k images of size 150x150 distributed under 6 categories i.e. Buildings, Forest, Glacier , Mountain, Sea and Street.<br/>
## Solution-1 (Without Transfer Learning and Data Augmentation)
A simple custom CNN was built with the following details <br/>
![](https://github.com/sana13792/Assignment-3/blob/main/Images/CnnModel.png) <br/>
**Results**-The following network produced the training accuracy of 81% after 30 epochs and test accuracy was 80% which isn't much satisfactory. The results are depicted in the image given below<br/>
![](https://github.com/sana13792/Assignment-3/blob/main/Images/result1.png)<br/>
## Solution 2 (With Transfer Learning and Data Augmentation)
**Data Augmentation**As the test accuracy wasn’t much satisfactory hence to improve the test accuracy, data augmentation and transfer learning were applied. Data is randomly flipped and rotated in order to increase the training data for getting effective results. <br/>
![](https://github.com/sana13792/Assignment-3/blob/main/Images/image_2021-01-28_032338.png) <br/>
**Transfer Learning**For transfer learning, here we take a pre train model and then we try to retrain it for the our problem. For this problem, we have used a mobilenet pre trained model from Google's tensorflow and we have used that pretrained model to classify our Natural scene data set. Google's trained mobilenet V2 model  is a deep learning model  trained on 1.4 million images and in total thousand classes. <br/>
![](https://github.com/sana13792/Assignment-3/blob/main/Images/image_2021-01-28_033459.png) <br/>
**Results** Previously it took many epochs to train the complete model and achieve high accuracy but in this case using a pre trained model and data augmentation, it took only like 10 iterations or epochs to get a test accuracy of 90%. The accuracy and loss plots are given below.<br/>
![](https://github.com/sana13792/Assignment-3/blob/main/Images/image_2021-01-28_034147.png) <br/>
![](https://github.com/sana13792/Assignment-3/blob/main/Images/image_2021-01-28_034109.png) <br/>
![](https://github.com/sana13792/Assignment-3/blob/main/Images/image_2021-01-28_034739.png) <br/>
## Conclusion
This document has outlined the results obtained by designing a simple CNN architecture and the results obtained by using  data augmentation and transfer learning for attaining better accuracy. The test accuracy was improved to 90% using data augmentation and transfer learning in only 10 epochs.
