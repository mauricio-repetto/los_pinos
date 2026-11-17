# Taller de Visión por Computadora — Los Pinos

Material del taller introductorio de **Visión por Computadora** dictado en Los Pinos (septiembre 2019, según las fechas de los archivos en Drive) por el equipo de ML de UruIT (contactos en las slides: Waldemar López y Davide Andreazzini).

El taller combina una parte teórica (qué es Computer Vision, qué problemas resuelve, clasificación vs. detección, cómo se entrena una red) con dos ejercicios prácticos:

1. **"¡Tierra a la vista baby!"**: clasificador binario que decide si la foto de un cuerpo celeste es el planeta Tierra o no. Es el notebook de este repo.
2. **"¡Hagan lugar que quiero estacionar!"**: detección de lugares libres de estacionamiento con YOLOv3 sobre el dataset COWC (Cars Overhead With Context). Ese notebook vive en Colab y no está en la carpeta de Drive (ver [Links externos](#links-externos)).

## Contenido de las slides

| Bloque | Temas |
|---|---|
| Conceptos | Qué es Computer Vision, disciplinas relacionadas (IA, ML, DL, IoT, procesamiento de imágenes) |
| Casos de uso | Reconocimiento facial, detección de objetos, análisis de video, descripción de imágenes, control de calidad, detección de tumores |
| Clasificación vs. detección | `f(imagen) -> categoría` vs. `f(imagen) -> [{categoría, bounding box}]` |
| Práctica 1: Tierra sí/no | Dataset etiquetado (`train/`, `test/`, `eval/`), aumentación de datos, redes neuronales y CNNs, transfer learning (VGG16, ResNet, InceptionV3, MobileNet), métricas (precision, recall, F1) |
| Práctica 2: Estacionamiento | Dataset COWC (subset Toronto), YOLOv3 pre-entrenado en COCO (~10 h de entrenamiento), evaluación con IoU |

## Estructura del repo

```
los_pinos/
├── README.md
├── drive_assets.json            # IDs de Drive de los archivos que se bajan al repo
├── notebooks/
│   └── finding_earth.ipynb      # Práctica 1: clasificador Tierra / no Tierra
├── slides/
│   └── taller_vision_por_computadora_los_pinos.pdf
└── scripts/
    └── fetch_assets.py          # Re-descarga notebooks y slides desde Drive
```

## El notebook: `notebooks/finding_earth.ipynb`

Pensado para correr en **Google Colab con GPU** y con la carpeta de Drive montada.

1. **Setup**: agregar a tu Drive las carpetas compartidas `corpus` y `space_dataset`, montar Drive y definir la ruta.
2. **Armado del dataset**: a partir de `space_dataset/` (clases `earth`, `moon`, `sun`, `jupiter`, ...) se arma la estructura `train/earth`, `train/no_earth`, etc.
3. **Features (embeddings)**: InceptionV3 pre-entrenado en ImageNet (`include_top=False`) para obtener el vector de cada imagen. Se guardan en `space.csv`.
4. **Visualización**: embeddings en 3D con el [Embedding Projector de TensorBoard](https://projector.tensorflow.org/) (archivos en `project-tensorboard/`) y en 2D con PCA (scikit-learn).
5. **Entrenamiento**: fine-tuning (transfer learning) con InceptionV3 congelado más capas nuevas, aumentación de datos con Keras.
6. **Evaluación**: curvas de accuracy/loss, precision/recall/F1, matriz de confusión (~90% de accuracy), análisis de thresholds y revisión de errores.
7. **Próximos pasos**: pasar a clasificación multiclase (tierra, luna, sol...).

Stack: Python, Keras/TensorFlow, NumPy, pandas, scikit-learn, Matplotlib.

## Archivos pesados en Google Drive (no incluidos en el repo)

El repo solo guarda notebooks y slides. Los datasets, el modelo entrenado y los videos se descargan desde la carpeta de Drive:

**Carpeta raíz:** <https://drive.google.com/drive/folders/1yxsWbQybViIU_odRL0vMRxQ_ypYhE-i7>

| Recurso | Qué es | Tamaño | Link |
|---|---|---|---|
| `corpus/` (`train/`, `test/`, `eval/`) | Dataset ya separado para el clasificador | — | [carpeta](https://drive.google.com/drive/folders/1oR7Z_rm1e6Hw6R7YjLMyAQAsbUju2KLq) |
| `space_dataset/` | Imágenes por clase: `asteroid`, `earth`, `jupiter`, `mars`, `moon`, `others`, `sun`, `venus` | — | [carpeta](https://drive.google.com/drive/folders/1qZd_zU7UZnvjrLI-TBnFK5-VK7a-ba6M) |
| `first_try.h5` | Modelo Keras entrenado (pesos) | 91.9 MB | [archivo](https://drive.google.com/file/d/1YfBx0hpyujJjd_Zyzq_PE7MRge_CUKrD/view) |
| `SUMMARY/space.csv` | Embeddings de InceptionV3 generados por el notebook | — | [carpeta](https://drive.google.com/drive/folders/1OOKmqbj6voHzJul8c9Z8HFH5i6fnLxNV) |
| `project-tensorboard/logdir-1` | Archivos para el Embedding Projector | — | [carpeta](https://drive.google.com/drive/folders/1x0Qd8WJyE6mvDn1lP9UmlmsztC_PinMy) |
| `space_vectors_3D.mp4` | Video de los embeddings en 3D | 17.1 MB | [archivo](https://drive.google.com/file/d/1weffnPqTj_v3jPykfFwqv2_h5fix_6VU/view) |

Para correr el notebook en Colab: botón derecho sobre `corpus` y `space_dataset` → *Organizar → Agregar acceso directo a Drive*, y apuntá la variable de ruta del notebook a esa carpeta.

## Links externos

- Colab de la práctica 1 (versión del taller): <https://colab.research.google.com/drive/1BwsgnWyO5WfBtS8kPmo4-qDBhMtxBdkE>
- Colab de la práctica 2 (YOLOv3 / estacionamiento): <https://colab.research.google.com/drive/1r3uTp8cHLwnL-NNRHxxujfq5XtutXUws>
- Modelo YOLOv3 entrenado sobre COWC: <https://drive.google.com/drive/folders/1xTXsq44HOVxZMVtIc9tbKK3Ty3Ba4o2I>
- Dataset COWC: <https://gdo152.llnl.gov/cowc/>
- Slides originales (Google Slides): <https://docs.google.com/presentation/d/11Ge-59hPgyqAJ-GqRbV3PwvzOs0dL_3jjv3Xccx1Uzg/edit>

## Actualizar notebooks y slides desde Drive

```bash
python scripts/fetch_assets.py          # baja lo que falte
python scripts/fetch_assets.py --force  # vuelve a bajar todo
```

El script lee `drive_assets.json`, exporta las slides a PDF y baja los notebooks. No toca los archivos pesados.
