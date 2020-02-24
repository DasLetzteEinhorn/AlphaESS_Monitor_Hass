ARG BUILD_FROM=hassioaddons/base:7.0.0
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Copy root filesystem
COPY rootfs /

# Setup base
RUN apk add --no-cache \
    coreutils=8.31-r0 \
    wget=1.20.3-r0

RUN apt-get update
# RUN apt-get install software-properties-common -y
# RUN add-apt-repository ppa:canonical-chromium-builds/stage -y
# RUN apt-get update
# RUN apt-get install chromium-browser -y
RUN apt-get install chromium-chromedriver -y

# Build arguments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_REF
ARG BUILD_VERSION

# Labels
LABEL \
    io.hass.name="AlphaESS Monitor" \
    io.hass.description="AlphaESS Monitor add-on by DasLetzteEinhorn" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="DasLetzteEinhorn <jo.fritsche@gmail.com>" \
    org.label-schema.description="AlphaESS Monitor add-on by DasLetzteEinhorn" \
    org.label-schema.build-date=${BUILD_DATE} \
    org.label-schema.name="AlphaESS Monitor" \
    org.label-schema.schema-version="0.0.1" \
    org.label-schema.url="https://addons.community" \
    org.label-schema.usage="https://github.com/hassio-addons/addon-example/tree/master/README.md" \
    org.label-schema.vcs-ref=${BUILD_REF} \
    org.label-schema.vcs-url="https://github.com/hassio-addons/addon-example" \
    org.label-schema.vendor="DasLetzeEinhorn"
