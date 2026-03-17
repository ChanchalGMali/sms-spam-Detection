import os
from django.conf import settings

model_path = os.path.join(settings.BASE_DIR, 'model.pkl')
model = pickle.load(open(model_path, 'rb'))

