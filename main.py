from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

iris_data = load_iris()

X_data = iris_data.get('data')
y_data = iris_data.get('target')

X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.1)

# training
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

model_svm = svm.SVC()
model_svm.fit(X_train, y_train)

prediction_svm = model_svm.predict(X_test)
score = metrics.accuracy_score(prediction_svm, y_test)

print('SVM accuracy: ', metrics.accuracy_score(prediction_svm, y_test))

