import joblib
from django.shortcuts import render
from .forms import AcidenteForm
import pandas as pd
import os
from sklearn.preprocessing import OneHotEncoder

def load_models():
    base_path = os.path.join(os.path.dirname(__file__), 'ml_models')
    models = {}
    try:
        models['lightgbm'] = joblib.load(os.path.join(base_path, 'lightgbm_model.pkl'))
        models['random_forest'] = joblib.load(os.path.join(base_path, 'random_forest_model.pkl'))
        models['xgboost'] = joblib.load(os.path.join(base_path, 'xgboost_model.pkl'))
    except FileNotFoundError as e:
        print(f"Model file not found: {e}")
    except Exception as e:
        print(f"Error loading model: {e}")
    return models

models = load_models()

def predict_acidente(request):
    if request.method == 'POST':
        form = AcidenteForm(request.POST)
        if form.is_valid():
            numero_ocorrencia = form.cleaned_data['Numero_Ocorrencia'] or 'default_value'
            data = form.cleaned_data['Data'] or 'default_value'
            localidade = form.cleaned_data['Localidade']
            uf = form.cleaned_data['UF']
            aerodromo = form.cleaned_data['Aerodromo']
            operacao = form.cleaned_data['Operacao']

            # Criar DataFrame com os dados do formulário
            data = {
                'Numero_Ocorrencia': [numero_ocorrencia],
                'Data': [data],
                'Localidade': [localidade],
                'UF': [uf],
                'Aerodromo': [aerodromo],
                'Operacao': [operacao]
            }
            df = pd.DataFrame(data)

            # Codificar variáveis categóricas
            categorical_features = ['Localidade', 'UF', 'Aerodromo', 'Operacao']
            encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
            encoder.fit(df[categorical_features])
            encoded_data = encoder.transform(df[categorical_features])
            encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_features))

            # Concatenar com as colunas não categóricas
            processed_df = pd.concat([df.drop(columns=categorical_features), encoded_df], axis=1)

            # Imprimir colunas do DataFrame para debug
            print("Colunas do DataFrame processado:")
            print(processed_df.columns)

            # Reordenar as colunas de acordo com a ordem esperada pelo modelo
            processed_df = processed_df[['Numero_Ocorrencia', 'Data'] + list(encoded_df.columns)]

            # Inicializar um dicionário para as previsões
            predictions = {}
            for name, model in models.items():
                try:
                    # Prever com o modelo
                    prediction = model.predict(processed_df)[0]
                    predictions[name] = prediction
                except Exception as e:
                    predictions[name] = f"Error: {e}"

            return render(request, 'resultado.html', {'predictions': predictions})

    else:
        form = AcidenteForm()

    return render(request, 'formulario.html', {'form': form})
