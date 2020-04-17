FROM jupyter/scipy-notebook
LABEL maintainer="Shigeru Kitazaki <skitazaki@gmail.com>"

USER $NB_UID

RUN conda install --yes --quiet \
    'psycopg2=2.8*' \
    && conda install --yes --quiet -c sodre 'ipython-sql=0.3*' \
    && conda clean -tipsy
