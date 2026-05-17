from django.apps import AppConfig

class DetectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'detection'
    model = None
    scaler = None

    def ready(self):
        import keras          # ← بدل tf.keras
        import joblib

        DetectionConfig.model = keras.models.load_model('drone_detection_model.keras')
        DetectionConfig.scaler = joblib.load('mfcc_scaler.joblib')