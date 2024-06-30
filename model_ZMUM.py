import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import RMSprop, SGD, Adam 
from keras import regularizers
from keras.layers import Input, Dense, Reshape, Flatten, LSTM, Dropout, GRU
from keras.models import save_model

def create_features(df, label=None):
    df['date'] = df.index
    df['hour'] = df['date'].dt.hour
    df['dayofweek'] = df['date'].dt.dayofweek
    df['quarter'] = df['date'].dt.quarter
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['dayofyear'] = df['date'].dt.dayofyear
    df['dayofmonth'] = df['date'].dt.day
    df['AEP_MW'] = df[label]
    
    X = df[['hour','dayofweek','quarter','month','year',
           'dayofyear','dayofmonth', 'AEP_MW']]

    return X

def dataset(df, input_length, target_length):
    data = df.values
    inputs = []
    targets = []

    for i in range(len(data) - input_length - target_length + 1):
        inputs.append(data[i:i+input_length])
        targets.append(data[i+input_length:i+input_length+target_length, 7])
    
    inputs = np.array(inputs)
    targets = np.array(targets)
    
    inputs = inputs[None, :]
    targets = targets[None, :]
    dataset = tf.data.Dataset.from_tensor_slices((inputs, targets))
    
    return dataset

pjme = pd.read_csv('./AEP_hourly.csv', index_col=[0], parse_dates=[0])

split_date_1 = '09-Jun-2014' #treningowy na poziomie 70% calosci
split_date_2 = '06-Jul-2016' #walidacyjny na poziomie 15% calosci
pjme_train = pjme.loc[pjme.index <= split_date_1].copy()
pjme_val = pjme.loc[(pjme.index > split_date_1) & (pjme.index <= split_date_2)].copy()
pjme_test = pjme.loc[pjme.index > split_date_2].copy()

df_train = create_features(pjme_train, label='AEP_MW')
df_val = create_features(pjme_val, label='AEP_MW')
df_test = create_features(pjme_test, label='AEP_MW')

input_length = 23
target_length = 1

dataset_train = dataset(df_train, input_length, target_length) # z ostatnich 23 godzin na najbliższą godzinę
dataset_val = dataset(df_val, input_length, target_length) # z ostatnich 23 godzin na najbliższą godzinę 
dataset_test = dataset(df_test, input_length, target_length) # z ostatnich 23 godzin na najbliższą godzinę  

mean_AEP_MW_test = df_test['AEP_MW'].mean()
std_AEP_MW_test = df_test['AEP_MW'].std()

# Określenie liczby kolumn danych wejściowych
column_names = df_train.columns
num_col = len(column_names)

model = Sequential()
model.add(Reshape((input_length * num_col,), input_shape=(input_length, num_col)))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(1))

model.compile(optimizer=RMSprop(), loss='mse', metrics=['mae'])

history = model.fit(dataset_train, epochs=100, validation_data=dataset_val)

# Zapisanie modelu do pliku
model.save('./dense_7.keras')

test_mae = model.evaluate(dataset_test)[1]
print(f"Test MAE: {test_mae:.2f}")

# Wyodrębnienie historii straty i metryki z historii treningu
loss = history.history['loss']
val_loss = history.history['val_loss']
mae = history.history['mae']
val_mae = history.history['val_mae']

epochs = range(1, len(loss) + 1)

# Rysowanie krzywej straty
plt.figure()
plt.plot(epochs, loss, 'r-', label='Strata trenowania')
plt.plot(epochs, val_loss, 'b-', label='Strata walidacji')
plt.title('Krzywe uczenia - strata')
plt.xlabel('Epoki')
plt.ylabel('Strata')
plt.legend()

plt.show()

# Rysowanie krzywej metryki
plt.figure()
plt.plot(epochs, mae, 'r-', label='MAE trenowania')
plt.plot(epochs, val_mae, 'b-', label='MAE walidacji')
plt.title('Krzywe uczenia - MAE')
plt.xlabel('Epoki')
plt.ylabel('MAE')
plt.legend()

plt.show()

predictions = model.predict(dataset_test).flatten()

real_data = pd.DataFrame({
    'Date': pjme_test['date'],
    'Power_consumption': pjme_test['AEP_MW'].round(1)
})

predicted_data = pd.DataFrame({
    'Date': pjme_test['date'].iloc[input_length:],
    'Power_consumption': predictions.round(1)
})

predicted_data.to_csv('predictions/predictions.csv', index=True)
real_data.to_csv('predictions/real.csv', index=True)


