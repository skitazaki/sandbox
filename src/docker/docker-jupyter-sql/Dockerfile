FROM jupyter/scipy-notebook
LABEL maintainer="Shigeru Kitazaki <skitazaki@gmail.com>"

USER $NB_UID

RUN conda install --yes --quiet \
    'psycopg2=2.8*' \
    'pandas-datareader=0.8.1' \
    'openpyxl=3.0.3' \
    'networkx=2.4' \
    'ipython-sql=0.3*' \
    'pgspecial=1.11*' \
    && conda clean -tipsy

USER root
RUN mkdir -p /data \
    && fix-permissions /data

USER $NB_UID
