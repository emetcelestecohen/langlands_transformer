import numerapi

napi = numerapi.NumerAPI()

models = napi.get_models()

print("Your Numerai Models:")
for model_name, model_id in models.items():
    print(f"Model: {model_name} | Model ID: {model_id}")
