from kfp import dsl

@dsl.component(base_image="python:3.11", packages_to_install=["scikit-learn"])
def load_data(test_size: float
      , train_out: dsl.OutputPath('numpy'), test_out: dsl.OutputPath('numpy')):

   from sklearn.datasets import load_iris
   from sklearn.model_selection import train_test_split
   import pickle

   iris_data = load_iris()

   X_data = iris_data.get('data')
   y_data = iris_data.get('target')

   X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=test_size)

   # write train data 
   with open(train_out, "wb") as f:
      pickle.dump((X_train, y_train), f)

   # write test data 
   with open(test_out, "wb") as f:
      pickle.dump((X_test, y_test), f)

@dsl.component(base_image="python:3.11", packages_to_install=["scikit-learn"])
def train_model(train_in: dsl.InputPath('numpy'), model_out: dsl.OutputPath('model')):
   from sklearn import svm
   import pickle

   # read in the training data
   with open(train_in, "rb") as f:
      X_train, y_train = pickle.load(f)

   # train
   model_svm = svm.SVC()
   model_svm.fit(X_train, y_train)

   # save the trained model
   with open(model_out, "wb") as f:
      pickle.dump(model_svm, f)

@dsl.component(base_image="python:3.11", packages_to_install=["scikit-learn"])
def predict(test_in: dsl.InputPath('numpy'), model_in: dsl.InputPath('model')):

   from sklearn import metrics
   import pickle

   # read test data
   with open(test_in, 'rb') as f:
      X_test, y_test = pickle.load(f)

   with open(model_in, 'rb') as f:
      model = pickle.load(f)

   prediction_svm = model.predict(X_test)
   score = metrics.accuracy_score(prediction_svm, y_test)

   print('****** SVM accuracy: ', score)

@dsl.pipeline(name="iris-pipeline")
def iris_pipeline(test_size: float):

   # load the data: train_out, test_out
   load_data_step = load_data(test_size=test_size)

   # pass the training data to the training component: model_out
   train_model_step = train_model(train_in=load_data_step.outputs['train_out'])

   # call prediction step with test data and model
   predict(test_in=load_data_step.outputs['test_out'],
         model_in=train_model_step.outputs['model_out'])


