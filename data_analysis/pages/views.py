import os
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
from plotly.subplots import make_subplots 
import json
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import UploadFileForm
from .models import UploadedFile
from typing import Dict, List, Tuple, Any

class DataAnalyzer:
    """Classe utilitaire pour l'analyse des données"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_columns = df.select_dtypes(include=['number']).columns
        self.categorical_columns = df.select_dtypes(include=['object']).columns
        
    def get_basic_stats(self) -> Dict[str, Any]:
        """Calcule les statistiques de base du DataFrame"""
        return {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'memory_usage': f"{self.df.memory_usage(deep=True).sum() / 1024:.2f} KB",
            'numeric_columns': len(self.numeric_columns),
            'categorical_columns': len(self.categorical_columns),
            'duplicate_rows': self.df.duplicated().sum()
        }
    
    def get_column_analysis(self) -> Dict[str, Dict[str, Any]]:
        """Analyse détaillée de chaque colonne"""
        analysis = {}
        for col in self.df.columns:
            col_type = str(self.df[col].dtype)
            missing = self.df[col].isnull().sum()
            missing_pct = (missing / len(self.df)) * 100
            
            analysis[col] = {
                'type': col_type,
                'missing': missing,
                'missing_pct': f"{missing_pct:.2f}%",
                'unique_values': self.df[col].nunique()
            }
            
            if col in self.numeric_columns:
                analysis[col].update({
                    'mean': f"{self.df[col].mean():.2f}",
                    'median': f"{self.df[col].median():.2f}",
                    'std': f"{self.df[col].std():.2f}",
                })
            elif col in self.categorical_columns:
                analysis[col].update({
                    'most_common': self.df[col].mode().iloc[0] if not self.df[col].mode().empty else None,
                    'most_common_count': self.df[col].value_counts().iloc[0] if not self.df[col].value_counts().empty else 0
                })
                
        return analysis

    def create_visualization(self, plot_type: str, x_col: str = None, y_col: str = None) -> Dict[str, Any]:
        """Crée une visualisation Plotly en fonction du type demandé"""
        try:
            if plot_type == "histogram":
                fig = px.histogram(self.df, x=x_col, title=f'Distribution de {x_col}')
            
            elif plot_type == "box":
                fig = px.box(self.df, y=y_col, title=f'Boîte à moustaches de {y_col}')
            
            elif plot_type == "scatter":
                fig = px.scatter(self.df, x=x_col, y=y_col, 
                               title=f'Nuage de points: {x_col} vs {y_col}')
            
            elif plot_type == "bar":
                if x_col in self.categorical_columns:
                    data = self.df[x_col].value_counts()
                    fig = px.bar(x=data.index, y=data.values, 
                                title=f'Distribution de {x_col}')
                else:
                    fig = px.bar(self.df, x=x_col, y=y_col, 
                                title=f'Graphique en barres: {x_col} vs {y_col}')
            
            elif plot_type == "correlation":
                corr_matrix = self.df[self.numeric_columns].corr()
                fig = px.imshow(corr_matrix, 
                              title="Matrice de corrélation",
                              labels=dict(color="Corrélation"))
            
            else:
                raise ValueError(f"Type de graphique non supporté: {plot_type}")

            # Personnalisation du layout
            fig.update_layout(
                template='plotly_white',
                plot_bgcolor='white',
                font=dict(size=12),
                margin=dict(l=40, r=40, t=40, b=40)
            )
            
            return {
                'success': True,
                'plot_data': fig.to_json()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }



def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file_instance = form.save()
                df = pd.read_csv(file_instance.file.path)
                if df.empty:
                    raise ValueError("Le fichier est vide")
                messages.success(request, 
                    f"Fichier '{file_instance.file.name}' uploadé avec succès! "
                    f"({len(df)} lignes, {len(df.columns)} colonnes)")
                return redirect('data_overview')
            except Exception as e:
                messages.error(request, f"Erreur lors du traitement du fichier: {str(e)}")
                return redirect('upload_file')
    else:
        form = UploadFileForm()

   
    context = {'form': form, 'base_html': 'base.html'}
    return render(request, 'pages/upload.html', context)

def data_overview(request):
    """Vue pour l'aperçu des données"""
    file = UploadedFile.objects.last()
    if not file:
        messages.warning(request, "Aucun fichier n'a encore été uploadé.")
        return render(request, 'pages/overview.html')

    try:
        # Lecture du fichier
        df = pd.read_csv(file.file.path)
        analyzer = DataAnalyzer(df)
        
        # Analyse des données
        basic_stats = analyzer.get_basic_stats()
        column_analysis = analyzer.get_column_analysis()
        
        # Conversion de `missing_pct` en flottant si nécessaire
        for key, analysis in column_analysis.items():
            if "missing_pct" in analysis and isinstance(analysis["missing_pct"], str):
                try:
                    analysis["missing_pct"] = float(analysis["missing_pct"])
                except ValueError:
                    analysis["missing_pct"] = 0.0  # Valeur par défaut si la conversion échoue

       

        # Préparation du contexte pour le rendu
        context = {
            'file_name': file.file.name,
            'basic_stats': basic_stats,
            'column_analysis': column_analysis,
            'columns': df.columns.tolist(),
            'preview': df.head(10).to_html(
                classes='table table-striped table-hover',
                index=False,
                float_format=lambda x: f'{x:.2f}' if isinstance(x, float) else x
            ),
        }
   
        return render(request, 'pages/overview.html', context)

    except Exception as e:
        # Gestion des erreurs
        messages.error(request, f"Erreur lors de l'analyse des données: {str(e)}")
        return render(request, 'pages/overview.html', {'error': str(e)})


def visualize_data(request):
    """Vue pour la visualisation interactive des données"""
    file = UploadedFile.objects.last()
    if not file:
        messages.warning(request, "Aucun fichier n'a encore été uploadé.")
        return render(request, 'pages/visualize.html')

    try:
        df = pd.read_csv(file.file.path)
        analyzer = DataAnalyzer(df)
        
        context = {
            'columns': df.columns.tolist(),
            'numeric_columns': analyzer.numeric_columns.tolist(),
            'categorical_columns': analyzer.categorical_columns.tolist(),
            'visualization_types': [
                {'value': 'histogram', 'label': 'Histogramme'},
                {'value': 'box', 'label': 'Boîte à moustaches'},
                {'value': 'scatter', 'label': 'Nuage de points'},
                {'value': 'bar', 'label': 'Graphique en barres'},
                {'value': 'correlation', 'label': 'Matrice de corrélation'}
            ]
        }
        
        return render(request, 'pages/visualize.html', context)
        
    except Exception as e:
        messages.error(request, f"Erreur lors du chargement des données: {str(e)}")
        return render(request, 'pages/visualize.html', {'error': str(e)})

@require_POST
def update_visualization(request):
    """Vue API pour mettre à jour les visualisations de manière asynchrone"""
    try:
        data = json.loads(request.body)
        plot_type = data.get('plot_type')
        x_column = data.get('x_column')
        y_column = data.get('y_column')
        
        file = UploadedFile.objects.last()
        if not file:
            return JsonResponse({'error': 'Aucun fichier disponible'}, status=400)
            
        df = pd.read_csv(file.file.path)
        analyzer = DataAnalyzer(df)
        
        result = analyzer.create_visualization(plot_type, x_column, y_column)
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
def home(request):
    """Vue pour la page d'accueil"""
    return render(request, 'pages/home.html')

