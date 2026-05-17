import io
import numpy as np
import librosa
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .apps import DetectionConfig


from django.shortcuts import render

def drone_page(request):
    return render(request, 'detection/drone.html')

def preprocess_audio(audio_bytes):
    y, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    max_pad_len = 174
    if mfccs.shape[1] < max_pad_len:
        mfccs = np.pad(mfccs, ((0, 0), (0, max_pad_len - mfccs.shape[1])), mode='constant')
    else:
        mfccs = mfccs[:, :max_pad_len]
    mfccs_scaled = DetectionConfig.scaler.transform(mfccs.flatten().reshape(1, -1))
    return mfccs_scaled.reshape(1, 40, 174, 1)

@method_decorator(csrf_exempt, name='dispatch')
class PredictView(View):
    def post(self, request):
        if 'audio' not in request.FILES:
            return JsonResponse({"error": "No audio file"}, status=400)
        try:
            processed = preprocess_audio(request.FILES['audio'].read())
            prediction = DetectionConfig.model.predict(processed)
            result_index = int(np.argmax(prediction[0]))
            return JsonResponse({
                "label": ['Drone', 'Not Drone'][result_index],
                "confidence": float(np.max(prediction[0])),
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)