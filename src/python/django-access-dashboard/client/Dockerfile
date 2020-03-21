FROM skitazaki/nodejs
MAINTAINER Shigeru Kitazaki <skitazaki@gmail.com>

RUN cp -p bower_components/nvd3/nv.d3.css bower_components/nvd3/nv.d3.scss
RUN mv bower_components app/

RUN sed -i 's;http://localhost:8000/;/;g' app/scripts/main.coffee

RUN grunt build
VOLUME /app/dist

