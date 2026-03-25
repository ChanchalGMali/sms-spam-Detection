from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from .forms import MessageForm


# -------- REGISTER VIEW --------
def register(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


# ---- Load dataset ----
import os 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataset = pd.read_csv(os.path.join(BASE_DIR,"emails.csv"))

# ---- Vectorize ----
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(dataset['text'])
y = dataset['spam']

# ---- Split ----
x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---- Train model ----
model = MultinomialNB()
model.fit(x_train, y_train)


def predictMessage(message):
    messageVector = vectorizer.transform([message])
    prediction = model.predict(messageVector)
    return 'Spam' if prediction[0] == 1 else 'Ham'

@login_required

def Home(request):
    return render(request, 'home.html')
    result = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['text']
            result = predictMessage(message)
    else:
        form = MessageForm()

    return render(request, 'home.html', {
        'form': form,
        'result': result
    })
