from sklearn.metrics import f1_score, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import sklearn

# df.Purchased.value_counts()


def train_knn_classifier(train_set, val_set):
    """
    kNN hyperparameters and models
    """
    params = {
        'n_neighbors': 5,
        'weights': 'distance',
        'algorithm': 'auto',
        'p': 2
    }
    model = sklearn.neighbors.KNeighborsClassifier(**params)
    model.fit(train_set['X'], train_set['y'])
    return model


def standard_scaler(train_set, val_set):
    """
    Standard Scalarization of training and validation dataset
    """
    _sc = StandardScaler()
    train_set['X'] = _sc.fit_transform(train_set['X'])
    val_set['X'] = _sc.transform(val_set['X'])
    return train_set, val_set


def split_dataset(df, label_col):
    """
    Split dataset to train and validation dataset
    """
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop(label_col, axis=1), df[label_col], random_state=0)
    train_set = {'X': X_train, 'y': y_train}
    val_set = {'X': X_test, 'y': y_test}
    return train_set, val_set


if __name__ == "__main__":
    X = df.copy()
    X['Gender'] = (X['Gender'] == 'Male').astype(int)

    train_set, val_set = standard_scaler(*split_dataset(X, 'Purchased'))
    model = train_knn_classifier(train_set, val_set)

    y_pred = model.predict(val_set['X'])
    y_test = val_set['y']
    print("KNN f1 socre", f1_score(y_test, y_pred))
    print("KNN accuracy socre", accuracy_score(y_pred, y_test))
    print("KNN Metrics \n", confusion_matrix(y_pred, y_test))
